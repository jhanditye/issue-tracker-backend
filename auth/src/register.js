const bcrypt = require('bcrypt');
const db = require('./database');
const jwt = require('jsonwebtoken');
require('dotenv').config()
const jwtSecretKey = process.env.JWT_SECRET_KEY;
let users = {}; // emulate database

module.exports.handler = async (event, context) => {
  const requestBody = JSON.parse(event.body);
  const { username, password } = requestBody;

  // Check if user exists in the database
  const user = await db.one('SELECT * FROM users WHERE username = $1', [username]);
  if (!user) {
    return {
      statusCode: 401,
      body: JSON.stringify({
        message: 'Username or password is incorrect.',
      }),
    };
  }

  // Verify password with bcrypt.compare()
  const passwordIsValid = await bcrypt.compare(password, user.password);
  if (!passwordIsValid) {
    return {
      statusCode: 401,
      body: JSON.stringify({
        message: 'Username or password is incorrect.',
      }),
    };
  }

  // If user exists and password matches, create and return a JWT
  const token = jwt.sign({ username }, jwtSecretKey, { expiresIn: '24h' });

  return {
    statusCode: 200,
    body: JSON.stringify({
      message: 'User login successful',
      token,
    }),
  };
};
