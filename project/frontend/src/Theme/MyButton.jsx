import React from 'react';
import './MyButton.css';

const MyButton = ({ to, text }) => {
  const isExternal = to.startsWith('http') || to.startsWith('https');

  return (
    <a
      href={isExternal ? to : `/${to}`}
      className="btn btn-primary my-button"
    >
      {text}
    </a>
  );
};


export default MyButton;
