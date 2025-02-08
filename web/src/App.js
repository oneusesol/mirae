import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import AiCheck from "./pages/AiCheck";
import TrendPredict from "./pages/TrendPredict";
import TrendFlow from "./pages/TrendFlow";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/ai-check" element={<AiCheck />} />
        <Route path="/trend-predict" element={<TrendPredict />} />
        <Route path="/trend-flow" element={<TrendFlow />} />
      </Routes>
    </Router>
  );
}

export default App;
