import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';
import './My_Navbar.css'; // You'll add custom CSS here to make the design similar to SpaceX

const My_Navbar = () => {
  return (
    <Navbar expand="lg" className="custom-navbar" variant="dark">
      <Container fluid>
        {/* Logo */}
        {/* Toggle button for mobile */}
        <Navbar.Toggle aria-controls="navbar-nav" />
        <Navbar.Collapse id="navbar-nav">
          {/* Navigation Links */}
          <Nav className="ml-auto">
            <Nav.Link href="#home">Home</Nav.Link>
            <Nav.Link href="#falcon9">Game</Nav.Link>
            <Nav.Link href="#falconheavy">About</Nav.Link>
            <Nav.Link href="#starship">Setting</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default My_Navbar;
