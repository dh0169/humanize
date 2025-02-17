import React from "react";
import { BrowserRouter, Routes, Route, Link } from 'react-router';
import Registration from "./components/Registration";
import UserInterface from "./components/UserInterface";
import Debugger from "./components/Debugger";
import About from "./components/About";
import Play from "./components/Play";

function App() {
   const isDeveloper = () => {
     // Only developers with this "secret" key can access
     return localStorage.getItem("devSecret") === "letMeIn";
   };


  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Registration />} />
        <Route path="/about" element={<About />} />
        <Route path="/home" element={<UserInterface />} />
        <Route path="/debug" element={isDeveloper() ? <Debugger /> : "Hey, what are you looking for?" } />
        <Route path="/play" element={<Play />}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;