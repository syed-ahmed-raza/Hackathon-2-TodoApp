
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  console.log('Token:', token);
  if (token && !config.url?.includes('/auth/')) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const signup = (data: any) => {
    const params = new URLSearchParams();
    params.append('username', data.email);
    params.append('password', data.password);

    return apiClient.post('/auth/signup', params, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    });
};

export const login = (data: any) => {
    const params = new URLSearchParams();
    params.append('username', data.email);
    params.append('password', data.password);

    return apiClient.post('/auth/login', params, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    });
};

export const getTasks = () => apiClient.get('/tasks');
export const addTask = (data: any) => apiClient.post('/tasks', data);
export const updateTask = (id: number, data: any) => apiClient.put(`/tasks/${id}`, data);
export const deleteTask = (id: number) => apiClient.delete(`/tasks/${id}`);
