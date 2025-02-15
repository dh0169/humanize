import React from "react";
import { BrowserRouter, Routes, Route, Link } from 'react-router';
import Registration from "./components/Registration";
import UserInterface from "./components/UserInterface";
import Debugger from "./components/Debugger";

function App() {
//   const isDeveloper = () => {
//     // Only developers with this "secret" key can access
//     return localStorage.getItem("devSecret") === "letMeIn";
//   };

  // return (
  //   <Router>
  //     <Routes>
  //       <Route path="/" element={<Debugger />} />
  //       {/* <Route path="/home" element={<UserInterface />} /> */}
  //     </Routes>
  //   </Router>
  // );
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Debugger />} />
        {/* <Route path="/about" element={<About />} /> */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;