import React from "react";
import { Link } from "react-router-dom";
import "../styles/Navbar.css"; // 스타일 적용

function Navbar() {
  return (
    <nav className="navbar">
      <div className="logo">
        <img src="/favicon.svg" alt="Phish Rader Logo" className="logo-img" />
        <span className="logo-text">Phish Rader</span>
      </div>
      <div className="nav-links">
        <Link to="/">소개</Link>
        <Link to="/ai-check">제보</Link>
        <Link to="/trend-predict">기능1</Link>
      </div>
    </nav>
  );
}

export default Navbar;
