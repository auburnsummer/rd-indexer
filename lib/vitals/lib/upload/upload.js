const b3 = require('blake3');
const { convertToBase58 } = require('../utils/b58');

const { b2 } = require('./b2_singleton');

const HASH_LENGTH = 16;

// upload a buffer. the filename is the base58 blake3 sum.
module.exports = async (buffer, extension, name) => {
  await b2.authorize();

  const bucketId = process.env.B2_BUCKET_ID;
  const hash = convertToBase58(b3.hash(buffer, { length: HASH_LENGTH }));
  const filename = name ? `${name}.${extension}` : `${hash}.${extension}`;
  // is it already uploaded?
  const resp3 = await b2.listFileNames({
    bucketId,
    startFileName: filename,
  });
  if (!name && resp3.files.length && resp3.files[0].fileName === filename) {
    // already uploaded.
    console.log('already has this hash, skipping upload...');
    return resp3.files[0];
  }
  // otherwise, we have to upload it...
  const resp = await b2.getUploadUrl(bucketId);
  const { uploadUrl, authorizationToken } = resp;

  const resp2 = await b2.uploadFile({
    uploadUrl,
    uploadAuthToken: authorizationToken,
    filename,
    data: buffer,
  });

  return resp2;
};
