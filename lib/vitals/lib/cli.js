#!/usr/bin/env node

require('dotenv').config();

const fs = require('fs');
const minimist = require('minimist');
const pkg = require('../package.json');
const vitals = require('.');

/*
vitals just takes a single argument - the name of the file.

it's otherwise configured through environment variables.
*/
const argv = minimist(process.argv.slice(2), {
  alias: {
    version: 'V',
  },
});

function version() {
  console.log(pkg.version);
}

if (argv.version) {
  version();
} else {
  const inFileName = argv._[0];

  let readIn;

  if (inFileName) {
    readIn = fs.readFileSync(inFileName);
  } else {
    console.error('A file is required!');
    process.exit(1);
  }

  vitals.analyse(readIn)
    .then(console.log);
}
