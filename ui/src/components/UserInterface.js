import { API_ENDPOINTS } from "../constants/apiEndpoints"; // Adjust the path as needed
import { Navigate, useNavigate } from "react-router";

const UserInterface = () => {
    const nav = useNavigate();
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
            <button
                onClick={() => nav("/play")}
                style={{
                    width: "20%",
                    padding: "1rem 0.5rem",
                    backgroundColor: "#6BE3DC",
                    color: "#000",
                    border: "1px solid#73726d",
                    borderRadius: "4px",
                    cursor: "pointer",
                }}
            >
                Play
            </button>
            <button
                onClick={() => nav("/about")}
                style={{
                    width: "20%",
                    padding: "1rem 0.5rem",
                    backgroundColor: "#6BE3DC",
                    color: "#000",
                    border: "1px solid#73726d",
                    borderRadius: "4px",
                    cursor: "pointer",
                }}
            >
                About
            </button>
        </div>
    );
}

export default UserInterface