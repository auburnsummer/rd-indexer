const Database = require('better-sqlite3');
const YAML = require("js-yaml");
const fs = require("fs/promises");
const {map, difference, toPairs, pipe, isBoolean, get, filter, identity, chunk} = require("lodash/fp");
const {analyse} = require("./vitals");
const upload = require("./vitals/lib/upload/upload");
const {default: PQueue} = require('p-queue');
const { fromPairs } = require('lodash');
const brotli = require('brotli');

const queue = new PQueue({concurrency: 3});


const driverMap = {
    "legacySheet": require("./sources/legacySheet")
}

// IN an object, convert false to 0 and true to 1.
const convertBoolsToInts = pipe(
    toPairs,
    map(([k, v]) => isBoolean(v) ? [k, Number(v)] : [k, v]),
    fromPairs
);

const addLevels = (db, levels) => {
    // status
    const insertStatus = db.prepare(`
        INSERT OR IGNORE INTO status (id, uploaded)
        VALUES (@id, @uploaded)
    `);
    const insertLevel = db.prepare(`
        INSERT INTO level (
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
        INSERT INTO level_tag (id, tag, seq)
        VALUES (@id, @tag, @seq)
    `);
    const insertAuthor = db.prepare(`
        INSERT INTO level_author (id, author, seq)
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
    console.log(`To add: ${iidsToAdd.length} | To remove: ${iidsToRemove.length}`);

    // Remove levels.
    map(removeIid(db, id), iidsToRemove);

    // for tracking progress.
    let count = 0;
    queue.on('active', () => {
        console.log(`Working on item #${++count} / ${iidsToAdd.length}.  Q size: ${queue.size}  Q pending: ${queue.pending}`);
    });

    for (let addChunk of chunk(10, iidsToAdd)) {
        try {
            const result = await queue.addAll(map(processIid(id, dr), addChunk));
            addLevels(db, filter(identity, result));
        } catch (err) {
            console.log(err);
            continue;
        }
    }
    // ...then add them.
}

const doIndex = async (dbFileName, srcFileName) => {
    const db = new Database(dbFileName);
    const sources = await fs.readFile(srcFileName, 'utf-8').then(YAML.load);

    await runDriver({...sources[0], db})
    db.close();
    console.log("done!");
}

const doUpload = async (dbFileName) => {
    const compBuffer = await fs.readFile(dbFileName).then(brotli.compress);
    await upload(compBuffer, "db.br", "orchard");
    console.log("done!");
}

module.exports = {doIndex, doUpload}