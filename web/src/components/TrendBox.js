import React from "react";
import "../styles/TrendBox.css";

function TrendBox({ apiData }) {
  return (
    <div className="trend-box-container">
      <h2 className="trend-title">피싱 트렌드 예측</h2>
      <div className="trend-box">
        {/* ✅ API 데이터가 있으면 메시지 출력, 없으면 "데이터 로딩 중..." */}
        {apiData ? (
          <p className="trend-message">API로 데이터가 가져와졌습니다.</p>
        ) : (
          <p className="trend-message">데이터 로딩 중...</p>
        )}
      </div>
    </div>
  );
}

export default TrendBox;
