const _ = require('lodash');
const upload = require('../upload/upload');

module.exports = async (rdlevel, zip) => {
  const imageName = rdlevel.settings.syringeIcon;
  if (_.isEmpty(imageName)) {
    // no syringe icon
    return {icon: null};
  }

  try {
    const imageBuffer = await zip.file(imageName).async('nodebuffer');
    const info = await upload(imageBuffer, 'png');
    return {
      icon: process.env.HOSTED_FILES_PREFIX + info.fileName,
    };
  } catch (err) {
    console.log(err);
    return {icon: null};
  }
};
