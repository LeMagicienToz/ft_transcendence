import React from 'react';
import './SpaceBackground.css';


const generateStarStyles = () => {
  return Array.from({ length: 400 }, () => ({
    top: `${Math.random() * 100}vh`,
    left: `${Math.random() * 100}vw`,
    animationDuration: `${Math.random() * 10 + 5}s`,
  }));
};

const generateStars = () => {
  const starStyles = generateStarStyles();

  return starStyles.map((style, index) => (
    <div
      key={index}
      className="star"
      style={style}
    ></div>
  ));
};


  const SpaceBackground = () => {
    return (
      <div className="space-background">
        {/* Generate 200 stars */}
        {generateStars(400)}
  
        {/* Other elements like shooting stars, planets, etc. */}
        <div className="shooting-star"></div>
        <div className="shooting-star" style={{ animationDelay: '2s', left: '50%' }}></div>
        <div className="shooting-star" style={{ animationDelay: '4s', left: '75%' }}></div>
        <div className="earth"></div>
        {/* Add other elements here */}
      </div>
    );
};  

export default SpaceBackground;