import React from "react";
import "../styles/PhishingIssues.css";

function PhishingIssues() {
  return (
    <div className="issues-container">
      <h2 className="issues-title">피싱 관련 이슈</h2>
      <div className="issues-list">
        {/* 기사 6개 공간 (2개씩 가로 정렬) */}
        {Array(6).fill().map((_, index) => (
          <div className="issue-item" key={index}>
            <div className="issue-thumbnail"></div> {/* 이미지 자리 */}
            <div className="issue-content">
              <h3 className="issue-headline">기사 제목 {index + 1}</h3>
              <p className="issue-summary">기사 내용이 들어갈 공간입니다...</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default PhishingIssues;
