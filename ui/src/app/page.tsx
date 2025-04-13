"use client"

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { API_ENDPOINTS, checkLogin } from "../constants/apiEndpoints";
import Image from 'next/image';
import hLogo from '@/../public/humanize_logo.png';

const Registration = () => {
  const [username, setUsername] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  useEffect(() => {
    checkLogin().then((current_user) => {
      // Do stuff with current user obj, like get username for display
      console.log(current_user)
      if (current_user) {
        router.push("/home");
      }
    })
  });


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
        router.push("/home");
      } else {
        setError(data.message || "Registration failed");
      }
    } catch (error) {
      setError("Network error. Please try again later.");
    }
  };


  // Look into "tabs" elements on shadcn -> register/login
  return (

    <div className="flex flex-col items-center justify-center min-h-screen gap-4">
      <Image src={hLogo} alt="Humanize Logo" style={{ width: "150px", marginBottom: "2rem" }} />

      <h1 className="text-[3rem] font-bold m-0">
        Humanize
      </h1>

      <h2 className="text-[1.5rem] font-bold mb-8">
        AI Among Us
      </h2>

      <div className="bg-[#b7fdce] p-8 rounded-[8px] [box-shadow:0_4px_8px_rgba(0,0,0,0.1)] w-[90%] max-w-[400px]">
        <h2 className="text-center mb-4 -mt-2">
          Register
        </h2>
        <input
          className="w-full p-2 mb-4 rounded-[4px] border-[1px] border-[solid] border-[#ccc]"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter a username"
        />
        <button
          onClick={handleRegister}
          className="w-full p-2 bg-[#44c4a1] text-[#fff] border-[none] rounded-[4px] cursor-pointer"
        >
          Register
        </button>
        {error && (
          <div
            className="text-[red] mt-4 text-center"
          >
            {error}
          </div>
        )}
      </div>
    </div>

  );
};

export default Registration;
