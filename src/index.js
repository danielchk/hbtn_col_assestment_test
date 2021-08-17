const express = require('express');
const morgan = require('morgan');
//start
const app = express()

//config
app.set('port', process.env.PORT || 4000);

//middleware
app.use(morgan('dev'));   //message to console to know what is going to server

//variables

//routes

//public

//server start
app.listen(app.get('port'), () => {
    console.log('Server on port', app.get('port'));
})