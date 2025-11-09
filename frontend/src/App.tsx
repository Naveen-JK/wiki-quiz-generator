import React from 'react';
import Quiz from './components/Quiz';
import './App.css';

const App: React.FC = () => {
  return (
    <div className="App">
      <h1>Wiki Quiz Generator</h1>
      <Quiz />
    </div>
  );
};

export default App;