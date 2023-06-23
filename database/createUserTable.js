const db = require('./database');

const recreateUsersTable = async () => {
  // Drop the existing 'users' table
  await db.none('DROP TABLE IF EXISTS users;');
  
  // Create the new 'users' table
  await db.none(`
    CREATE TABLE users (
      id SERIAL PRIMARY KEY,
      username VARCHAR(50) UNIQUE NOT NULL,
      password VARCHAR(255) NOT NULL,
      email VARCHAR(255) UNIQUE NOT NULL
    );
  `);
};

recreateUsersTable()
  .then(() => console.log("Users table recreated successfully."))
  .catch(error => console.log("Failed to recreate users table:", error));