const {
  filter, includes, map, max, min, pipe,
} = require('lodash/fp');

module.exports = (rdlevel) => {
  const isBpmEvent = (evt) => includes(evt.type, ['PlaySong', 'SetBeatsPerMinute']);

  const bpms = pipe(
    // first, filter for just the BPM events.
    filter(isBpmEvent),
    // then, the bpm is either in the .bpm or .beatsPerMinute key
    map((evt) => evt.bpm || evt.beatsPerMinute),
  )(rdlevel.events);

  return {
    max_bpm: max(bpms) || 0,
    min_bpm: min(bpms) || 0,
  };
};
