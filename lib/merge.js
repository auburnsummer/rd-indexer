const Database = require("better-sqlite3");

const tablesToCopy = [
    "status",
    "user",
    "user_level"
];

function doMerge (pathA, pathB) {
    console.log("loading level database...");
    const dbA = new Database(pathA);
    console.log("attaching hub database...");
    dbA.prepare(`ATTACH '${pathB}' AS other`).run();
    console.log("copying tables...");
    // copy tables from B directly. we don't need to retain any changes in A.
    for (let table of tablesToCopy) {
        console.log(`copying table ${table}...`);
        dbA.prepare(`DELETE FROM main.${table}`).run();
        dbA.prepare(`INSERT INTO main.${table} SELECT * FROM other.${table}`).run();
    }
    // if there are any remaning levels in A that don't have a corresponding status in B, make
    // it now.
    const result = dbA.prepare(`
    INSERT INTO main.status (id, uploaded)
    SELECT level.id, strftime('%s', 'now') FROM level
    LEFT JOIN status
    ON level.id = status.id
    WHERE status.id IS NULL
`).run();
    console.log(result);

    dbA.close();
}

module.exports = { doMerge }