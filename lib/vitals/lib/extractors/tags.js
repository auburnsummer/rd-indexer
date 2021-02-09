const {
  pipe, split, map, trim, filter, identity,
} = require('lodash/fp');

module.exports = (rdlevel) => {
  const tags = pipe(
    split(','),
    map(trim),
    filter(identity),
  )(rdlevel.settings.tags);

  return {
    tags,
  };
};
