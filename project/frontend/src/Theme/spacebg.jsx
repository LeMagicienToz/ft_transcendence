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

{/* <div className="sbod">


</div> */}

const SpaceBackground = ({ children }) => {
  return (
    <div>

        <div className="space-background">
          {/* Generate 400 stars */}
          {generateStars()}

          {/* Shooting stars */}
          {/* <div className="shooting-star"></div>
          <div className="shooting-star" style={{ animationDelay: '2s', left: '50%' }}></div>
          <div className="shooting-star" style={{ animationDelay: '4s', left: '75%' }}></div> */}

          {/* Earth or other elements */}
        </div>
        {children}
      </div>
  );
};

export default SpaceBackground;