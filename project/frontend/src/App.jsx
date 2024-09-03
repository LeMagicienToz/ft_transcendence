// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import React from 'react';
import './App.css'
// import Badge from 'react-bootstrap/Badge';
// import Button from 'react-bootstrap/Button';
import { motion } from "framer-motion";
// import { useTime } from "framer-motion";
import SpaceBackground from './spacebg';
import Typewriter from './typewritter';

function mot_button() {
	return(
		<motion.button whileTap={{ scale: 0.85 }}>
			Get Started !
		</motion.button>

	);
}

function App() {
	return (
		<>
			<div>
				<SpaceBackground />
					<h1>
						<Typewriter/>
						{/* {show_menu()} */}
						
					</h1>
						{mot_button()}
			</div>
		</>
	);
}

export default App 
