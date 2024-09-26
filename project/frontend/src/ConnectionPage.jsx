import React from 'react';
// import './App.css';
import Typewriter from './Theme/typewritter';

// The component name should be capitalized and followed by parentheses
function ConnectionPage() {
	return (
		<>
		<div>
				<h1>
					<Typewriter text="Login" csscontext="typewriter-main"/>
					{/* {show_menu()} */}
				</h1>
		</div>
	 </>
	);
}

export default ConnectionPage;