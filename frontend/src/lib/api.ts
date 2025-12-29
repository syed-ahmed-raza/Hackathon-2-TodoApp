import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json', // ✅ Default JSON
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token && !config.url?.includes('/auth/')) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 👇 FIX: Ab hum clean JSON bhej rahe hain (No URLSearchParams)
export const signup = (data: any) => {
    return apiClient.post('/auth/signup', {
        email: data.email,
        password: data.password,
        username: data.email // Backend compatibility ke liye dono bhej diye
    });
};

export const login = (data: any) => {
    return apiClient.post('/auth/login', {
        email: data.email,
        password: data.password,
        username: data.email
    });
};

export const getTasks = () => apiClient.get('/tasks');
export const addTask = (data: any) => apiClient.post('/tasks', data);
export const updateTask = (id: number, data: any) => apiClient.put(`/tasks/${id}`, data);
export const deleteTask = (id: number) => apiClient.delete(`/tasks/${id}`);