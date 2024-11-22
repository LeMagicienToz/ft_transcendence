import React from 'react';
// import './App.css';
import { Canvas } from '@react-three/fiber';
import Earth from './Home/Earth.jsx';
import './Home/Earth.css';
import Spaceship from './Home/Spaceship.jsx';
import { AuthWebSocketContext } from './auth/AuthWebSocketContext.jsx';

function Home() {
	const { socket } = useContext(AuthWebSocketContext);
	return (
		<div className="earth-container">
		<Canvas
				style={{ height: '100vh', backgroundColor: 'black' }} // Canvas styles
				camera={{ position: [0, 0, 10], fov: 75 }}
		>
			<ambientLight intensity={0.5} />
			<directionalLight position={[5, 5, 5]} />
			<Spaceship/>
			<Earth />
    </Canvas>
</div>

	);
}

export default Home
