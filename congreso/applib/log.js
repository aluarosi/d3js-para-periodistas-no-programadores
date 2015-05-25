/*
    LOGger (wrapper on bunyan)
 */

/**
    CONFIG
 */
var APP_NAME = 'congreso';
var LOG_LEVEL = "debug";

/**
    IMPORT
 */
var bunyan = require('bunyan');

/**
    MAIN
 */
var $ = bunyan.createLogger({
  name: APP_NAME,
  level: LOG_LEVEL
});

/**
    EXPORT
 */
module.exports = $;


