import axios from 'axios';

// 👇 JUGAAD FIX:
// Hum direct server URL nahi use karenge.
// Hum '/api/proxy' use karenge jo Next.js rewrite ke through Render tak jayega.
const API_BASE_URL = '/api/proxy'; 

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  // Auth routes ke liye token ki zaroorat nahi
  if (token && !config.url?.includes('/auth/')) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Signup Function (JSON Data)
export const signup = (data: any) => {
    return apiClient.post('/auth/signup', {
        email: data.email,
        password: data.password,
        username: data.email
    });
};

// Login Function (JSON Data)
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