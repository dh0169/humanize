"use client"

import React, { useState } from "react";
// Adjust the import path to your actual file location:
import { API_ENDPOINTS } from "@/constants/apiEndpoints";

// 1. Import the SyntaxHighlighter components/styles you like:
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

import { useRouter } from 'next/navigation';

function Debugger() {
  const router = useRouter();
  const isDeveloper = () => {
    // Only developers with this "secret" key can access
    return localStorage.getItem("devSecret") === "letMeIn";
  };

  if(!isDeveloper()) {
    router.push("/");
  }

  const [username, setUsername] = useState("");
  const [room, setRoom] = useState("");
  const [log, setLog] = useState<string[]>([]);

  // Helper to append messages to our debug log
  const addLog = (message: string) => {
    setLog((prev) => [...prev, message]);
  };

  const handleRegister = async () => {
    const bodyData = { username };
    try {
      const res = await fetch(API_ENDPOINTS.AUTH.REGISTER, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(bodyData),
        credentials: "include",
      });
      const data = await res.json();
      addLog(`
POST /register
Request Body:
${JSON.stringify(bodyData, null, 2)}

Response:
${JSON.stringify(data, null, 2)}
`);
    } catch (error) {
      addLog(`
POST /register
Request Body:
${JSON.stringify(bodyData, null, 2)}

Error:
${(error as Error).message}
`);
    }
  };

  const handleLobbyGet = async () => {
    try {
      const res = await fetch(API_ENDPOINTS.LOBBY.BASE, {
        credentials: "include",
      });
      const data = await res.json();
      addLog(`
GET /lobby
(No body sent)

Response:
${JSON.stringify(data, null, 2)}
`);
    } catch (error) {
      addLog(`
GET /lobby
(No body sent)

Error:
${(error as Error).message}
`);
    }
  };

  const handleHostSession = async () => {
    const bodyData = { type: "host", room: room.trim() };
    try {
      const res = await fetch(API_ENDPOINTS.LOBBY.BASE, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(bodyData),
        credentials: "include",
      });
      const data = await res.json();
      addLog(`
POST /lobby (host)
Request Body:
${JSON.stringify(bodyData, null, 2)}

Response:
${JSON.stringify(data, null, 2)}
`);
    } catch (error) {
      addLog(`
POST /lobby (host)
Request Body:
${JSON.stringify(bodyData, null, 2)}

Error:
${(error as Error).message}
`);
    }
  };

  const handleJoinSession = async (random = false) => {
    const bodyData = {
      type: "join",
      room: room.trim(),
      random,
    };
    try {
      const res = await fetch(API_ENDPOINTS.LOBBY.BASE, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(bodyData),
        credentials: "include",
      });
      const data = await res.json();
      addLog(`
POST /lobby (join)
Request Body:
${JSON.stringify(bodyData, null, 2)}

Response:
${JSON.stringify(data, null, 2)}
`);
    } catch (error) {
      addLog(`
POST /lobby (join)
Request Body:
${JSON.stringify(bodyData, null, 2)}

Error:
${(error as Error).message}
`);
    }
  };

  const handleListSessions = async () => {
    try {
      const res = await fetch(API_ENDPOINTS.LOBBY.SESSIONS, {
        credentials: "include",
      });
      const data = await res.json();
      addLog(`
GET /lobby/sessions
(No body sent)

Response:
${JSON.stringify(data, null, 2)}
`);
    } catch (error) {
      addLog(`
GET /lobby/sessions
(No body sent)

Error:
${(error as Error).message}
`);
    }
  };

  const handleListUsers = async () => {
    try {
      const res = await fetch(API_ENDPOINTS.LOBBY.USERS, {
        credentials: "include",
      });
      const data = await res.json();
      addLog(`
GET /lobby/users
(No body sent)

Response:
${JSON.stringify(data, null, 2)}
`);
    } catch (error) {
      addLog(`
GET /lobby/users
(No body sent)

Error:
${(error as Error).message}
`);
    }
  };

  const handleLogout = async () => {
    try {
      const res = await fetch(API_ENDPOINTS.AUTH.LOGOUT, {
        credentials: "include",
      });
      const data = await res.json();
      addLog(`
GET /logout
(No body sent)

Response:
${JSON.stringify(data, null, 2)}
`);
    } catch (error) {
      addLog(`
GET /logout
(No body sent)

Error:
${(error as Error).message}
`);
    }
  };

  return (
    <div
      style={{
        backgroundColor: "#121212",
        color: "#ffffff",
        minHeight: "100vh",
        padding: "1rem",
        fontFamily: "sans-serif",
      }}
    >
      <h2 style={{ marginBottom: "1rem", color: "#44c4a1" }}>
        Simple Chat API Debugger
      </h2>

      {/* Registration */}
      <div style={{ marginBottom: "1rem" }}>
        <label style={{ marginRight: "0.5rem" }}>Username:</label>
        <input
          style={{
            marginRight: "1rem",
            backgroundColor: "#2c2c2c",
            color: "#fff",
            border: "1px solid #555",
            padding: "0.25rem",
          }}
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter a username"
        />
        <button
          onClick={handleRegister}
          style={{
            backgroundColor: "#44c4a1",
            color: "#121212",
            border: "none",
            padding: "0.5rem 1rem",
            cursor: "pointer",
          }}
        >
          POST /register
        </button>
      </div>

      {/* Lobby (GET) */}
      <div style={{ marginBottom: "1rem" }}>
        <button
          onClick={handleLobbyGet}
          style={{
            backgroundColor: "#44c4a1",
            color: "#121212",
            border: "none",
            padding: "0.5rem 1rem",
            cursor: "pointer",
            marginRight: "1rem",
          }}
        >
          GET /lobby
        </button>
      </div>

      {/* Host/Join */}
      <div style={{ marginBottom: "1rem" }}>
        <label style={{ marginRight: "0.5rem" }}>Room:</label>
        <input
          style={{
            marginRight: "1rem",
            backgroundColor: "#2c2c2c",
            color: "#fff",
            border: "1px solid #555",
            padding: "0.25rem",
          }}
          value={room}
          onChange={(e) => setRoom(e.target.value)}
          placeholder="Enter a room name"
        />
        <button
          onClick={handleHostSession}
          style={{
            backgroundColor: "#44c4a1",
            color: "#121212",
            border: "none",
            padding: "0.5rem 1rem",
            cursor: "pointer",
            marginRight: "0.5rem",
          }}
        >
          POST /lobby (Host)
        </button>
        <button
          onClick={() => handleJoinSession(false)}
          style={{
            backgroundColor: "#44c4a1",
            color: "#121212",
            border: "none",
            padding: "0.5rem 1rem",
            cursor: "pointer",
            marginRight: "0.5rem",
          }}
        >
          POST /lobby (Join Custom)
        </button>
        <button
          onClick={() => handleJoinSession(true)}
          style={{
            backgroundColor: "#44c4a1",
            color: "#121212",
            border: "none",
            padding: "0.5rem 1rem",
            cursor: "pointer",
          }}
        >
          POST /lobby (Join Random)
        </button>
      </div>

      {/* List Sessions/Users */}
      <div style={{ marginBottom: "1rem" }}>
        <button
          onClick={handleListSessions}
          style={{
            backgroundColor: "#44c4a1",
            color: "#121212",
            border: "none",
            padding: "0.5rem 1rem",
            cursor: "pointer",
            marginRight: "0.5rem",
          }}
        >
          GET /lobby/sessions
        </button>
        <button
          onClick={handleListUsers}
          style={{
            backgroundColor: "#44c4a1",
            color: "#121212",
            border: "none",
            padding: "0.5rem 1rem",
            cursor: "pointer",
          }}
        >
          GET /lobby/users
        </button>
      </div>

      {/* Logout */}
      <div style={{ marginBottom: "1rem" }}>
        <button
          onClick={handleLogout}
          style={{
            backgroundColor: "#44c4a1",
            color: "#121212",
            border: "none",
            padding: "0.5rem 1rem",
            cursor: "pointer",
          }}
        >
          GET /logout
        </button>
      </div>

      {/* Debug Log */}
      <h3 style={{ marginTop: "2rem", marginBottom: "0.5rem" }}>Debug Log</h3>
      <div
        style={{
          backgroundColor: "#2c2c2c",
          border: "1px solid #555",
          padding: "1rem",
          minHeight: "300px",
          width: "100%",
          boxSizing: "border-box",
        }}
      >
        {log.length === 0 && (
          <div style={{ color: "#aaa" }}>No logs yet...</div>
        )}
        {log.map((entry, index) => (
          <SyntaxHighlighter
            key={index}
            language="json"
            style={vscDarkPlus}
            wrapLines={true}
            showLineNumbers={true}
          >
            {entry}
          </SyntaxHighlighter>
        ))}
      </div>
    </div>
  );
}

export default Debugger;