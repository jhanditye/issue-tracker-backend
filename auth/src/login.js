const bcrypt = require('bcrypt');
require('dotenv').config()
const secretKey = process.env.SECRET_KEY;
let users = {}; // emulate database

module.exports.handler = async (event, context) => {
  const requestBody = JSON.parse(event.body);
  const { username, password } = requestBody;

  // TODO: Check if user already exists
  if (users[username]) {
    return {
      statusCode: 400,
      body: JSON.stringify({
        message: 'Username already exists.',
      }),
    };
  }

  // TODO: Hash password
  const hashedPassword = await bcrypt.hash(password, 10);

  // TODO: Store user in the database
  users[username] = {
    password: hashedPassword,
  };

  return {
    statusCode: 200,
    body: JSON.stringify({
      message: 'User registration successful',
    }),
  };
};