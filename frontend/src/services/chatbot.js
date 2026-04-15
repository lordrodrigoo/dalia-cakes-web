import api from './api'

export const sendMessage = (message, sessionId) =>
  api.post('/chatbot/message', { message, session_id: sessionId })
