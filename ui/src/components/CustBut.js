import React from 'react';
import { useNavigate } from 'react-router';

const CustBut = ({ text, navLoc, onClick, style }) => {
    const navigate = useNavigate();

    const handleClick = () => {
        if(onClick) {
            // Potential future proofing to reuse button for voting phase
            // send param onClick="api endpoint for voting"
            onClick(onClick);
        }
        
        if(navLoc) {
            navigate(navLoc);
        }
    };

    return (
        <button
            onClick={handleClick}
            style={{
                width: "20%",
                padding: "1rem 0.5rem",
                backgroundColor: "#6BE3DC",
                color: "#000",
                border: "1px solid #73726d",
                borderRadius: "4px",
                cursor: "pointer",
                ...style, // Merge custom styles with default styles
            }}
        >
            {text} {/* Default text if no text prop is provided */}
        </button>
    );
};

export default CustBut;