import React, { useState } from 'react';
import './QuizDisplay.css';

const QuizDisplay = ({ quizData, isTakeQuizMode = false }) => {
  const [userAnswers, setUserAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);

  const handleAnswerSelect = (questionIndex, answer) => {
    if (!submitted) {
      setUserAnswers(prev => ({
        ...prev,
        [questionIndex]: answer
      }));
    }
  };

  const calculateScore = () => {
    return quizData.quiz.reduce((score, question, index) => {
      return score + (userAnswers[index] === question.answer ? 1 : 0);
    }, 0);
  };

  const handleSubmit = () => {
    setSubmitted(true);
  };

  const resetQuiz = () => {
    setUserAnswers({});
    setSubmitted(false);
  };

  return (
    <div className="quiz-display">
      <div className="quiz-header">
        <h3>Generated Quiz ({quizData.quiz?.length || 0} questions)</h3>
        {isTakeQuizMode && !submitted && (
          <button onClick={handleSubmit} className="submit-btn">
            Submit Answers
          </button>
        )}
        {isTakeQuizMode && submitted && (
          <div className="score-display">
            Score: {calculateScore()} / {quizData.quiz?.length || 0}
            <button onClick={resetQuiz} className="retry-btn">
              Try Again
            </button>
          </div>
        )}
      </div>

      <div className="questions-container">
        {quizData.quiz?.map((question, index) => (
          <div key={index} className="question-card">
            <div className="question-header">
              <h4>Q{index + 1}: {question.question}</h4>
              <span className={`difficulty-badge ${question.difficulty}`}>
                {question.difficulty}
              </span>
            </div>
            
            <div className="options-container">
              {question.options?.map((option, optIndex) => {
                const optionLetter = String.fromCharCode(65 + optIndex);
                const isSelected = userAnswers[index] === optionLetter;
                const isCorrect = optionLetter === question.answer;
                const showAnswer = submitted && isTakeQuizMode;
                
                return (
                  <div 
                    key={optIndex}
                    className={`option ${isSelected ? 'selected' : ''} 
                      ${showAnswer ? (isCorrect ? 'correct' : (isSelected ? 'incorrect' : '')) : ''}`}
                    onClick={() => !submitted && handleAnswerSelect(index, optionLetter)}
                  >
                    <span className="option-letter">{optionLetter}.</span>
                    <span className="option-text">{option}</span>
                    {showAnswer && isCorrect && <span className="correct-mark">✓</span>}
                    {showAnswer && isSelected && !isCorrect && <span className="incorrect-mark">✗</span>}
                  </div>
                );
              })}
            </div>

            {(submitted || !isTakeQuizMode) && (
              <div className="answer-explanation">
                <p><strong>Correct Answer:</strong> {question.answer}. {question.options?.[question.answer.charCodeAt(0) - 65]}</p>
                <p><strong>Explanation:</strong> {question.explanation}</p>
              </div>
            )}
          </div>
        ))}
      </div>

      {quizData.related_topics && quizData.related_topics.length > 0 && (
        <div className="related-topics">
          <h4>Related Topics for Further Reading</h4>
          <div className="topics-list">
            {quizData.related_topics.map((topic, index) => (
              <span key={index} className="topic-tag">{topic}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default QuizDisplay;