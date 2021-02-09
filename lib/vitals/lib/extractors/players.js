module.exports = (rdlevel) => ({
  single_player: ['OnePlayerOnly', 'BothModes'].includes(rdlevel.settings.canBePlayedOn),
  two_player: ['TwoPlayerOnly', 'BothModes'].includes(rdlevel.settings.canBePlayedOn),
});
