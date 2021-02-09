/*
Get things like
donte, ladybug
donte & ladybug
donte and ladybug
donte, noche, and ladybug
donte, noche, & ladybug
*/
const AUTHOR_REGEX = /\s*?(?:,|&|\/|\\|,? ,?and )\s*?/;
const {
  map, split, trim, pipe,
} = require('lodash/fp');

module.exports = (rdlevel) => ({
  authors: pipe(
    split(AUTHOR_REGEX),
    map(trim),
  )(rdlevel.settings.author),
});
