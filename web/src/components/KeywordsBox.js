import React from "react";

function KeywordsBox({ trends }) {
  return (
    <div className="keywords-box">
      <h3>실시간 주목 받고 있는 키워드</h3>
      <div>
        <h4>네이버</h4>
        <ul>{trends.naver.map((word, index) => <li key={index}>{word}</li>)}</ul>
      </div>
      <div>
        <h4>구글</h4>
        <ul>{trends.google.map((word, index) => <li key={index}>{word}</li>)}</ul>
      </div>
      <div>
        <h4>트위터</h4>
        <ul>{trends.twitter.map((word, index) => <li key={index}>{word}</li>)}</ul>
      </div>
    </div>
  );
}

export default KeywordsBox;
