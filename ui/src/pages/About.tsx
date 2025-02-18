import React from 'react';

//TODO: Fix the spacing to make it look better, maybe make the text more uniform so it looks better
//TODO: Add a button to go back to the main page

const About = () => {
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
            <p style={{ textAlign: "center", width: "50%", fontSize: "50px", fontStyle: "italic" }}>
                How To Play:
            </p>
            <p><strong>Humanize</strong> is a game which can be explained simply; find the AI Among Us!</p>
            <p>You will be put into a game ranging from 4-6 players, but here’s the catch; one of them is actually an Artificial Intelligence with the goal of making it to the final round.</p>
            <p>Converse with each other to decipher who is human and who isn’t.</p>
            <p>At the end of each round you must choose to vote someone out.</p>
            <p>If the AI gets voted out, the humans win.</p>
            <p>If there is an AI among the last 2 players, the AI wins.</p>
            <p><strong>Do not let the AI take over humanity!</strong></p>
        </div>
    )
}

export default About;