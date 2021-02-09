const bx = require('base-x');

const BASE58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';

const convertToBase58 = (buf) => bx(BASE58).encode(buf);

module.exports = {
  convertToBase58,
};
