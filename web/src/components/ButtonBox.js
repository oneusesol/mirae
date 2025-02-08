import React from "react";
import { Link } from "react-router-dom";
import "../styles/ButtonBox.css"; // 스타일 적용

function ButtonBox({ to, text, icon }) {
  return (
    <Link to={to} className="button-box">
      <img src={icon} alt={text} className="button-icon" />
      <span className="button-text">{text}</span>
    </Link>
  );
}

export default ButtonBox;
