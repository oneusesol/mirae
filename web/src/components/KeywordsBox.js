import React from "react";
import "../styles/KeywordsBox.css";

function KeywordsBox() {
  return (
    <div className="keywords-box-container">
      <h2 className="keywords-title">실시간 주목 받고 있는 키워드</h2>
      <div className="keywords-box"></div>
    </div>
  );
}

export default KeywordsBox;
