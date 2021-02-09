const { indexOf } = require('lodash');

const DIFFICULTIES = ['Easy', 'Medium', 'Tough', 'VeryTough'];
const defaultDifficulty = 1; // Medium

module.exports = (rdlevel) => {
  let difficultyIndex = indexOf(DIFFICULTIES, rdlevel.settings.difficulty);
  if (difficultyIndex === -1) {
    difficultyIndex = defaultDifficulty;
  }
  return {
    difficulty: difficultyIndex,
  };
};
