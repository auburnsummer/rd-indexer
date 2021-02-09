module.exports = async (rdlevel, zip) => {
  const rdlevelFile = await zip.file('main.rdlevel');
  return {
    last_updated: rdlevelFile.date.getTime() / 1000
  };
};
