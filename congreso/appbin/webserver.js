#!/usr/bin/env node
//require('newrelic');
/**
 */

/*
  IMPORT
 */
var IS_DEV = require("../applib/aux").is_dev_environ();
var net_config = require("../appetc/net.conf");

/*
  CONFIG
 */


/*
  Start WEBSERVER 
 */
var debug = require('debug')('twittocracy');
var app = require('../applib/webserver');

app.set('port', net_config.PORT);

var server = app.listen(app.get('port'), function() {
  debug('Express server listening on port ' + server.address().port);
});
