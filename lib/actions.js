/*
Actions are things that we do to the sqlite database

i.e. approvals, etc.

They go in a queue (lodge.seelie.dev) and we process them here
*/

const { default: axios } = require("axios");

// seelie.dev is my own domain!
// I'm using it to host small, occasionally useful, sometimes mischievous tools + utilities
// i'll make a nice website listing the utilities when i have time.
// for instance, lodge.seelie.dev stores JSON data and edits it with json patch.
const API_URL = "https://lodge.seelie.dev/fdc043b4d9fa1535cf9951c6ea2891ae0ba032b247959bbde5eaae1ba391e0f7";

const getActions = async () => {
    return axios({
        method: "GET",
        url: API_URL
    }).then(resp => resp.data);
}

const approvalAction = async (db, {set, id, s_id, s_iid}) => {
    // setting can be done two ways:
    // specify id directly
    const setApprovalOnId = db.prepare(`
        UPDATE status
            SET approval = @set
        WHERE id = @id
    `);
    // specify a source_id and a source_iid
    const setApprovalOnSource = db.prepare(`
        UPDATE status
        SET approval = @set
        WHERE id IN (
            SELECT id FROM level
            WHERE source_iid = @s_iid
            AND source_id = @s_id
        )
    `)
    if (id) {
        setApprovalOnId.run({set, id});
    } else {
        setApprovalOnSource.run({set, s_id, s_iid});
    }
}

const runAction = async (db, action, args) => {
    const router = {
        "approval" : approvalAction
    }
    try {
        await router[action](db, args);
    }
    catch (err) {
        console.log(err);
    }
}

const clearActions = async () => {
    return axios({
        method: "POST",
        url: API_URL,
        headers: {
            Authorization: `Token ${process.env.LODGE_TOKEN}`
        },
        data: []
    })
}

module.exports = {
    getActions,
    runAction,
    clearActions
}