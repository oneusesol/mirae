import React, { useState } from "react";

function InputBox({ onTextChange }) {
  const [text, setText] = useState("");

  const handleChange = (e) => {
    setText(e.target.value);
    if (onTextChange) {
      onTextChange(e.target.value); // 부모 컴포넌트로 입력값 전달
    }
  };

  return (
    <textarea
      className="input-box"
      placeholder="피싱 문자를 입력해주세요."
      value={text}
      onChange={handleChange}
    />
  );
}

export default InputBox;
