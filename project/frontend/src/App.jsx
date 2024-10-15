import React from 'react';
import './App.css'
import MyButton from './Theme/MyButton';
import Typewriter from './Theme/typewritter';
import "./index.css";
function App() {
	return (
		<>
			<div>
					<h1>
						<Typewriter text="Ft_Transcendence" csscontext="typewriter-container"/>
						{/* {show_menu()} */}
						
					</h1>
					<MyButton to="https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-0fb37f903a509ffef7fef8a465a0d364fd68770a44139adc8a756ee25376f128&redirect_uri=https%3A%2F%2Flocalhost%3A8443%2Fapi%2Fauth%2Fcallback%2F42%2F&response_type=code" text="Login with 42" />
						{/* {MyButton()} */}
					<MyButton to="login" text="Register/Login" />
						{/* {MyButton()} */}
			</div>
		</>
	);
}

export default App 
