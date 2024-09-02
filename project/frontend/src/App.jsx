import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Badge from 'react-bootstrap/Badge';
import Button from 'react-bootstrap/Button';
import { motion } from "framer-motion";
import { useTime } from "framer-motion"


function show_menu() {
	const time = useTime()
	const rotate = useTransform(
	time,
	[0, 4000], // For every 4 seconds...
	[0, 360], // ...rotate 360deg
	{ clamp: false }
)
}


function mot_button() {
	return(
		<motion.button whileTap={{ scale: 0.85 }}>
			Get Started !
		</motion.button>

	)
}


function App() {
	return (
		<>
		<view className='bg'>
			<div>
					<h1>
						{/* {show_menu()} */}
						{mot_button()}
						
					</h1>
			</div>
		</view>
		</>
	)
}

export default App 
