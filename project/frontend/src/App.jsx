import React from 'react';
import './App.css'
import SpaceBackground from './Theme/spacebg';
import MyButton from './Theme/MyButton';
import Typewriter from './Theme/typewritter';
import { Link } from 'react-router-dom';  // Link component for navigation

function App() {
	return (
		<>
			<div>
				<SpaceBackground />
					<h1>
						<Typewriter text="Ft_Transcendence" csscontext="typewriter-container"/>
						{/* {show_menu()} */}
						
					</h1>
					<MyButton to="ConnectionPage" text="Get Started!" />
						{/* {MyButton()} */}
			</div>
		</>
	);
}

export default App 
