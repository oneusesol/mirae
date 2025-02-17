import React, { useEffect, useState } from "react";
import "../styles/TrendFlow.css";

function TrendFlow() {
  const [trends, setTrends] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/data/trends.json") // public 폴더에서 JSON 불러오기
      .then((response) => {
        if (!response.ok) {
          throw new Error("데이터를 불러오는 데 실패했습니다.");
        }
        return response.json();
      })
      .then((data) => {
        setTrends(data);
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>데이터 로딩 중...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div className="TrendFlow">
      <header className="header"></header>

      <div className="container">
        <h2>피싱 트렌드 흐름</h2>
        <div className="year-section">
          {Object.keys(trends).map((year) => (
            <div key={year} className="year-block">
              <div className="year-title">{year}</div>
              <div className="quarter-container">
                {Object.keys(trends[year]).map((quarter) => (
                  <div className="quarter-wrapper" key={quarter}>
                    <div className="quarter-label">{quarter}</div>
                    <div className="quarter">
                      {trends[year][quarter] ? trends[year][quarter] : "데이터 없음"}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default TrendFlow;
