const upload = require('../upload/upload');

/**
 * Upload the image to our hosting. Give a URL.
 *
 * No messing around with IPFS that kinda sucked tbh
 */
module.exports = async (rdlevel, zip) => {
  try {
    const imageName = rdlevel.settings.previewImage;
    const imageBuffer = await zip.file(imageName).async('nodebuffer');
    const info = await upload(imageBuffer, 'png');
    return {
      thumb: process.env.HOSTED_FILES_PREFIX + info.fileName,
    };
  } catch (e) {
    // if we couldn't upload, don't add a parameter.
    console.log(e);
    return {icon: null};
  }
};
