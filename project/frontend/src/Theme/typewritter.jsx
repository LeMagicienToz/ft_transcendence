
// src/Typewriter.js
import React from 'react';
import './Typewriter.css'; // We'll create this CSS file next

const Typewriter = ({ text }) => {

  return (
    <div> 
    {text.split("").map((letter, index) => (
        <span
          key={index}
          className="typewriter-letter"
          style={{ animationDelay: `${index * 0.1}s` }}
        >
          {letter}
        </span>
      ))}
    </div>
  );
};

export default Typewriter;
