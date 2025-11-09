import React, { useState, useEffect } from 'react';
import { getQuizzes } from '../services/api';
import QuizDisplay from './QuizDisplay';
import './PastQuizzes.css';

const PastQuizzes = () => {
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedQuiz, setSelectedQuiz] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchQuizzes();
  }, []);

  const fetchQuizzes = async () => {
    try {
      const data = await getQuizzes();
      setQuizzes(data);
    } catch (error) {
      console.error('Failed to fetch quizzes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetails = async (quiz) => {
    setSelectedQuiz(quiz);
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedQuiz(null);
  };

  if (loading) {
    return <div className="loading">Loading past quizzes...</div>;
  }

  return (
    <div className="past-quizzes">
      <h2>Quiz History</h2>
      
      {quizzes.length === 0 ? (
        <div className="no-quizzes">
          <p>No quizzes generated yet. Go to "Generate Quiz" to create your first quiz!</p>
        </div>
      ) : (
        <div className="quizzes-table-container">
          <table className="quizzes-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Title</th>
                <th>URL</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {quizzes.map(quiz => (
                <tr key={quiz.id}>
                  <td>{quiz.id}</td>
                  <td className="title-cell">{quiz.title}</td>
                  <td className="url-cell">
                    <a href={quiz.url} target="_blank" rel="noopener noreferrer">
                      {quiz.url}
                    </a>
                  </td>
                  <td>{new Date(quiz.created_at).toLocaleDateString()}</td>
                  <td>
                    <button 
                      onClick={() => handleViewDetails(quiz)}
                      className="details-btn"
                    >
                      Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showModal && selectedQuiz && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{selectedQuiz.title}</h3>
              <button className="close-btn" onClick={closeModal}>×</button>
            </div>
            <div className="modal-body">
              <QuizDisplay quizData={selectedQuiz} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PastQuizzes;