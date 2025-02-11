// src/constants/apiEndpoints.ts

// Base API URL - defined in .env file
const BASE_API_URL = 'https://2d41-79-127-217-43.ngrok-free.app/api'
//const BASE_API_URL = 'http://127.0.0.1:5000/api';

// API Endpoint Definitions
export const API_ENDPOINTS = {
  // Base Endpoint
  INDEX: `${BASE_API_URL}/`,

  // Lobby Endpoints
  LOBBY: {
    BASE: `${BASE_API_URL}/lobby`,
    SESSIONS: `${BASE_API_URL}/lobby/sessions`,
    USERS: `${BASE_API_URL}/lobby/users`,
  },

  // Authentication Endpoints
  AUTH: {
    REGISTER: `${BASE_API_URL}/register`,
    LOGOUT: `${BASE_API_URL}/logout`,
  },
};

// Dynamic Endpoints (if any)
export const dynamicAPIEndpoints = {
  // Example: If you have endpoints that require parameters, define them as functions
  // For instance, fetching a specific session by ID
  GET_SESSION_BY_ID: (sessionId) => `${API_ENDPOINTS.LOBBY.SESSIONS}/${sessionId}`,
};
