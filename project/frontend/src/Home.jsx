import React from 'react';
import './App.css';
import AstronautAvatar from './avatar/AstronautAvatar'
import MyButton from './Theme/MyButton';
import Typewriter from './Theme/typewritter';
import My_Navbar from './Theme/My_Navbar';

function Home() {
	return (
		<>
			<div>
				{/* <AstronautAvatar></AstronautAvatar> */}
			  <My_Navbar />
			  {/* Your other components */}
			</div>		
		</>
	);
}

export default Home
