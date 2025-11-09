import React, { useState } from 'react';
import { generateQuiz } from '../services/api';
import QuizDisplay from './QuizDisplay';
import './GenerateQuiz.css';

const GenerateQuiz = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [quizData, setQuizData] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setQuizData(null);

    try {
      const data = await generateQuiz(url);
      setQuizData(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate quiz');
    } finally {
      setLoading(false);
    }
  };

  const previewArticle = () => {
    if (url) {
      window.open(url, '_blank');
    }
  };

  return (
    <div className="generate-quiz">
      <div className="input-section">
        <h2>Generate New Quiz</h2>
        <form onSubmit={handleSubmit} className="url-form">
          <div className="input-group">
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Enter Wikipedia URL (e.g., https://en.wikipedia.org/wiki/Alan_Turing)"
              required
              className="url-input"
            />
            <button 
              type="button" 
              onClick={previewArticle}
              disabled={!url}
              className="preview-btn"
            >
              Preview
            </button>
          </div>
          <button 
            type="submit" 
            disabled={loading || !url}
            className="generate-btn"
          >
            {loading ? 'Generating Quiz...' : 'Generate Quiz'}
          </button>
        </form>

        {error && <div className="error-message">{error}</div>}
      </div>

      {quizData && (
        <div className="quiz-result">
          <div className="article-header">
            <h2>{quizData.title}</h2>
            <p className="summary">{quizData.summary}</p>
            <div className="article-meta">
              <span><strong>Sections:</strong> {quizData.sections?.join(', ')}</span>
            </div>
          </div>
          
          <QuizDisplay quizData={quizData} />
        </div>
      )}
    </div>
  );
};

export default GenerateQuiz;