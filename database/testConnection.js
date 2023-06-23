const db = require('./database');

db.any('SELECT 1')
  .then(() => console.log('Database connection successful'))
  .catch(err => console.error('Database connection error', err));