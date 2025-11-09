import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="home-page">
      <div className="hero-section">
        <div className="hero-content">
          <h1>Transform Wikipedia into Interactive Quizzes</h1>
          <p>AI-powered quiz generation from any Wikipedia article. Learn while having fun!</p>
          <div className="hero-buttons">
            <Link to="/generate" className="btn btn-primary">
              Generate Your First Quiz
            </Link>
            <Link to="/history" className="btn btn-secondary">
              View Past Quizzes
            </Link>
          </div>
        </div>
        <div className="hero-image">
          <div className="feature-card">
            <h3>🚀 Instant Generation</h3>
            <p>Get quizzes in seconds using advanced AI</p>
          </div>
          <div className="feature-card">
            <h3>📚 Learn Efficiently</h3>
            <p>Reinforce knowledge with targeted questions</p>
          </div>
          <div className="feature-card">
            <h3>💾 Save History</h3>
            <p>Access all your generated quizzes anytime</p>
          </div>
        </div>
      </div>

      <div className="features-section">
        <h2>How It Works</h2>
        <div className="features-grid">
          <div className="feature-step">
            <div className="step-number">1</div>
            <h3>Paste Wikipedia URL</h3>
            <p>Copy and paste any Wikipedia article URL you want to learn about</p>
          </div>
          <div className="feature-step">
            <div className="step-number">2</div>
            <h3>AI Generates Quiz</h3>
            <p>Our AI reads the article and creates relevant questions automatically</p>
          </div>
          <div className="feature-step">
            <div className="step-number">3</div>
            <h3>Test Your Knowledge</h3>
            <p>Take the quiz and get instant feedback with explanations</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;