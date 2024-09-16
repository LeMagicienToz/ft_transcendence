import React from 'react';
import './App.css'
import SpaceBackground from './Theme/spacebg';
import MyButton from './Theme/MyButton';
import Typewriter from './Theme/typewritter';
import "./index.css";
import DisableButton from './Theme/DisableButton';
function App() {
	return (
		<>
			<div>
				
				<SpaceBackground />
					<h1>
						<Typewriter text="Ft_Transcendence" csscontext="typewriter-container"/>
						{/* {show_menu()} */}
						
					</h1>
					<MyButton to="https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-242573ba154f7837cd46b6784ee0617f44e56f4721266aa5e981458c6ed0ac86&redirect_uri=http%3A%2F%2Flocalhost%3A5173%2FHome&response_type=code" text="Login with 42" />
						{/* {MyButton()} */}
					<MyButton to="Register" text="Register" />
						{/* {MyButton()} */}
			</div>
			<div classname="custom-tag">
					<DisableButton />
			</div>
		</>
	);
}

export default App 
