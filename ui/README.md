# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

## Setup

1. **Install dependencies** (in your React project root):
   ```bash
   npm install
   ```
2. **Install syntax highlighting library**:
   ```bash
   npm install react-syntax-highlighter
   ```
3. **Run the development server**:
   ```bash
   npm start
   ```
4. Make sure your **Flask backend** is running on the URL defined by [`API_ENDPOINTS`](#api-endpoints) or configure a proxy in `package.json` to forward API requests if necessary.

## File Structure

```
ui
├── README.md           # Project documentation (this file)
├── package.json        # Dependencies, scripts, etc.
├── public/             # Static files (index.html, etc.)
└── src/
    ├── constants/      
    │   └── apiEndpoints.js   # Central place for API endpoint URLs
    ├── App.js         # Main React Debugger page
    ├── index.js       # Entry point that renders <App /> 
    └── ...            # Other files (styling, tests, etc.)
```

### `apiEndpoints.ts`
- Stores all the endpoint URLs to communicate with your Flask server.  
- Example:
  ```ts
  const BASE_API_URL = 'http://127.0.0.1:5000/api';

  export const API_ENDPOINTS = {
    LOBBY: {
      BASE: `${BASE_API_URL}/lobby`,
      SESSIONS: `${BASE_API_URL}/lobby/sessions`,
      USERS: `${BASE_API_URL}/lobby/users`,
    },
    AUTH: {
      REGISTER: `${BASE_API_URL}/register`,
      LOGOUT: `${BASE_API_URL}/logout`,
    }
  };
  ```
- Adjust `BASE_API_URL` as needed for your setup.

