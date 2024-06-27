import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
// import "./App.css";
// import Conversation from "./Conversation";
import Chat from "./Chat";

const App = () => {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* <Route path="/conversation" element={<Conversation />} /> */}
          <Route path="/chat" element={<Chat />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
