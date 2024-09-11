import React from 'react';
import './App.css'
import SpaceBackground from './Theme/spacebg';
import MyButton from './Theme/MyButton';
import Typewriter from './Theme/typewritter';

function App() {
	return (
		<>
			<div>
				<SpaceBackground />
					<h1>
						<Typewriter text="Ft_Transcendence" csscontext="typewriter-container"/>
						{/* {show_menu()} */}
						
					</h1>
					<MyButton to="ConnectionPage.jsx" text="Get Started!" />
						{/* {MyButton()} */}
			</div>
		</>
	);
}

export default App 
