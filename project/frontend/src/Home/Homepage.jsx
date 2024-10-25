import './Homepage.css'
import React, { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import Avatarhp from './Avatarhp';
import MyButton from '../Theme/MyButton';
import logo from '../../public/logout.svg';
import { useNavigate } from "react-router-dom";

const hexToRgb = (hex) => {
	const bigint = parseInt(hex.replace('#', ''), 16);
	const r = (bigint >> 16) & 255;
	const g = (bigint >> 8) & 255;
	const b = bigint & 255;
	return [r / 255, g / 255, b / 255];
};

const Homepage = () => {
	const navigate = useNavigate();
	
	const [suitColor] = useState('#A52A2A');
	const [visColor] = useState('#A00A2A');
	const [ringsColor] = useState('#A52A2A');
	const [bpColor] = useState('#A52A2A');
	const [logoMoved, setLogoMoved] = useState(false);

	const handleClick = () => {
		setLogoMoved(true);
		setTimeout(() => {
			navigate('/');
		  }, 600); // 0.6 seconds delay
	};

	return (
		<div className="Homebg">
			<div className="logout-container">
				<button type="button" className="logout-button" onClick={handleClick}>
					<img src={logo} alt="Logo"  className={`logout-logo ${logoMoved ? 'move-logo' : ''}`} />
					Logout
				</button>
			</div>
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
					<MyButton to="Profile" text="My Profile"/>
				</div>
			</div>
				<div className="menu-button-container">
					<div className="title-game">Game</div>
					<button type="button" className="btn btn-primary btn-one">1v1</button>
					<button type="button" className="btn btn-primary btn-one">Tournois</button>
					<button type="button" className="btn btn-primary btn-one">3d game</button>
		
			</div>
			<div className="right-container">

			</div>
		</div>
	)
};

export default Homepage