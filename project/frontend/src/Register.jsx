import React, { useState } from 'react';
import './App.css';
import SpaceBackground from './Theme/spacebg';

function Register() {
	const [username, setUserName] = useState('');
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');

	const handleSubmit = (event) => {
		event.preventDefault();

		const data = { username, email, password };

		// Envoie des donnees
		fetch('http://localhost:8000/api/register/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(data),
		})
			.then(response => response.json())
			.then(data => {
				console.log('Success:', data);
				// Part pour gerer la reponse du back
			})
			.catch((error) => {
				console.error('Error:', error);
			});
	};

	return (
		<>
			<SpaceBackground />
			<div className="container d-flex justify-content-center align-items-center min-vh-100">
				<div className="card p-4 shadow-lg" style={{ width: '100%', maxWidth: '400px' }}>
					<h2 className="text-center mb-4">Register</h2>
					<form onSubmit={handleSubmit}>
						<div className="form-group mb-3">
							<label htmlFor="exampleInputUsername1">UserName </label>
							<input
								type="email"
								className="form-control"
								id="exampleInputUsername1"
								placeholder="Enter UserName"
								value={username}
								onChange={(e) => setUserName(e.target.value)}
							/>
						</div>
						<div className="form-group mb-3">
							<label htmlFor="exampleInputEmail1">Email address </label>
							<input
								type="email"
								className="form-control"
								id="exampleInputEmail1"
								placeholder="Enter email"
								value={email}
								onChange={(e) => setEmail(e.target.value)}
							/>
						</div>
						<div className="form-group mb-3">
							<label htmlFor="exampleInputPassword1">Password </label>
							<input
								type="password"
								className="form-control"
								id="exampleInputPassword1"
								placeholder="Password"
								value={password}
								onChange={(e) => setPassword(e.target.value)}
							/>
						</div>
						<button type="submit" className="btn btn-primary btn-block">
							Submit
						</button>
					</form>
				</div>
			</div>
		</>
	);
}

export default Register;
