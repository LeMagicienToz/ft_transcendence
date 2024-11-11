import './Homepage.css';
import React, { useContext, useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import Avatarhp from './Avatarhp';
import MyButton from '../Theme/MyButton';
import logo from '../../public/logout.svg';
import { useNavigate } from "react-router-dom";
import Modal_composant from "../Theme/modal_composant/Modal_composant.jsx";
import Tableone from "../game/Tableone.jsx";
import { AuthContext } from '../auth/AuthContext';
import MaterialAvatar from '../avatar/MaterialAvatar.jsx';

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

const fetchUserData = async () => {
		try {
			const response = await fetch('/api/auth/get_user/', {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
				},
				credentials: 'include'
			});
	
			if (response.ok) {
				return await response.json();
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
	const [closed_modal, setClosed_modal] = useState(true);
	const [value_modal, setValueModal] = useState(0);
	const { logout } = useContext(AuthContext);

	const onClosedModal = () => {
		setClosed_modal(true);
	}

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

	const renderContent = () => {
		switch (value_modal) {
		  case 0:
			return <Tableone create={true}/>;
		  default:
		  return <Tableone create={false}/>;
		}
	  };

	const handleLogout = async () => {
		try {
			const response = await fetch('/api/auth/logout/', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				credentials: 'include'
			});

			if (response.ok) {
				logout();
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
		}, 400);
	};
	return (
		<>
		{!closed_modal ? <Modal_composant onClosedModal={onClosedModal}>
		{renderContent()}
		</Modal_composant> : null}	
			<div className="Homebg">
				<div className="left-container">
					<Canvas style={{ position: 'relative', touchAction: 'none' }}>
						<ambientLight intensity={0.5} />
						<directionalLight position={[3, 3, 5]} />
						<MaterialAvatar
							suitColor={hexToRgb(userData?.suitColor || '#FFFFFF')}
							visColor={hexToRgb(userData?.visColor || '#FFFFFF')}
							ringsColor={hexToRgb(userData?.ringsColor || '#FFFFFF')}
							bpColor={hexToRgb(userData?.bpColor || '#FFFFFF')}
							flatness={userData?.flatness || 2.8}
							horizontalPosition={userData?.horizontalPosition || 0.73}
							verticalPosition={userData?.verticalPosition || 0.08}
							visTexture={userData?.visTexture || null}
							/>
					</Canvas>
					<div className="profil-button-container">
						<MyButton text="Profile" to="profile" />
						<MyButton text="Avatar" to="avatar" />
					</div>
				</div>
				<div className="menu-button-container">
					<div className="title-game">Space 🚀 Pong</div>
					<MyButton text="Create a game" onClick={() => {
						setClosed_modal(false);
						setValueModal(0);
					}}/>
					{/* </MyButton> */}
					<MyButton text="Join a game" onClick={() => {
						setClosed_modal(false);
						setValueModal();
					}}/>
				</div>
				<div className="right-container">
					<div className="logout-container">
						<button type="button" className="logout-button" onClick={handleClick}>
							<img src={logo} alt="Logo" className={`logout-logo ${logoMoved ? 'move-logo' : ''}`} />
							Logout
						</button>
					</div>
				</div>
			</div>
		</>
	);
};

export default Homepage;
