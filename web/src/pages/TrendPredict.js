import React, { useState, useEffect } from "react";
import "./../styles/TrendPredict.css";
import PhishingExampleList from "../components/PhishingExampleList";

const TrendPredict = () => {
  const [categories, setCategories] = useState([]);
  const [phishingExamples, setPhishingExamples] = useState([]);

  useEffect(() => {
    const mockCategories = ["보험/카드", "도박", "취업", "대출"];

    fetch("https://api.example.com/phishing-examples")
      .then((response) => response.json())
      .then((data) => {
        setPhishingExamples(data);
      })
      .catch((error) => {
        console.error("API 오류:", error);
        setPhishingExamples(["예시 1 (오류 발생)", "예시 2 (오류 발생)", "예시 3 (오류 발생)"]);
      });

    setCategories(mockCategories);
  }, []);

  return (
    <div className="trend-predict-container">
      <h2>피싱 트렌드 예측</h2>

      <div className="container-box">
        <div className="category-container">
          <h3 className="category-title">카테고리</h3>
          <div className="category-list">
            {categories.map((category, index) => (
              <div key={index} className="category-box">
                #{category}
              </div>
            ))}
          </div>
        </div>

        <div className="phishing-warning-container">
          <h3 className="phishing-warning-title">! 다음과 같은 피싱을 주의하세요</h3>
          <PhishingExampleList examples={phishingExamples} />
        </div>
      </div>
    </div>
  );
};

export default TrendPredict;
