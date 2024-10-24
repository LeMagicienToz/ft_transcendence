import './Homepage.css'
import React, { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import Avatarhp from './Avatarhp';

const hexToRgb = (hex) => {
	const bigint = parseInt(hex.replace('#', ''), 16);
	const r = (bigint >> 16) & 255;
	const g = (bigint >> 8) & 255;
	const b = bigint & 255;
	return [r / 255, g / 255, b / 255];
};

const fetchUserData = async () => {
	try {
	  const response = await fetch('https://localhost:8443/api/auth/get_42_user/', {
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
	
	const [suitColor] = useState('#A52A2A');
	const [visColor] = useState('#A00A2A');
	const [ringsColor] = useState('#A52A2A');
	const [bpColor] = useState('#A52A2A');
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

	return (
		<div className="Homebg">
			{error ? (
				<h1>{error}</h1> // Afficher un message d'erreur si une erreur est survenue
			) : (
				<h1>
				{userData ? userData.username : "None"} {/* Afficher le nom d'utilisateur ou un message de chargement */}
				</h1>
			)}
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
					<button type="button" class="btn btn-primary btn-one">Profile</button>
				</div>
			</div>
			{/* <div className="middle-container"> */}
				<div className="menu-button-container">
					<div className="title-game">Game</div>
					<button type="button" class="btn btn-primary btn-one">1v1</button>
					<button type="button" class="btn btn-primary btn-one">Tournois</button>
					<button type="button" class="btn btn-primary btn-one">3d game</button>
				{/* </div> */}
		
			</div>
			<div className="right-container">

			</div>
		</div>
	)
};

export default Homepage