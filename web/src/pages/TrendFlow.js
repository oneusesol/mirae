import React from "react";
import "../styles/TrendFlow.css";

function TrendFlow() {
  return (
    <div className="TrendFlow">
      <header className="header">
      </header>

      <div className="container">
        <h2>피싱 트렌드 흐름</h2>
        <div className="year-section">
          {["2025년", "2024년", "2023년"].map((year) => (
            <div key={year}>
              <div className="year-title">{year}</div>
              <div className="quarter-container">
                {["1분기", "2분기", "3분기", "4분기"].map((quarter) => (
                  <div className="quarter-wrapper" key={quarter}>
                    <div className="quarter-label">{quarter}</div>
                    <div className="quarter"></div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default TrendFlow;