import React, { useState } from 'react';
import { Button, Card, Row, Col } from 'react-bootstrap';
import './Theme/RegisterForm.css';
// import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useNavigate } from 'react-router-dom';
import SpaceBackground from "./Theme/spacebg.jsx";
import SwapButton from "./Theme/Swap_button.jsx";

function Switch_button() {
	const [isLogin, setIsLogin] = useState(true);

	// Fonction pour basculer l'état
	const toggleForm = () => {
		setIsLogin(!isLogin);
	};

	return (
		<div className="bg-container">	
			<SpaceBackground/>
				<div className="white-box">
					{isLogin ? <h2 className="top-bg">login</h2> : <h2 className="top-bg">Register</h2>}
					<div>
						{/* Bouton animé pour basculer entre Login et Register */}
						<SwapButton isLogin={isLogin} onToggle={toggleForm} />

						{/* Formulaire conditionnel */}
						{isLogin ? <LoginForm /> : <RegisterForm />}
					</div>
			</div>
		</div>
	);
}

// Login Form Component
const LoginForm = () => {
		
		const [username, setUserName] = useState('');
		const [password, setPassword] = useState('');
		const [userData, setUserData] = useState(null);
		const [error, setError] = useState('');
		const navigate = useNavigate();
		const handleLogin = async (e) => {
			e.preventDefault();

			try {
				const response = await fetch('https://localhost:8443/api/auth/login/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({ username, password }),
				});
	
				if (response.ok) {
					const data = await response.json();
					setUserData(data);
					const errorData = await response.json();
					setError(errorData.error); // Gérer l'erreur
				}
			}catch (err) {
			   setError('Une erreur s\'est produite');
		   }
		};

	
	return (
		<>			
		<div>
						<form onSubmit={handleLogin}>
							<div className="case">
								<label htmlFor="exampleInputEmail1">Email or UserName </label>
								<input
									type="username"
									className="case-input"
									username="exampleInputEmail1"
									placeholder="Enter Email or UserName"
									value={username}
									onChange={(e) => setUserName(e.target.value)}
									/>
							</div>
							<div className="case">
								<label htmlFor="exampleInputPassword1">Password </label>
								<input
									type="password"
									className="case-input"
									id="exampleInputPassword1"
									placeholder="Password"
									value={password}
									onChange={(e) => setPassword(e.target.value)}
									/>
							</div>
							<button className="mybtn" type="submit">Se connecter</button>
						</form>
					</div>
		</>

	);
}

// Register Form Component
const RegisterForm = () => {
		const [username, setUserName] = useState('');
		const [password, setPassword] = useState('');
		const [email, setEmail] = useState('');
		const [userData, setUserData] = useState(null);
		const [error, setError] = useState('');
		const navigate = useNavigate();
	
		const handleRegister = async (e) => {
			e.preventDefault();
			
			try {
				const response = await fetch('https://localhost:8443/api/auth/register/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({ username, password, email }),
				});
				if (response.ok) {
					const data = await response.json();
					setUserData(data);
					navigate('/Avatar');
				} else {
					const errorData = await response.json();
					setError(errorData.error);
				}
			} catch (err) {
				setError('Une erreur s\'est produite');
			}
		};	
	
	return (
		<>
			<div>
					<form onSubmit={handleRegister}>
						<div className="case">
							<label htmlFor="exampleInputUsername1">UserName </label>
							<input
								type="text"
								className="case-input"
								id="exampleInputUsername1"
								placeholder="Enter UserName"
								value={username}
								onChange={(e) => setUserName(e.target.value)}
								/>
						</div>
						<div className="case">
							<label htmlFor="exampleInputEmail1">Email address </label>
							<input
								type="email"
								className="case-input"
								id="exampleInputEmail1"
								placeholder="Enter email"
								value={email}
								onChange={(e) => setEmail(e.target.value)}
							/>
						</div>
						<div className="case">
							<label htmlFor="exampleInputPassword1">Password </label>
							<input
								type="password"
								className="case-input"
								id="exampleInputPassword1"
								placeholder="Password"
								value={password}
								onChange={(e) => setPassword(e.target.value)}
							/>
						</div>
						<button className="mybtn" type="submit">S´inscrire</button>
					</form>
				</div>
		</>

	);
}

export default Switch_button;
