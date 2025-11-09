import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const generateQuiz = async (url) => {
  const response = await api.post('/generate-quiz', { url });
  return response.data;
};

export const getQuizzes = async () => {
  const response = await api.get('/quizzes');
  return response.data;
};

export const getQuizDetails = async (quizId) => {
  const response = await api.get(`/quizzes/${quizId}`);
  return response.data;
};

export default api;