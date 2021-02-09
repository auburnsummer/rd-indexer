const upload = require('../upload/upload');

/**
 * Upload the level to our hosting. Give a URL.
 *
 * No messing around with IPFS that kinda sucked tbh
 */
module.exports = async (rdlevel, zip, buffer) => {
  try {
    const info = await upload(buffer, 'rdzip');
    return {
      url: process.env.HOSTED_FILES_PREFIX + info.fileName,
    };
  } catch (e) {
    // if we couldn't upload, don't add a URL parameter.
    console.log(e);
    return {url: null};
  }
};
