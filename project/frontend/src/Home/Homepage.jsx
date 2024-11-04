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

const fetchUserData = async () => {
	try {
	  const response = await fetch('https://localhost:8443/api/auth/get_user/', {
		method: 'GET',
		headers: {
		  'Content-Type': 'application/json',
		},
		credentials: 'include'
	  });
  
	  if (response.ok) {
		const data = await response.json();
		return(data);
	  } else {
		  const errorData = await response.json();
		  console.log(errorData.error);
		}
	} catch (error) {
	  console.error("Erreur lors de la requête : ", error);
	  console.log("Une erreur est survenue");
	}
  };

const Homepage = () => {

	const data=fetchUserData();
	const navigate = useNavigate();

	const [logoMoved, setLogoMoved] = useState(false);
	
	const [userData, setUserData] = useState(null);
	const [error, setError] = useState(null);
	
	useEffect(() => {
		const getUserData = async () => {
			try {
				const data = await fetchUserData();
				setUserData(data);
			} catch (error) {
				setError("Impossible de récupérer les données utilisateur");
			}
		};
	getUserData();
}, []);

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
							suitColor={error ? hexToRgb('#FFFFFF') : hexToRgb(userData ? userData.suitColor : '#FFFFFF')}
							visColor={error ? hexToRgb('#FFFFFF') : hexToRgb(userData ? userData.visColor : '#FFFFFF')}
							ringsColor={error ? hexToRgb('#FFFFFF') : hexToRgb(userData ? userData.ringsColor : '#FFFFFF')}
							bpColor={error ? hexToRgb('#FFFFFF') : hexToRgb(userData ? userData.bpColor : '#FFFFFF')}
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