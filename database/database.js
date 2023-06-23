const pgp = require('pg-promise')();
require('dotenv').config();


const cn = {
  host: 'localhost',
  port: 5432,
  database: 'issue_tracker_db',
  user: 'issue_tracker_user',
  password: process.env.DB_PASSWORD
};

const db = pgp(cn);

db.connect()
  .then(obj => {
    obj.done(); // success, release the connection
  })
  .catch(error => {
    console.log('ERROR:', error.message);
  });

module.exports = db;