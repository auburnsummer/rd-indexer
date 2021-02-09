# vitals


[![Build Status](https://cloud.drone.io/api/badges/auburnsummer/vitals/status.svg)](https://cloud.drone.io/auburnsummer/vitals) [![](https://img.shields.io/github/license/auburnsummer/vitals?color=e597d5)](LICENCE) [![](https://img.shields.io/npm/v/@auburnsummer/vitals)](https://www.npmjs.com/package/@auburnsummer/vitals)

vitals takes an .rdzip file from Rhythm Doctor and produces a JSON object
of the important metadata from it.

```
> npx @auburnsummer/vitals Andrew_Huang_-_Know_You.rdzip
{
  sha256: 'e86fbc334db27ebd59dbc472e38849c871715c787f5d11f30534a05522462340',
  artist: 'Andrew Huang',
  song: 'Know You',
  difficulty: 1,
  seizureWarning: false,
  description: 'Two lonely stars\r, wandering in the dark...',
  maxBPM: 78.5,
  minBPM: 78.5,
  tags: [ 'slow', 'pop', '1p' ],
  lastUpdated: 2019-08-31T21:13:26.000Z,
  authors: [ 'lugi' ],
  singlePlayer: true,
  twoPlayer: false,
  songNameHue: 0.47
}
```

You can also use it in a script:

```
const vitals = require('@auburnsummer/vitals')
some_function_that_downloads_an_rdzip()
.then( (buffer) => {
  console.log(vitals.analyse(buffer))
})
```

# Contributing

Hi, thanks for being interested in contributing!

This is eventually going to be part of a larger project called Orchard, which is meant for
providing a more consistent experience for Rhythm Doctor custom levels. When I get that set up,
I'll have a proper code of conduct and contributing documents, etc, etc.

In the meantime, you can look at [lib/extract.js](lib/extract.js) for the list of currently implemented extractors.
You can get vitals to pull out more things by adding more extractor functions.