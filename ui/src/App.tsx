import React from "react";
import './styles/App.css';
import { BrowserRouter, Routes, Route, Link } from 'react-router';
import Registration from "./pages/Registration";
import UserInterface from "./pages/UserInterface";
import Debugger from "./pages/Debugger";
import About from "./pages/About";
import Play from "./pages/Play";

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