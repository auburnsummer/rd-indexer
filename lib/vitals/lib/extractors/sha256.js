const { sha256 } = require('js-sha256');

module.exports = (rdlevel, zip, buffer) => ({
  sha256: sha256(buffer),
});
