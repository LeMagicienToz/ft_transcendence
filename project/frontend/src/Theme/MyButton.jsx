import React from 'react';
import './MyButton.css';
import { useNavigate } from "react-router-dom";

const MyButton = ({ to, text, href, onClick}) => {
	const navigate = useNavigate();
	const testos = () => {
		navigate(`/${to}`)
	}
	if(href == true)
		return(
				<button
				href={to}
				className="btn btn-primary btn-one"
			>
			{text}
			</button>
		)
	else if(onClick)
		return (
				<button
				onClick={onClick}
				className="btn btn-primary btn-one"
			>
			{text}
			</button>
		)
	return (
			<button
				onClick={testos}
				className="btn btn-primary btn-one"
			>
			{text}
			</button>
		);
};


export default MyButton;
