import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',  // Agora com /api/v1
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Interceptor para debug
api.interceptors.request.use(request => {
  console.log('📤 Requisição:', request.method?.toUpperCase(), request.url);
  return request;
});

api.interceptors.response.use(
  response => {
    console.log('📥 Resposta:', response.status, response.config.url);
    return response;
  },
  error => {
    console.error('❌ Erro:', error.message);
    if (error.response) {
      console.error('Status:', error.response.status);
      console.error('Dados:', error.response.data);
    }
    return Promise.reject(error);
  }
);

export { api };