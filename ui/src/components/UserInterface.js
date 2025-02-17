import React, { useEffect } from "react";
import { API_ENDPOINTS, checkLogin } from "../constants/apiEndpoints"; // Adjust the path as needed
import { useNavigate } from "react-router";
import CustBut from "./CustBut";

const UserInterface = () => {
    const navigate = useNavigate();

    // Also add this to apiEndpoints?
    const handleLogout = async () => {
        try {
          const res = await fetch(API_ENDPOINTS.AUTH.LOGOUT, {
            credentials: "include",
          });
          const data = await res.json();
          console.log(data);
        } catch (error) {
            console.log(error.message);
        }
    };

    useEffect(() => {
        checkLogin().then((current_user) => {
          // Do stuff with current user obj, like get username for display
          console.log(current_user) 
          if(!current_user){
            navigate("/");
          }
        })
      });
    

    return (
        <div
            style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                minHeight: "100vh",
                gap: "1rem",
                backgroundColor: "#E7FFE4",
            }}
        >
            <img
                src="/humanize_logo.png"
                alt="Logo"
                style={{ width: "150px", marginBottom: "2rem" }}
            />
            <h1 style={{ fontSize: "3rem", fontWeight: "bold", margin: 0 }}>
                Humanize
            </h1>
            <h2
                style={{
                    fontSize: "1.5rem",
                    fontWeight: "bold",
                    marginBottom: "2rem",
                }}
            >
                AI Among Us
            </h2>

            // TODO: add name of logged in player?
            <CustBut text="Play" navLoc="/play" />
            <CustBut text="About" navLoc="/about"/>
            <CustBut text="Logout" navLoc="/" onClick={handleLogout}/>
        </div>
    );
}

export default UserInterface