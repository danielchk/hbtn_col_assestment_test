const express = require('express');
const morgan = require('morgan');
const exphbs = require('express-handlebars');
const path = require('path'); //Join directories

//start
const app = express()

//config
app.set('port', process.env.PORT || 4000);
app.set('views', path.join(__dirname, 'views'));   //directions views
app.engine('.hbs', exphbs({
    defaultLayout : 'main',
    layoutsDir: path.join(app.get('views'), 'layouts'),
    partialsDir : path.join(app.get('views'), 'partials'),
    extname: '.hbs',            //change extension in views
    helpers: require('./lib/handlebars')  //usage of reuses
}));

app.set('view engine', '.hbs'); //engine handlebars working

//middleware
app.use(morgan('dev'));   //message to console to know what is going to server
app.use(express.urlencoded({extended: false}));  //accept formulario but not everything
app.use(express.json());  //tradoing json

//variables

//routes
app.use(require('./routes'));
//public

//server start
app.listen(app.get('port'), () => {
    console.log('Server on port', app.get('port'));
})