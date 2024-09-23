import React, { useState } from 'react';
// import './App.css';
import './Theme/RegisterForm.css';

// Login Form Component
function LoginForm() {
  return (
    <Form>
      <Form.Group id="email">
        <Form.Label>Email</Form.Label>
        <Form.Control type="email" required />
      </Form.Group>
      <Form.Group id="password">
        <Form.Label>Password</Form.Label>
        <Form.Control type="password" required />
      </Form.Group>
      <Button className="w-100 mt-3" type="submit">
        Log In
      </Button>
    </Form>
  );
}

function switch_button() {
// State to toggle between login and registration form
const [isLogin, setIsLogin] = useState(true);

// Function to toggle between login and register
const toggleForm = () => {
	setIsLogin(!isLogin);
};

return (
	<Container className="d-flex align-items-center justify-content-center" style={{ minHeight: '100vh' }}>
	<Row>
		<Col>
		<Card>
			<Card.Body>
			<h2 className="text-center mb-4">
				{isLogin ? 'Login' : 'Register'}
			</h2>
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
);
}

export default switch_button;