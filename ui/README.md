# Front-end Stack

This project was created using
  - React 19
  - Typescript 5.7.3
  - NextJS 15.1.7

## Available Scripts

In the project directory, you can run:

### `npm run dev`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm run test`

Testing implementation WIP;

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

### `npm run start`

Simulates a production hosting environment and a production build of the project.

## Learn More

You can learn more in the [NextJS documentation](https://nextjs.org/docs).

To learn React, check out the [React documentation](https://reactjs.org/).

To learn Typescript, check out the [TypeScript documentation](https://www.typescriptlang.org/docs/).

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
   npm run dev
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
    ├── app/             # Describes the routes from NextJS
    │   ├── layout.tsx   # Initializes the root
    │   ├── page.tsx     # Actual layout of the page; occurs in every folder
    │   └── ...
    ├── components/    # Reusable components
    └── ...            # Other files (libraries, tests, etc.)
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

