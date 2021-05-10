const Database = require('better-sqlite3');
const YAML = require("js-yaml");
const fs = require("fs/promises");
const {map, difference, toPairs, pipe, isBoolean, get, filter, identity, chunk} = require("lodash/fp");
const {analyse} = require("./vitals");
const {default: PQueue} = require('p-queue');
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

const addLevels = (db, levels) => {
    // status. most values are default, except for @id and @uploaded.
    const insertStatus = db.prepare(`
        INSERT OR IGNORE INTO status (id, uploaded)
        VALUES (@id, @uploaded)
    `);
    const insertLevel = db.prepare(`
        INSERT OR IGNORE INTO level (
            id, artist, song, difficulty, seizure_warning, description,
            max_bpm, min_bpm, last_updated, single_player, two_player, thumb,
            url, url2, icon, hue, has_classics, has_oneshots, has_squareshots,
            has_swing, has_freetimes, has_holds, source_id, source_iid
        ) VALUES (
            @id, @artist, @song, @difficulty, @seizure_warning, @description,
            @max_bpm, @min_bpm, @last_updated, @single_player, @two_player, @thumb,
            @url, @url2, @icon, @hue, @has_classics, @has_oneshots, @has_squareshots,
            @has_swing, @has_freetimes, @has_holds, @source_id, @source_iid 
        )
    `);
    const insertTag = db.prepare(`
        INSERT OR IGNORE INTO level_tag (id, tag, seq)
        VALUES (@id, @tag, @seq)
    `);
    const insertAuthor = db.prepare(`
        INSERT OR IGNORE INTO level_author (id, author, seq)
        VALUES (@id, @author, @seq)
    `);

    // lodash/fp map doesn't have index by default
    const _map = map.convert({'cap': false});

    const insert = db.transaction(map(level => {
        insertStatus.run({id: level.id, uploaded: Math.floor(Date.now() / 1000)})
        insertLevel.run(convertBoolsToInts(level));
        _map((v, i) => insertTag.run({id: level.id, tag: v, seq: i}), level.tags);
        _map((v, i) => insertAuthor.run({id: level.id, author: v, seq: i}), level.authors);
    }));

    insert(levels);
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
    catch {
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
    await dr.init();
    const iids = await dr.getIids();

    const {iidsToAdd, iidsToRemove} = getIidDiff(db, id, iids);
    console.log(`[${id}] To add: ${iidsToAdd.length} | To remove: ${iidsToRemove.length}`);
    console.log(iidsToAdd);
    const queue = new PQueue({concurrency: 3});

    // Remove levels.
    map(removeIid(db, id), iidsToRemove);

    // for tracking progress.
    let count = 0;
    let successes = 0;
    queue.on('active', () => {
        console.log(`[${id}] #${count} / ${iidsToAdd.length} : ${iidsToAdd[count]}`);
        count++;
    });

    for (let addChunk of chunk(1, iidsToAdd)) {
        try {
            const result = await queue.addAll(map(processIid(id, dr), addChunk));
            // if processing the IID failed, processIid returns false...
            const successfulResults = filter(identity, result);
            addLevels(db, successfulResults);
            successes += successfulResults.length;
        } catch (err) {
            console.log(err);
            continue;
        }
    }
    console.log("Running cleanup...")
    await dr.cleanup();

    return successes;
    
}

const doIndex = async (dbFileName, srcFileName) => {
    console.log("Starting index...");
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
    
    console.log(sources);

    const successesPerSource = {}
    console.log(`Indexing ${sources.length} sources...`)
    for (let source of sources) {
        console.log(`Indexing source ${source.id}...`);
        try {
            const successes = await runDriver({...source, db})
            console.log(`Added ${successes} levels from source ${source.id}.`)
            successesPerSource[source.id] = successes;
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