import React, { useState } from "react";
import "../styles/AiCheck.css";
import InputBox from "../components/InputBox"; // 🔥 새로 만든 InputBox 컴포넌트 가져오기

function AiCheck() {
  const [inputText, setInputText] = useState("");

  return (
    <div className="ai-check-container">
      {/* 타이틀 */}
      <h1 className="ai-check-title">
        <span className="icon">🔍</span> AI 피싱 문자 검사
      </h1>

      {/* 입력 및 결과 컨테이너 */}
      <div className="ai-check-content">
        {/* 피싱 문자 입력 */}
        <div className="input-section">
          <h2 className="section-title">피싱 문자 입력</h2>
          <InputBox onTextChange={setInputText} /> {/* 🔥 분리된 컴포넌트 사용 */}
          <button className="check-btn">검사하기</button>
        </div>

        {/* 검사 결과 */}
        <div className="result-section">
          <h2 className="section-title">검사 결과</h2>
          <div className="result-box-container">
            <div className="result-box"></div>
            <div className="result-box"></div>
          </div>
          <button className="trend-btn">실시간 피싱 트렌드 보러가기</button>
        </div>
      </div>
    </div>
  );
}

export default AiCheck;
