var express = require('express');
var router = express.Router();
var busboy = require('connect-busboy');
var VError = require('verror');
var util = require('util');
var async = require('async');
var log = require('../../../applib/log');


// Middleware
//router.use(busboy());

/* GET home page. */
router.get('/', function(req, res) {
  res.render('index', { title: 'Twittocracy' });
});

module.exports = router;
