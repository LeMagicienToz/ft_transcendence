import React, { useState } from 'react';
import { Canvas } from '@react-three/fiber';
import "./AstronautAvatar.css";
import { useNavigate } from 'react-router-dom';
import MaterialAvatar from './MaterialAvatar.jsx';
import MyButton from '../Theme/MyButton.jsx';


//set_user_color
// Utility function to convert hex color to RGB array
const hexToRgb = (hex) => {
	const bigint = parseInt(hex.replace('#', ''), 16);
	const r = (bigint >> 16) & 255;
	const g = (bigint >> 8) & 255;
	const b = bigint & 255;
	return [r / 255, g / 255, b / 255];
};
	function Show_Avatar() {
		const [suitColor, setSuitColor] = useState('#FFFFFF'); // Default color in hex
		const [visColor, setVisColor] = useState('#FFFFFF');
		const [ringsColor, setRingsColor] = useState('#FFFFFF');
		const [bpColor, setBpColor] = useState('#FFFFFF');
		const [flatness, setFlatness] = useState(2.8);
		const [visTexture, setVisTexture] = useState("");
		const [horizontalPosition, setHorizontalPosition] = useState(0.73);
		const [verticalPosition, setVerticalPosition] = useState(0.08);

		const handleVisTexture = (e) => setVisTexture(e.target.value);
		const handleSuitChange = (e) => setSuitColor(e.target.value);
		const handleVisChange = (e) => setVisColor(e.target.value);
		const handleRingsChange = (e) => setRingsColor(e.target.value);
		const handleBpChange = (e) => setBpColor(e.target.value);

	// Button click handlers
		const adjustFlatness = (amount) => setFlatness(prev => Math.max(0, Math.min(5, prev + amount)));
		const adjustHorizontal = (amount) => setHorizontalPosition(prev => prev + amount);
		const adjustVertical = (amount) => setVerticalPosition(prev => prev + amount);

		const navigate = useNavigate();
		const handleClick = async (e) => {
			e.preventDefault();

			try {
				const response = await fetch('https://localhost:8443/api/auth/set_user_color/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({ suitColor, visColor, ringsColor, bpColor, flatness, horizontalPosition, verticalPosition, visTexture}),
					credentials: 'include',
				});
			
				if (response.ok) {
					// const data = await response.json();
					navigate('/Home');
				} else {
					console.log("Non-200 response", response.status, response.statusText);
					// Optional: Capture the response error details here
				}
			} catch (err) {
				console.error("Fetch error:", err);
				// setError('Une erreur s\'est produite');
			}
		};

		return (
			<div id="stage">
			<Canvas style={{ touchAction: 'none' }}>
					<ambientLight intensity={0.5} />	
					<directionalLight position={[5, 5, 5]} />
					<MaterialAvatar 
						suitColor={hexToRgb(suitColor)} 
						visColor={hexToRgb(visColor)} 
						ringsColor={hexToRgb(ringsColor)} 
						bpColor={hexToRgb(bpColor)}
						flatness={flatness} // Control flatness
						horizontalPosition={horizontalPosition} // Control horizontal position
						verticalPosition={verticalPosition} // Control vertical position
						visTexture={visTexture}
					/>
			</Canvas>
			<div className="input-container">
					<div className="Photo_url" htmlFor="visTexture">Photos URL</div>
					<input
						className="Photo_container"
						id="visTexture"
						type="text"
						value={visTexture}
						onChange={handleVisTexture}
					/>
					<div className="input-group">
					<label htmlFor="suitColor">Suit Color</label>
					<input
						id="suitColor"
						type="color"
						value={suitColor}
						onChange={handleSuitChange}
					/>
					</div>
					<div className="input-group">
					<label htmlFor="visColor">Visor Color</label>
					<input
						id="visColor"
						type="color"
						value={visColor}
						onChange={handleVisChange}
					/>
					</div>
					<div className="input-group">
					<label htmlFor="ringsColor">Rings Color</label>
					<input
						id="ringsColor"
						type="color"
						value={ringsColor}
						onChange={handleRingsChange}
					/>
					</div>
					<div className="input-group">
					<label htmlFor="bpColor">Backpack Color</label>
					<input
						id="bpColor"
						type="color"
						value={bpColor}
						onChange={handleBpChange}
					/>
					</div>

					<div className="input-group">
					<label>Flatness</label>
					<button onClick={() => adjustFlatness(-0.1)}>-</button>
					<button onClick={() => adjustFlatness(0.1)}>+</button>
				</div>

				{/* Horizontal Position Control */}
				<div className="input-group">
					<label>Horizontal Position</label>
					<button onClick={() => adjustHorizontal(-0.01)}>-</button>
					<button onClick={() => adjustHorizontal(0.01)}>+</button>
				</div>

				{/* Vertical Position Control */}
				<div className="input-group">
					<label>Vertical Position</label>
					<button onClick={() => adjustVertical(-0.01)}>-</button> 
					<button onClick={() => adjustVertical(0.01)}>+</button>
				</div>
			</div>
				<div className="button-container">
				<MyButton text="Save & Quit" onClick={handleClick}/>
				</div>
		</div>
	);
}

export default Show_Avatar;
