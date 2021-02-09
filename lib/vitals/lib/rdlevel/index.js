const parse5 = require('./parse')
const stringify = require('./stringify')

const parse = (text, reviver) => {
    try {
        return JSON.parse(text, reviver)
    } catch (e) {
        return parse5(text, reviver)
    }
}

const RDLevel = {
    parse,
    stringify,
}

module.exports = RDLevel
