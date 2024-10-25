import React from 'react';
import Button from 'react-bootstrap/Button';
import './App.css'
import MyButton from './Theme/MyButton';
import Typewriter from './Theme/typewritter';
import "./index.css";
import SpaceBackground from "./Theme/spacebg.jsx";

function App() {
	const authorizeURL = new URL("https://api.intra.42.fr/oauth/authorize");
	authorizeURL.searchParams.append("client_id", "u-s4t2ud-0fb37f903a509ffef7fef8a465a0d364fd68770a44139adc8a756ee25376f128")
	authorizeURL.searchParams.append("redirect_uri", "https://localhost:8443/api/auth/callback/42/")
	authorizeURL.searchParams.append("response_type", "code")
	return (
		<>
			<div className="bg-container">	
				<SpaceBackground/>
					<div className="typewriter-container">
						<Typewriter text="Ft_Transcendence"/>
						<div className="button-placement">
							<MyButton to="login" text="Register/Login" />
							<MyButton to={authorizeURL} text="log42" href={true} />
						</div>
					</div>
			</div>
		</>
	);
}

export default App 
