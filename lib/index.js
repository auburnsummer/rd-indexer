const Database = require('better-sqlite3');
const YAML = require("js-yaml");
const fs = require("fs/promises");
const {map, difference, toPairs, pipe, isBoolean, get} = require("lodash/fp");
const {analyse} = require("./vitals");
const { fromPairs } = require('lodash');

// Map of driver shortnames (referenced in sources.yml) to modules. these all comply to the same interface.
const driverMap = {
    "legacySheet": require("./sources/legacySheet"),
    "discord": require("./sources/discord"),
    "workshop": require("./sources/workshop")
}

// In an object, convert false to 0 and true to 1.
const convertBoolsToInts = pipe(
    toPairs,
    map(([k, v]) => isBoolean(v) ? [k, Number(v)] : [k, v]),
    fromPairs
);

const addLevel = (db, level) => {
    // level. if it already exists, just update the source id and iid.
    // this has the effect of giving later sources in the sources.yml higher 'priority'.
    const insertLevel = db.prepare(`
        INSERT INTO level (
            id, artist, song, difficulty, seizure_warning, description,
            max_bpm, min_bpm, last_updated, single_player, two_player, thumb,
            url, url2, icon, hue, tags, authors, has_classics, has_oneshots, has_squareshots,
            has_swing, has_freetimes, has_holds, source_id, source_iid
        ) VALUES (
            @id, @artist, @song, @difficulty, @seizure_warning, @description,
            @max_bpm, @min_bpm, @last_updated, @single_player, @two_player, @thumb,
            @url, @url2, @icon, @hue, json(@tags), json(@authors), @has_classics, @has_oneshots, @has_squareshots,
            @has_swing, @has_freetimes, @has_holds, @source_id, @source_iid 
        )
        ON CONFLICT (id) DO UPDATE SET
            source_id=excluded.source_id,
            source_iid=excluded.source_iid
    `);

    const insert = db.transaction(level => {
        const toInsert = {
            ...convertBoolsToInts(level),
            authors: JSON.stringify(level.authors),
            tags: JSON.stringify(level.tags)
        }
        insertLevel.run(toInsert);
    });
    insert(level);
}

const getIidDiff = (db, source_id, proposed_iids) => {
    const getCurrentIids = db.prepare(`
        SELECT source_iid FROM level
        WHERE source_id = @source_id
    `);
    const currentIids = map(get("source_iid"), getCurrentIids.all({source_id}));
    const iidsToAdd = difference(proposed_iids, currentIids);
    const iidsToRemove = difference(currentIids, proposed_iids);
    return {iidsToAdd, iidsToRemove};
}

// hecc
const processIid = (id, dr) => iid => async () => {
    try {   
        const buffer = await dr.get(iid);
        const vitalsResults = await analyse(buffer);
        // non-hosted url, if it's available.
        let url = null;
        if (!dr.rehost) {
            url = await dr.getDownloadLink(iid)
        }

        return {
            ...vitalsResults,
            url,
            url2: vitalsResults.url,
            source_id: id,
            source_iid: iid
        }
    }
    catch (err) {
        console.log(err);
        return false;
    }
}

const removeIid = (db, id) => iid => {
    const removeLevel = db.prepare(
        `DELETE FROM level
        WHERE source_iid = @iid
        AND source_id = @id
        `
    )
    removeLevel.run({iid, id});
}

const runDriver = async ({db, id, driverName, args}) => {
    const Driver = driverMap[driverName];
    const dr = new Driver(args);
    console.log("Initialising driver...");
    await dr.init();
    console.log("Getting iids...");
    const iids = await dr.getIids();

    const {iidsToAdd, iidsToRemove} = getIidDiff(db, id, iids);
    console.log(`[${id}] To add: ${iidsToAdd.length} | To remove: ${iidsToRemove.length}`);
    console.log(iidsToAdd);

    // trackers.
    let count = 0;
    let successes = 0;
    let failuresDueToVitals = 0;
    let failuresDueToDB = 0;

    // Remove levels.
    map(removeIid(db, id), iidsToRemove);

    // add levels.
    for (let iid of iidsToAdd) {
        console.log(`[${id}] #${count} / ${iidsToAdd.length} : ${iid}`);
        count += 1;
        const parsed = await processIid(id, dr)(iid)();
        // processIid returns false if a error occured parsing it.
        if (!parsed) {
            console.log("An error occured in vitals, we will have printed it above. bailing out now.");
            failuresDueToVitals += 1;
            continue;
        }
        console.log(`id: ${parsed.id}`);
        // if we're here, we can add the level.
        try {
            addLevel(db, parsed);
            successes += 1;
        }
        catch (err) {
            console.log(err);
            console.log("An error occured adding it to the DB, we will have printed it above. bailing out now.");
            failuresDueToDB += 1;
        }
    }
    console.log(`
RESULTS ${id}
=======
${count} total
${successes} successes
${failuresDueToVitals} vitals errors
${failuresDueToDB} DB errors
    `)
    console.log("Running cleanup...")
    await dr.cleanup();

    return;
}

const doIndex = async (dbFileName, srcFileName) => {
    console.log("Loading database...");
    const db = new Database(dbFileName);
    const sources = await
        fs.readFile(srcFileName, 'utf-8')
        .then(s => {
            const re = /{env!(.+?)}/g;
            return s.replaceAll(re, (_, p1) => {
                return process.env[p1];
            });
        })
        .then(YAML.load);

    console.log(`Indexing ${sources.length} sources...`)
    for (let source of sources) {
        console.log(`Beginning index of source ${source.id}...`);
        try {
            await runDriver({...source, db})
        }
        catch (err) {
            console.log(`an error occured while indexing source ${source.id}:`)
            console.log(err);
        }
    }

    db.close();
    console.log("done!");
} 

module.exports = {doIndex}