import React from "react";
import "../styles/Banner.css"; // 스타일 적용

function Banner() {
  return (
    <div className="banner">
      <div className="banner-content">
        <div className="logo-title">
          <img src="/favicon.svg" alt="Phish Rader Logo" className="banner-logo" />
          <h1 className="banner-title">Phish Rader</h1>
        </div>
        <p className="banner-subtitle">새로운 피싱 위협 예측 서비스</p>
      </div>
    </div>
  );
}

export default Banner;
