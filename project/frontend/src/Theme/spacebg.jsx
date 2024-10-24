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

const SpaceBackground = ({ children }) => {
	return (
		<div>

				<div className="space-background">
					{generateStars()}
				</div>
				{children}
			</div>
	);
};

export default SpaceBackground;