import React from 'react';

interface QuestionProps {
    question: string;
    options: string[];
    onAnswer: (answer: string) => void;
}

const Question: React.FC<QuestionProps> = ({ question, options, onAnswer }) => {
    return (
        <div>
            <h2>{question}</h2>
            <ul>
                {options.map((option, index) => (
                    <li key={index} onClick={() => onAnswer(option)}>
                        {option}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Question;