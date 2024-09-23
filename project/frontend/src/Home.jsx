import React from 'react';
import './App.css'
import SpaceBackground from './Theme/spacebg';
import MyButton from './Theme/MyButton';
import Typewriter from './Theme/typewritter';

function Home() {
	return (
		<>
			<div>
				
				<SpaceBackground />
					<h1>
						<Typewriter text="Home" csscontext="typewriter-container"/>
						{/* {show_menu()} */}
						
					</h1>
					<MyButton to="Login" text="Get Started!" />
						{/* {MyButton()} */}
			</div>
		</>
	);
}

export default Home
