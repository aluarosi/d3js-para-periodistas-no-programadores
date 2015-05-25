/*
    Auxiliar/utilities
 */

/*
    EXPORT
 */
var $ = {};
module.exports = $;

/*
    IMPORT
 */
os = require('os');

// Check if we are in a DEVELOPMENT ENVIRONMENT
$.is_dev_environ = function is_dev_environ(){
  // Check a Heroku specific env var to determine
  //    if we are running on Heroku
  is_dev = process.env.DYNO === undefined;
  return is_dev;
};


