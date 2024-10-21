import './Homepage.css'
import React, { useState } from 'react';
import { Canvas } from '@react-three/fiber';
import Avatarhp from './Avatarhp';

const hexToRgb = (hex) => {
	const bigint = parseInt(hex.replace('#', ''), 16);
	const r = (bigint >> 16) & 255;
	const g = (bigint >> 8) & 255;
	const b = bigint & 255;
	return [r / 255, g / 255, b / 255];
};

const Homepage = () => {
		
	const [suitColor] = useState('#A52A2A'); // Default color in hex
	const [visColor] = useState('#A00A2A'); // Default color in hex ringsColor
	const [ringsColor] = useState('#A52A2A');
	const [bpColor] = useState('#A52A2A');

	return (
		<div className="Homebg">
			<div className="left-container">
				<Canvas style={{ touchAction: 'none' }}>
						<ambientLight intensity={0.5} />	
						<directionalLight position={[3, 3, 5]} />
						<Avatarhp
							suitColor={hexToRgb(suitColor)} 
							visColor={hexToRgb(visColor)} 
							ringsColor={hexToRgb(ringsColor)} 
							bpColor={hexToRgb(bpColor)}
						/>
				</Canvas>
				<div className="profil-button-container">
					<button type="button" class="btn btn-primary button-middle">Profile</button>
				</div>
			</div>
			{/* <div className="middle-container"> */}
				<div className="menu-button-container">
					<div className="title-game">Game</div>
					<button type="button" class="btn btn-primary button-middle">1v1</button>
					<button type="button" class="btn btn-primary button-middle">Tournois</button>
					<button type="button" class="btn btn-primary button-middle">3d game</button>
				{/* </div> */}
		
			</div>
			<div className="right-container">

			</div>
		</div>
	)
};

export default Homepage