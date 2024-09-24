import React, { useState } from 'react';
import { Form, Button, Card, Container, Row, Col } from 'react-bootstrap';
// import './App.css';
import SpaceBackground from './Theme/spacebg';
import './Theme/RegisterForm.css';
import { AuthService } from './services/AuthService';
import MyButton from './Theme/MyButton';

function Switch_button() {
  // State to toggle between login and registration form
  const [isLogin, setIsLogin] = useState(true);

  // Function to toggle between login and register
  const toggleForm = () => {
    setIsLogin(!isLogin);
  };

  return (
    <div>
  <SpaceBackground />

    <Container className="d-flex align-items-center justify-content-center" style={{ minHeight: '100vh' }}>
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
    </Container>
    </div>
  );
}

// Login Form Component
function LoginForm() {
  const [id, setId] = useState('');
	const [password, setPassword] = useState('');
	const response = "";
	
	const authService = new AuthService();

	const handleSubmit = (event) => {
		event.preventDefault();

		const data = { username, email, password };

		// Envoie des donnees
		authService.login(response);
		if (response) {
			console.log("good");
		} else {
			console.log("bad");
		}
	};

	
	return (
		<>
			<div className="white-box">
						<h2 className="top-bg">Login</h2>
						<form onSubmit={handleSubmit}>
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
						</form>
              <MyButton to="Avatar" text="Submit"/>
					</div>
		</>

	);
}

// Register Form Component
function RegisterForm() {
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
							<MyButton to="Avatar" text="Submit"/>
					</div>
		</>

	);
}

export default Switch_button;
