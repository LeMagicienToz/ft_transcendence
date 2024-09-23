import React, { useState } from 'react';
// import './App.css';
import SpaceBackground from './Theme/spacebg';
import './Theme/RegisterForm.css';
import { AuthService } from './services/AuthService';
import MyButton from './Theme/MyButton';
// import { switch_button } from "./log.jsx";


function Register() {
	const [username, setUserName] = useState('');
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const response = "";
	
	const authService = new AuthService();

	const handleSubmit = (event) => {
		event.preventDefault();

		const data = { username, email, password };

		// Envoie des donnees
		authService.register(response);
		if (response) {
			console.log("good");
		} else {
			console.log("bad");
		}
	};

	
	return (
		<>
			<SpaceBackground />
			<div className="white-box">
						<h2 className="top-bg">Register</h2>
						<form onSubmit={handleSubmit}>
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
						</form>
							<MyButton to="aaaa" text="aaa"/>
					</div>
		</>

	);
}

export default Register;
