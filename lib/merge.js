const Database = require("better-sqlite3");

const defaultInserter = table => `INSERT INTO main.${table} SELECT * FROM other.${table}`;

const tablesToCopy = [
    ["status", table => `INSERT INTO main.${table} SELECT * FROM other.${table} WHERE other.${table}.id IN (SELECT id FROM main.level)`],
    ["user", defaultInserter],
    ["user_level", defaultInserter],
];

function doMerge (pathA, pathB) {
    console.log("loading level database...");
    const dbA = new Database(pathA);
    console.log("attaching hub database...");
    dbA.prepare(`ATTACH '${pathB}' AS other`).run();
    console.log("copying tables...");
    // copy tables from B directly. we don't need to retain any changes in A.
    for (let [table, f] of tablesToCopy) {
        console.log(`copying table ${table}...`);
        dbA.prepare(`DELETE FROM main.${table}`).run();
        dbA.prepare(f(table)).run();
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