const jszip = require('jszip');
const RDLevel = require('./rdlevel/index.js');
const extract = require('./extract.js');

require('dotenv').config();

/**
 * Analyse an rdzip file.
 *
 * @param buffer: A Buffer object which is the loaded rdzip file
 */
module.exports = async (buffer) => {
  // unzip it.
  let zip;
  let rdlevelRaw;
  try {
    // load the contents of the .rdlevel. The rdlevel is always called main.rdlevel
    zip = await jszip.loadAsync(buffer);
    const rdlevelFile = zip.file('main.rdlevel');
    rdlevelRaw = await rdlevelFile.async('string');
  } catch (err) {
    console.log(err);
    return Promise.reject(new Error(`Zip error. Is this an rdzip? | ${err}`));
  }

  let rdlevel;
  try {
    // parse it with the RDlevel parser (modified JSON5)
    rdlevel = RDLevel.parse(rdlevelRaw);
  } catch (err) {
    console.log(err);
    return Promise.reject(new Error(`Error parsing the main.rdlevel | ${err}`));
  }
  // Finally start extracting things.
  return extract(rdlevel, zip, buffer);
};
