import React from "react";
import { Link } from "react-router-dom";
import "../styles/Navbar.css"; // 스타일 적용

function Navbar() {
  return (
    <nav className="navbar">
      <div className="logo">
        <img src="/favicon.svg" alt="Phish Rader Logo" className="logo-img" />
        <span className="logo-text"><Link to="/">Phish Rader</Link></span>
      </div>
      <div className="nav-links">
        <Link to="/">소개</Link>
        <Link to="/">제보</Link>
      </div>
    </nav>
  );
}

export default Navbar;
