import React from 'react';
import './MyButton.css';

const MyButton = ({ to, text }) => {
  return (
    <a href={`/${to}`} className="btn btn-primary my-button">
      {text}
    </a>
  );
}

export default MyButton;
