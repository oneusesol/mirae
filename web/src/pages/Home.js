import React from "react";
import Banner from "../components/Banner";
import ButtonBox from "../components/ButtonBox";
import TrendBox from "../components/TrendBox";
import KeywordsBox from "../components/KeywordsBox";
import PhishingIssues from "../components/PhishingIssues"; // 추가
import "../styles/Home.css";

function Home() {
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
          <KeywordsBox />
        </div>
      </div>
      <PhishingIssues /> {/* 피싱 관련 이슈 추가 */}
    </div>
  );
}

export default Home;
