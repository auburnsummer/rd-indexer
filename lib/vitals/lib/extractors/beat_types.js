/*
Does a level contain:

 - classics
 - swung beats
 - oneshots
 - squareshots
 - freetimes
 - holds (assuming holds are a thing)

*/

const { some, curry, isUndefined } = require('lodash');

const zeroOrUndefined = (x) => (x === 0) || isUndefined(x);

module.exports = (rdlevel) => {
  // return True if any event meets a predicate.
  const anyEvent = curry(some, 2)(rdlevel.events);

  const classics = anyEvent((evt) => evt.type === 'AddClassicBeat' && evt.swing === 0 && zeroOrUndefined(evt.holds));
  const swing = anyEvent((evt) => evt.type === 'AddClassicBeat' && evt.swing !== 0 && zeroOrUndefined(evt.holds));
  const holds = anyEvent((evt) => evt.type === 'AddClassicBeat' && evt.hold !== 0);
  const freetimes = anyEvent((evt) => evt.type === 'AddFreeTimeBeat');
  const oneshots = anyEvent((evt) => evt.type === 'AddOneshotBeat' && evt.pulseType === 'Wave');
  const squareshots = anyEvent((evt) => evt.type === 'AddOneshotBeat' && evt.pulseType === 'Square');
  return {
    has_classics: classics,
    has_swing: swing,
    has_holds: holds,
    has_freetimes: freetimes,
    has_oneshots: oneshots,
    has_squareshots: squareshots,
  };
};
