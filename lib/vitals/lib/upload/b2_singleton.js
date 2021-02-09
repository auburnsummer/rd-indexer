const B2 = require('backblaze-b2');

const b2 = new B2({
  accountId: process.env.B2_KEY_ID,
  applicationKey: process.env.B2_APPLICATION_KEY,
});

module.exports = {
  b2,
};
