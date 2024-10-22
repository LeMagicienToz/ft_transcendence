import React from 'react';
import Button from 'react-bootstrap/Button';
import './App.css'
import MyButton from './Theme/MyButton';
import Typewriter from './Theme/typewritter';
import "./index.css";
import SpaceBackground from "./Theme/spacebg.jsx";

function App() {

	return (
		<>
			<div className="bg-container">	
				<SpaceBackground/>
					<div className="typewriter-container">
						<Typewriter text="Ft_Transcendence"/>
						<div className="button-placement">
							<MyButton to="login" text="Register/Login" />
							<MyButton to="https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-0fb37f903a509ffef7fef8a465a0d364fd68770a44139adc8a756ee25376f128&redirect_uri=https%3A%2F%2Flocalhost%3A8443%2Fapi%2Fauth%2Fcallback%2F42%2F&response_type=code" text="log42" />
						</div>
					</div>
			</div>
		</>
	);
}

export default App 
