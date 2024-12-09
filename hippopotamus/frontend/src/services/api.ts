import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = async (username: string, password: string) => {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);
  
  const response = await axios.post(`${API_URL}/token`, formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    withCredentials: true
  });
  
  return response.data;
};

export const register = async (username: string, password: string) => {
  const response = await api.post('/register', { username, password });
  return response.data;
};

export const tapHippo = async (amount: number) => {
  const response = await api.post('/tap-hippo', { amount });
  return response.data;
};

export const getShopItems = async () => {
  const response = await api.get('/items');
  return response.data;
};

export const buyItem = async (itemId: number) => {
  const response = await api.post(`/buy/${itemId}`);
  return response.data;
};

export const getUserProfile = async () => {
  const response = await api.get('/me');
  return response.data;
};

export const getBalance = async () => {
  const response = await api.get('/balance');
  return response.data;
};

export const generateVerificationCode = async () => {
  const response = await api.post('/generate-verification-code');
  return response.data;
};

export const unlinkTelegram = async () => {
  const response = await api.post('/unlink-telegram');
  return response.data;
};

export const donate = async () => {
  const response = await api.post('/donate');
  return response.data;
};

export const sellItem = async (purchaseId: number) => {
  const response = await api.post(`/sell/${purchaseId}`);
  return response.data;
};

export const getUserPurchases = async () => {
  const response = await api.get('/my-purchases');
  return response.data;
};

export const getCurrentElection = async () => {
  const response = await api.get('/election/current');
  return response.data;
};


export const nominateCandidate = async (name: string) => {
  const response = await api.post(`/election/nominate?name=${encodeURIComponent(name)}`);
  return response.data;
};

export const voteForCandidate = async (candidateId: number) => {
  const response = await api.post(`/election/vote/${candidateId}`);
  return response.data;
};

export default api; 