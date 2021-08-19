//connection to my database

const mysql = require('mysql');
const { promisify } = require('util');  //callbacks to promises

const { database } = require('./keys');

const pool = mysql.createPool(database);  //like createConnection but less exigent to errors(Connection)

pool.getConnection((err, connection) => {   //connection config to pool
    if (err) {
        if (err.code === 'PROTOCOL_CONNECTION_LOST') {
            console.error('DATABASE CONNECTION CLOSED')
        }
        if (err.code === 'ER_CON_COUNT_ERROR'){
            console.error('DATABASE HAS TOO MANY CONNECTIONS');
        }
        if (err.code === 'ECONNREFUSED') {
            console.error('DATABASE CONNECTION WAS REFUSED');
        }
    }
    if (connection) connection.release();
    console.log('DB is connected');
    return;
});

pool.query = promisify(pool.query);

module.exports = pool;