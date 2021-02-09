const tap = require('tap');

const vitals = require('../lib/index.js')
const fs = require('fs');
const _ = require('lodash');
const Promise = require('bluebird');

const Ajv = require('ajv');

const readFile_p = Promise.promisify(fs.readFile);

/**
 * Given a JSON schema object, allow it to also pass if it's null.
 * @param {} schema 
 */
const nullable = (schema) => {
  return {
    "anyOf": [
      schema,
      {'type' : 'null'}
    ]
  }
}

/* json schema */
const schema = {
  '$id': 'http://rhythm.cafe/schemas/myschema.json',
  'type': 'object',
  'properties': {
    'sha256': {
      'type': 'string',
      'minLength': 44,
      'maxLength': 44,
    },
    'artist': {
      'type': 'string',
    },
    'song': {
      'type': 'string',
    },
    'difficulty': {
      'type': 'number',
      'multipleOf': 1.0,
    },
    'seizure_warning' : {
      'type': 'boolean',
    },
    'description' : {
      'type': 'string',
    },
    'max_bpm' : {
      'type': 'number',
      'minimum': 0,
    },
    'min_bpm' : {
      'type': 'number',
      'minimum': 0,
    },
    'last_updated': {
      'type': 'string',
      'format': 'date-time'
    },
    'single_player': {
      'type': 'boolean'
    },
    'two_player': {
      'type': 'boolean'
    },
    'image_ipfs': {
      'type': 'string'
    },
    'icon_ipfs': nullable({
      'type': 'string'
    }),
    'song_name_hue': {
      'type': 'number'
    },
    'rdzip_ipfs': {
      'type': 'string'
    },
    'has_classics': {
      'type': 'boolean'
    },
    'has_swing': {
      'type': 'boolean'
    },
    'has_freetimes': {
      'type': 'boolean'
    },
    'has_oneshots': {
      'type': 'boolean'
    },
    'has_squareshots': {
      'type': 'boolean'
    },
    'has_holds': {
      'type': 'boolean'
    }
  },
  'required' : ['sha256', 'artist', 'song', 'difficulty', 'seizure_warning', 'description', 'max_bpm',
                'min_bpm', 'last_updated', 'single_player', 'two_player', 'image_ipfs', 'icon_ipfs',
              'has_classics', 'has_swing', 'has_freetimes', 'has_oneshots', 'has_squareshots', 'has_holds']
}


const checkSchema = (result) => {
  const ajv = new Ajv();
  const valid = ajv.validate(schema, result);
  if (!valid) {
    console.error(ajv.errors);
  }
  return valid;
}


// const testRdzip = async (rdzipFilename, expected) => {
//   const readIn = await readFile_p(rdzipFilename);
//   const result = await vitals.analyse(readIn, "all");

//   // check the schema
//   const ajv = new Ajv();
//   const validate = ajv.validate(schema, result);
//   if (!validate) {
//     throw new Exception("Json schema failure.");
//   }

//   return _.isMatch(result, expected);
// }


tap.pass('this is fine');

tap.test('Know You aligns to schema', async childTest => {
  const buffer = await readFile_p("test/Andrew_Huang_-_Know_You.rdzip");
  const output = await vitals.analyse(buffer, "all");

  childTest.ok(checkSchema(output));
})

tap.test('Triplet thing aligns to schema', async childTest => {
  const buffer = await readFile_p("test/auburnsummer - triplet thing.rdzip");
  const output = await vitals.analyse(buffer, "all");

  childTest.ok(checkSchema(output));
})

tap.test('Jazz Candy aligns to schema', async childTest => {
  const buffer = await readFile_p("test/Nate_Harrell_-_Jazz_Candy_VIP.rdzip");
  const output = await vitals.analyse(buffer, "all");

  childTest.ok(checkSchema(output));
})


// tap.test('Correct header info from Know You', childTest => {
//   return testRdzip("test/Andrew_Huang_-_Know_You.rdzip", {
//     sha256: 'e86fbc334db27ebd59dbc472e38849c871715c787f5d11f30534a05522462340',
//     artist: 'Andrew Huang',
//     song: 'Know You',
//     difficulty: 1,
//     seizureWarning: false,
//     description: 'Two lonely stars\r, wandering in the dark...',
//     maxBPM: 78.5,
//     minBPM: 78.5,
//     tags: [ 'slow', 'pop', '1p' ],
//     authors: [ 'lugi' ],
//     singlePlayer: true,
//     twoPlayer: false
//   })
//   .then( (result) => {
//     console.log(result);
//     childTest.ok(result);
//   });
// })