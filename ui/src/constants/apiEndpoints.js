// src/constants/apiEndpoints.ts

// const BASE_API_URL = 'https://humanize.live/api'
//const BASE_API_URL = 'http://127.0.0.1:8080/api';
const BASE_API_URL = '/api'

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

// Helper function to fetch and return data.content
const fetchData = async (url) => {
  try {
    const res = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    });
    if (res.ok) {
      const data = await res.json();
      return data.content;
    }
    return null;
  } catch (error) {
    console.error(error);
    console.log("Network error. Please try again later.");
    return null;
  }
};

// Helper function to send data and return data.content
const sendData = async (url, data, method = "POST") => {
  try {
    const res = await fetch(url, {
      method: method, // Allow different HTTP methods
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(data), // Convert data to JSON
    });

    if (res.ok) {
      const responseData = await res.json();
      return responseData.content;
    }
    return null;
  } catch (error) {
    console.error(error);
    console.log("Network error. Please try again later.");
    return null;
  }
};


export const checkLogin = () => fetchData(API_ENDPOINTS.LOBBY.BASE);
export const getSessions = () => fetchData(API_ENDPOINTS.LOBBY.SESSIONS);
export const getSessionByID = (id) => fetchData(dynamicAPIEndpoints.GET_SESSION_BY_ID(id));
