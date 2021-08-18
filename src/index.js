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
    layoutsDir: path.join(app.get('views'), 'layouts'),     //search for layouts in views
    partialsDir : path.join(app.get('views'), 'partials'),  //reuse parts of code
    extname: '.hbs',            //change extension in views
    helpers: require('./lib/handlebars')  //usage of functions in handlebars
}));

app.set('view engine', '.hbs'); //engine handlebars working

//middleware

app.use(morgan('dev'));   //message to console to know what is going to server
app.use(express.urlencoded({extended: false}));  //accept only strings
app.use(express.json());  //accept json too

//Golbal variables

app.use((req, res, next) => {  //Requirement, Response

    next();   //Take info, requirement and the respond function
})

//routes

app.use(require('./routes'));
app.use(require('./routes/authentication'));
app.use(require('./routes/links'));

//public

app.use(express.static(path.join(__dirname, 'public')));

//server start
app.listen(app.get('port'), () => {
    console.log('Server on port', app.get('port'));
})