import React from "react";
import "../styles/TrendPredict.css";

const PhishingExampleList = ({ examples }) => {
  return (
    <div className="phishing-list">
      {examples.length > 0 ? (
        examples.map((example, index) => (
          <div key={index} className="phishing-box">
            {example}
          </div>
        ))
      ) : (
        <p>로딩 중...</p> // 백엔드에서 데이터가 들어오기 전 상태
      )}
    </div>
  );
};

export default PhishingExampleList;
