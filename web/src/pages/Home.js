import React, { useEffect, useState } from "react";
import Banner from "../components/Banner";
import ButtonBox from "../components/ButtonBox";
import TrendBox from "../components/TrendBox";
import KeywordsBox from "../components/KeywordsBox";  // 트렌드 데이터 받는 컴포넌트 추가
import PhishingIssues from "../components/PhishingIssues"; 
import "../styles/Home.css";

function Home() {
  const [trends, setTrends] = useState({ naver: [], google: [], twitter: [] });

  useEffect(() => {
    fetch("http://13.124.216.106:8000/api/trends-live/")  // Django 백엔드에서 실시간 트렌드 가져오기
      .then(response => response.json())
      .then(data => {
        console.log("실시간 키워드 데이터:", data);  // 콘솔 로그 확인
        setTrends(data);
      })
      .catch(error => console.error("API 오류:", error));
  }, []);

  return (
    <div className="home">
      <Banner />
      <div className="button-container">
        <ButtonBox to="/ai-check" text="AI 피싱 문자 검사" icon="/AiCheck.svg" />
        <ButtonBox to="/trend-predict" text="피싱 트렌드 예측" icon="/TrendPredict.svg" />
        <ButtonBox to="/trend-flow" text="피싱 트렌드 흐름" icon="/TrendFlow.svg" />
      </div>
      <div className="content-container">
        <div className="trend-section">
          <TrendBox />
        </div>
        <div className="keyword-section">
          {/* KeywordsBox에 trends 데이터 전달 */}
          <KeywordsBox trends={trends} />
        </div>
      </div>
      <PhishingIssues />
    </div>
  );
}

export default Home;
