/* uh */

require('dotenv').config();

const minimist = require('minimist');
const pkg = require('../package.json');
const {doIndex, doUpload} = require('.');

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
    const inFileName = argv._[0];
    const srcFileName = argv._[1];
    doIndex(inFileName, srcFileName);
}
  