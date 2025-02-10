import React from "react";
import "../styles/Home.css";

function AiCheck() {
  return (
    <div className="container" style={{ display: "flex", flexDirection: "row", alignItems: "flex-start", justifyContent: "center", textAlign: "left", gap: "40px", width: "95%", margin: "0 auto" }}>
      <div style={{ flex: 1 }}>
        <h2>피싱 문자 입력</h2>
        <textarea className="input-box" style={{ width: "100%", height: "300px", borderRadius: "10px" }} placeholder="검사할 문자를 입력하세요..."></textarea>
        <br />
        <button className="check-btn" style={{ width: "100%", marginTop: "30px", height: "30px", backgroundColor: "#003366", color: "white" }}>검사하기</button>
      </div>

      <div style={{ flex: 2 }}>
        <h2>검사 결과</h2>
        <div style={{ display: "flex", gap: "3px" }}>
          <textarea className="resale-box result-box" style={{ width: "100%", height: "300px", backgroundColor: "#f0f0f0", borderRadius: "10px" }} readOnly placeholder="검사 결과가 여기에 표시됩니다..."></textarea>
          <textarea className="resale-box result-box" style={{ width: "100%", height: "300px", backgroundColor: "#f0f0f0", borderRadius: "10px" }} readOnly placeholder="추가 정보가 여기에 표시됩니다..."></textarea>
        </div>
        <br />
        <button className="trend-btn" style={{ width: "100%", marginTop: "14px", height: "30px", backgroundColor: "#003366", color: "white" }}>실시간 피싱 트렌드 보기</button>
      </div>
    </div>
  );
};

export default AiCheck;