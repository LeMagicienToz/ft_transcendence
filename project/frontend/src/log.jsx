import React, { useState } from 'react';
import { Form, Button, Card, Container, Row, Col } from 'react-bootstrap';
import './Theme/RegisterForm.css';
// import { AuthService } from './services/AuthService';
// import MyButton from './Theme/MyButton';

function Switch_button() {
  // State to toggle between login and registration form
  const [isLogin, setIsLogin] = useState(true);

  // Function to toggle between login and register
  const toggleForm = () => {
    setIsLogin(!isLogin);
  };

  return (
    <div>
    {/* <Container className="" style={{ minHeight: '100vh' }}> */}
      <Row>
        <Col>
          <Card>
            <Card.Body>
              {isLogin ? <LoginForm /> : <RegisterForm />}
              <div className="text-center mt-3">
                {isLogin ? "Don't have an account?" : 'Already have an account?'}
                <Button variant="link" onClick={toggleForm}>
                  {isLogin ? 'Register here' : 'Login here'}
                </Button>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    {/* </Container> */}
    </div>
  );
}

// Login Form Component
const LoginForm = () => {
		const [id, setId] = useState('');
		const [password, setPassword] = useState('');
		const [userData, setUserData] = useState(null);
		const [error, setError] = useState('');
	
		const handleLogin = async (e) => {
			e.preventDefault();
			
			try {
				const response = await fetch('http://localhost:8080/login/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({ id, password }),
				});
	
				if (response.ok) {
					const data = await response.json();
					setUserData(data); // Ici, vous pouvez récupérer user_id, user_name et image_url
				} else {
					const errorData = await response.json();
					setError(errorData.error); // Gérer l'erreur
				}
			} catch (err) {
				setError('Une erreur s\'est produite');
			}
		};	

	
	return (
		<>
			<div className="white-box">
						<h2 className="top-bg">Login</h2>
						<form onSubmit={handleLogin}>
							<div className="case">
								<label htmlFor="exampleInputEmail1">Email or UserName </label>
								<input
									type="id"
									className="case-input"
									id="exampleInputEmail1"
									placeholder="Enter Email or UserName"
									value={id}
									onChange={(e) => setId(e.target.value)}
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
							<button type="submit">Se connecter</button>
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
	
		const handleRegister = async (e) => {
			e.preventDefault();
			
			try {
				const response = await fetch('http://localhost:8080/register/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({ username, password }),
				});
	
				if (response.ok) {
					const data = await response.json();
					setUserData(data); // Ici, vous pouvez récupérer user_id, user_name et image_url
				} else {
					const errorData = await response.json();
					setError(errorData.error); // Gérer l'erreur
				}
			} catch (err) {
				setError('Une erreur s\'est produite');
			}
		};	
	
	return (
		<>
				<div className="white-box">
					<h2 className="top-bg">Register</h2>
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
							<button type="submit">S´inscrire</button>
						</form>
							{/* <MyButton to="Avatar" text="Submit"/> */}
					</div>
		</>

	);
}

export default Switch_button;
