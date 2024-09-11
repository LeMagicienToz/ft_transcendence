import React from 'react';
import './App.css'
import SpaceBackground from './Theme/spacebg';
import Typewriter from './Theme/typewritter';

// The component name should be capitalized and followed by parentheses
function ConnectionPage() {
	return (
		<>
		<div>
			<SpaceBackground />
				<h1>
					<Typewriter text="Login" csscontext="typewriter-main"/>
					{/* {show_menu()} */}
				</h1>
		</div>
	 </>
	);
}

export default ConnectionPage;