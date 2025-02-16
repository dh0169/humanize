import React from "react";
import { BrowserRouter, Routes, Route, Link } from 'react-router';
import Registration from "./components/Registration";
import UserInterface from "./components/UserInterface";
import Debugger from "./components/Debugger";

function App() {
   const isDeveloper = () => {
     // Only developers with this "secret" key can access
     return localStorage.getItem("devSecret") === "letMeIn";
   };


  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Registration />} />
        {/* <Route path="/about" element={<About />} /> */}
        {/* <Route path="Registration" element={<Registration />}/> */}
        <Route path="Home" element={<UserInterface />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;