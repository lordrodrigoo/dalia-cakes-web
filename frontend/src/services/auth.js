import api from './api';

// Função para login (POST /api/v1/auth/login)
export async function login(username, password) {
  const response = await api.post('/auth/login', { username, password });
  return response.data; // { access_token, refresh_token, ... }
}

// Função para salvar token (pode ser adaptada para context ou redux)
export function saveToken(token) {
  localStorage.setItem('access_token', token);
}

export function getToken() {
  return localStorage.getItem('access_token');
}

export function logout() {
  localStorage.removeItem('access_token');
}
