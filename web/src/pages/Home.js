import React, { useEffect, useState } from "react";
import Banner from "../components/Banner";
import ButtonBox from "../components/ButtonBox";
import TrendBox from "../components/TrendBox";
import KeywordsBox from "../components/KeywordsBox";
import PhishingIssues from "../components/PhishingIssues"; // 추가
import "../styles/Home.css";

function Home() {
  const [apiData, setApiData] = useState(null);  // API 데이터를 저장할 상태

  useEffect(() => {
    fetch("http://13.124.216.106:8000/api/test/")  // Django 백엔드 API 호출
      .then(response => response.json())
      .then(data => {
        console.log("백엔드 응답:", data);  // 콘솔에 응답 출력
        setApiData(data);
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
          {/* ✅ API 데이터 상태를 TrendBox에 전달 */}
          <TrendBox apiData={apiData} />
        </div>
        <div className="keyword-section">
          <KeywordsBox />
        </div>
      </div>
      <PhishingIssues />
    </div>
  );
}

export default Home;

