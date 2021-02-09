/**
 * Generate an id based off the hashes of the files.
 *
 * The idea here is two archives that might be zipped differently still generate
 * the same id as long as the internal files are the same.
 */
const HASH_LENGTH = 16;

const b3 = require('blake3');
const _ = require('lodash');

const { convertToBase58 } = require('../utils/b58');

module.exports = async (rdlevel, zip) => {
  // filename + blake5 hash pair for each file
  const promises = [];

  zip.forEach((relativePath, file) => {
    if (!file.dir) {
      // push a IIFE
      promises.push((async (f) => {
        const buf = await f.async('nodebuffer');
        const hash = b3.hash(buf, { length: HASH_LENGTH }).toString('base64');
        return `${f.name}.${hash}`;
      })(file));
    }
  });
  let tokens = await Promise.all(promises);
  // sort the file + hash pairs
  tokens = _.sortBy(tokens);
  const finalHashBuf = b3.hash(_.join(tokens, ''), { length: HASH_LENGTH });
  return {
    id: convertToBase58(finalHashBuf),
  };
};
