import React, { useState } from "react";
import { API_ENDPOINTS } from "../constants/apiEndpoints"; // Adjust the path as needed
import { useNavigate } from "react-router";

const Registration = () => {
  const [username, setUsername] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleRegister = async () => {
    if (username.trim() === "") {
      setError("Username cannot be empty");
      return;
    }
    setError(""); // Clear any previous errors

    const bodyData = { username };
    try {
      const res = await fetch(API_ENDPOINTS.AUTH.REGISTER, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(bodyData),
        credentials: "include",
      });
      const data = await res.json();

      if (res.ok) {
        // If registration is successful, navigate to homepage
        navigate("/home");
      } else {
        setError(data.message || "Registration failed");
      }
    } catch (error) {
      setError("Network error. Please try again later.");
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        backgroundColor: "#f0f2f5",
      }}
    >
      <img
        src="/humanize_logo.png"
        alt="Logo"
        style={{ width: "150px", marginBottom: "2rem" }}
      />
      <div
        style={{
          backgroundColor: "#fff",
          padding: "2rem",
          borderRadius: "8px",
          boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
          width: "90%",
          maxWidth: "400px",
        }}
      >
        <h2 style={{ textAlign: "center", marginBottom: "1rem" }}>
          Register
        </h2>
        <input
          style={{
            width: "100%",
            padding: "0.5rem",
            marginBottom: "1rem",
            borderRadius: "4px",
            border: "1px solid #ccc",
          }}
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter a username"
        />
        <button
          onClick={handleRegister}
          style={{
            width: "100%",
            padding: "0.5rem",
            backgroundColor: "#44c4a1",
            color: "#fff",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Register
        </button>
        {error && (
          <div
            style={{
              color: "red",
              marginTop: "1rem",
              textAlign: "center",
            }}
          >
            {error}
          </div>
        )}
      </div>
    </div>
  );
};

export default Registration;
