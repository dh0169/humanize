// Edit this for the general layout of the page
// In this example, utilized the styling established by Aaron
// (mint green-ish background for every page)


import React from 'react';

interface LayoutProps {
    children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
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
            {children}
        </div>
    );
};

export default Layout;