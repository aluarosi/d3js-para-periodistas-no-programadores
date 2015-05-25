var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

var routes = require('../applib/webserver/routes/index');
var users = require('../applib/webserver/routes/users');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, '/webserver/views'));
app.set('view engine', 'ejs');

//app.use(favicon(path.join(__dirname, '../appvar/webserver/public/img/favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded());
app.use(cookieParser());
var CACHE_TIME_HOURS = 0; // Cache time in hours
app.use(express.static(path.join(__dirname, '../appvar/webserver/public'),
  {maxAge: 1000 * 60 * 60 * CACHE_TIME_HOURS} ));

app.use('/', routes);
app.use('/users', users);

/// catch 404 and forward to error handler
app.use(function(req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

/// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function(err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});


module.exports = app;

