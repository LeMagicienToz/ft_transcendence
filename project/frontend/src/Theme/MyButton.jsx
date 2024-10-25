import React from 'react';
import './MyButton.css';
import { useNavigate } from "react-router-dom";

const MyButton = ({ to, text, href}) => {
	const navigate = useNavigate();
	const testos = () => {
		navigate(`/${to}`)
	}
	if(href == true)
		return(
			<a
			href={to}
			className="btn btn-primary btn-one"
			// target="_blank"
		>
			{text}
		</a>
		)

	return (
		<a
			onClick={testos}
			className="btn btn-primary btn-one"
		>
			{text}
		</a>
	);
};


export default MyButton;
