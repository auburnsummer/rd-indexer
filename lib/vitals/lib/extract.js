/**
 * Mapping of strings to functions that extract things out
 */

const { map, reduce, merge } = require('lodash/fp');
const { get } = require('lodash');

/*
By the way, what's an extractor function? It's basically any function that meets
the signature (rdlevel, zip, buffer) => (a json object).

rdlevel is a json object parsed using the RDLevel library. Probably most extractors will
only use this one.

zip is a jszip object of the .rdzip file. You can use this if your extractor needs
to reach outside of the rdlevel (e.g. looking at images or doing analysis of the song)

buffer is the raw binary representation of the .rdzip file. this is used for the
ipfs uploader and the sha256 hash extractors currently.
*/

/**
 * Generate an extractor function which gets out a key and puts it under the name
 * or gives it a default value if the key does not exist
 */
const simpleKeyExtractor = (name, key, def) => (rdlevel) => ({
  [name]: get(rdlevel, key, def),
});

/**
 * List of extractor functions we support.
 *
 * For simpler ones, feel free to either use simpleKeyExtractor or
 * inline an anonymous function. Otherwise, you should make it a seperate file.
 */
/* eslint-disable */
const extractors = [
  require('./extractors/id.js'),
  simpleKeyExtractor('artist', 'settings.artist'),
  simpleKeyExtractor('song', 'settings.song'),
  require('./extractors/difficulty.js'),
  simpleKeyExtractor('seizure_warning', 'settings.seizureWarning', false),
  simpleKeyExtractor('description', 'settings.description', ''),
  require('./extractors/bpm.js'),
  require('./extractors/tags.js'),
  require('./extractors/last_updated.js'),
  require('./extractors/authors.js'),
  simpleKeyExtractor('hue', 'settings.songNameHue'),
  require('./extractors/beat_types.js'),
  require('./extractors/players.js'),
  require('./extractors/b2_rehost.js'),
  require('./extractors/image_rehost'),
  require('./extractors/icon_rehost'),
];
/* eslint-enable */

module.exports = async (rdlevel, zip, buffer) => {
  const results = await Promise.all(map((f) => f(rdlevel, zip, buffer), extractors));
  return reduce(merge, {}, results);
};
