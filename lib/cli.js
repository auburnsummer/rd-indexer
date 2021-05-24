require('dotenv').config();

const minimist = require('minimist');
const pkg = require('../package.json');
const {doIndex} = require('.');

const {doMerge} = require("./merge.js");

function version() {
    console.log(pkg.version);
}

const argv = minimist(process.argv.slice(2), {
    alias: {
      version: 'V',
    },
});
  
if (argv.version) {
    version();
} else {
    if (argv._[0] === "merge") {
        const dbA = argv._[1];
        const dbB = argv._[2];
        doMerge(dbA, dbB);
    } else {
        const inFileName = argv._[0];
        const srcFileName = argv._[1];
        doIndex(inFileName, srcFileName);
    }
}
  