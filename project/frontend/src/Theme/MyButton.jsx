import React from 'react';
import './MyButton.css';

const MyButton = ({ to, text }) => {
  const isExternal = to.startsWith('http') || to.startsWith('https');
  // console.log("dwadwadwa");
  return (
    <a
      href={isExternal ? to : `/${to}`}
      className="btn btn-primary btn-one"
    >
      {text}
    </a>
  );
};


export default MyButton;
