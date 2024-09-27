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
					<MyButton to="https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-f1baaa46276efc8df101232e02ee11a95c2db9c89960cd4a176966f230277a1f&redirect_uri=https%3A%2F%2Flocalhost%3A8443%2Fhome&response_type=code" text="Login with 42" />
						{/* {MyButton()} */}
					<MyButton to="login" text="Register/Login" />
						{/* {MyButton()} */}
			</div>
		</>
	);
}

export default App 
