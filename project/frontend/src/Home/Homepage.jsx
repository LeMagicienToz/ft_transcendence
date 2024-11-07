import './Homepage.css';
import React, { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import Avatarhp from './Avatarhp';
import MyButton from '../Theme/MyButton';
import logo from '../../public/logout.svg';
import { useNavigate } from "react-router-dom";

const hexToRgb = (hex) => {
	if (typeof hex === 'string') {
		const bigint = parseInt(hex.replace('#', ''), 16);
		const r = (bigint >> 16) & 255;
		const g = (bigint >> 8) & 255;
		const b = bigint & 255;
		return [r / 255, g / 255, b / 255];
	} else {
		return [1, 1, 1]; // Valeur par défaut pour éviter les erreurs
	}
};


const fetchlogOut = async () => {
	const navigate = useNavigate();
	
	const handleLogout = async (e) => {
		e.preventDefault();

		try {
			const response = await fetch('https://localhost:8443/api/auth/logout_user/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				credentials: 'include'
			});

			if (response.ok) {
				navigate('/');
			}
			else 
			{
				const errorData = await response.json();
				setError(errorData.error); // Gérer l'erreur
			}
		}catch (err) {
		   setError('Une erreur s\'est produite');
	   }
	};
}

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
			return null;
		} else {
			const errorData = await response.json();
			console.log(errorData.error);
			return null;
		}
	} catch (error) {
		console.error("Erreur lors de la requête : ", error);
		return null;
	}
};

const Homepage = () => {
	const navigate = useNavigate();
	const [logoMoved, setLogoMoved] = useState(false);
	const [userData, setUserData] = useState(null);
	const [error, setError] = useState(null);

	useEffect(() => {
		const getUserData = async () => {
			const data = await fetchUserData();
			if (data) {
				setUserData(data);
			} else {
				setError("Impossible de récupérer les données utilisateur");
			}
		};
		getUserData();
	}, []);

	const handleLogout = async () => {
		try {
			const response = await fetch('https://localhost:8443/api/auth/logout/', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				credentials: 'include'
			});

			if (response.ok) {
				navigate('/');
			} else {
				const errorData = await response.json();
				setError(errorData.error);
			}
		} catch (err) {
			console.log("dwadwa");
			setError('Une erreur s\'est produite');
		}
	};

	const handleClick = () => {
		setLogoMoved(true);
		setTimeout(() => {
			handleLogout(); // Logout after logo animation
		}, 600);
	};

	return (
		<div className="Homebg">
			<div className="logout-container">
				<button type="button" className="logout-button" onClick={handleClick}>
					<img src={logo} alt="Logo" className={`logout-logo ${logoMoved ? 'move-logo' : ''}`} />
					Logout
				</button>
			</div>
			<div className="left-container">
				<Canvas style={{ touchAction: 'none' }}>
					<ambientLight intensity={0.5} />
					<directionalLight position={[3, 3, 5]} />
					<Avatarhp
						suitColor={hexToRgb(userData?.suitColor || '#FFFFFF')}
						visColor={hexToRgb(userData?.visColor || '#FFFFFF')}
						ringsColor={hexToRgb(userData?.ringsColor || '#FFFFFF')}
						bpColor={hexToRgb(userData?.bpColor || '#FFFFFF')}
					/>
				</Canvas>
				<div className="profil-button-container">
					<MyButton to="Profile" text="My Profile" />
				</div>
			</div>
			<div className="menu-button-container">
				<div className="title-game">Game Mode</div>
				<MyButton text="1 vs 1"></MyButton>
				<MyButton text="Tournois"></MyButton>
				<MyButton text="2 vs 2"></MyButton>
			</div>
			<div className="right-container"></div>
		</div>
	);
};

export default Homepage;
