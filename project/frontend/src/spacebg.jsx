import React from 'react';
import './SpaceBackground.css';

const generateStars = (numberOfStars) => {
    const stars = [];
  
    for (let i = 0; i < numberOfStars; i++) {
      const starStyle = {
        top: `${Math.random() * 100}vh`,  // Random position for vertical axis
        left: `${Math.random() * 100}vw`, // Random position for horizontal axis
        position: 'absolute',  // Ensure the stars are positioned absolutely
      };
  
      stars.push(<div key={i} className="star" style={starStyle}></div>);
    }
  
    return stars;
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