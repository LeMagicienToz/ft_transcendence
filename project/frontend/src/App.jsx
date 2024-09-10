// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import React from 'react';
import './App.css'
// import Badge from 'react-bootstrap/Badge';
// import Button from 'react-bootstrap/Button';
// import { useTime } from "framer-motion";
import SpaceBackground from './spacebg';
import MyButton from './MyButton';
import Typewriter from './typewritter';

function App() {
	return (
		<>
			<div>
				<SpaceBackground />
					<h1>
						<Typewriter/>
						{/* {show_menu()} */}
						
					</h1>
					<MyButton to="Connection.jsx" text="Get Started!" />
						{/* {MyButton()} */}
			</div>
		</>
	);
}

export default App 
