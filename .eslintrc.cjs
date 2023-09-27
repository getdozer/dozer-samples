/* eslint-env node */
module.exports = {
  extends: ['eslint:recommended', 'plugin:@typescript-eslint/recommended'],
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  root: true,
  settings: {
    "import/resolver": {
      typescript: {} // this loads <rootdir>/tsconfig.json to eslint
    },
  },
};