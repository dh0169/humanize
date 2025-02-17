import React from "react";
import { BrowserRouter, Routes, Route, Link } from 'react-router';
import Registration from "./components/Registration";
import UserInterface from "./components/UserInterface";
import Debugger from "./components/Debugger";
import About from "./components/About";

function App() {
   const isDeveloper = () => {
     // Only developers with this "secret" key can access
     return localStorage.getItem("devSecret") === "letMeIn";
   };

<<<<<<< HEAD

=======
>>>>>>> 6f0fea930b585c119cb741c3415d9ddf25cc9218

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Registration />} />
        <Route path="/about" element={<About />} />
        {/* <Route path="Registration" element={<Registration />}/> */}
        <Route path="/home" element={<UserInterface />} />
        <Route path="/debug" element={isDeveloper() ? <Debugger /> : "Hey, what are you looking for?" } />
      </Routes>
    </BrowserRouter>
  );
}

export default App;