import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const location = useLocation();

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          📚 WikiQuiz
        </Link>
        
        <div className="nav-menu">
          <Link 
            to="/" 
            className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
          >
            Home
          </Link>
          <Link 
            to="/generate" 
            className={`nav-link ${location.pathname === '/generate' ? 'active' : ''}`}
          >
            Generate Quiz
          </Link>
          <Link 
            to="/history" 
            className={`nav-link ${location.pathname === '/history' ? 'active' : ''}`}
          >
            Past Quizzes
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;