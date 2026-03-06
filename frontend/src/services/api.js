import axios from 'axios';

// Use the current domain/IP address of the window, so it works on any device in the network
const getBaseUrl = () => {
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  // If running in development or served from the same server, use the current hostname
  return `http://${window.location.hostname}:5000/api`;
};

const API_URL = getBaseUrl();

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      // Ensure headers object exists
      if (!config.headers) {
        config.headers = {};
      }

      // Use set method if available (Axios >= 1.x with AxiosHeaders)
      if (typeof config.headers.set === 'function') {
        config.headers.set('Authorization', `Bearer ${token}`);
      } else {
        config.headers['Authorization'] = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth APIs
export const register = async (email, password, full_name) => {
  const response = await api.post('/auth/register', {
    email,
    password,
    full_name
  });
  return response.data;
};

export const login = async (email, password) => {
  const response = await api.post('/auth/login', {
    email,
    password
  });
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

export const updateProfile = async (data) => {
  const response = await api.put('/auth/update-profile', data);
  return response.data;
};

export const changePassword = async (currentPassword, newPassword) => {
  const response = await api.post('/auth/change-password', {
    current_password: currentPassword,
    new_password: newPassword
  });
  return response.data;
};

// Dashboard APIs
export const getDashboardOverview = async (hours = 24) => {
  const response = await api.get(`/dashboard/overview?hours=${hours}`);
  return response.data;
};

export const getRealtimeMetrics = async () => {
  const response = await api.get('/dashboard/real-time-metrics');
  return response.data;
};

export const getAgentStatus = async () => {
  const response = await api.get('/dashboard/agent-status');
  return response.data;
};

// Traffic APIs
export const getTrafficStats = async (hours = 1) => {
  const response = await api.get(`/traffic/stats?hours=${hours}`);
  return response.data;
};

export const getLiveTraffic = async (limit = 20) => {
  const response = await api.get(`/traffic/live?limit=${limit}`);
  return response.data;
};

export const exportTrafficData = async (startDate, endDate) => {
  const response = await api.get('/traffic/export', {
    params: { start_date: startDate, end_date: endDate }
  });
  return response.data;
};

// Alerts APIs
export const getAlerts = async (params = {}) => {
  const response = await api.get('/alerts/', { params });
  return response.data;
};

export const acknowledgeAlert = async (alertId, notes) => {
  const response = await api.post(`/alerts/${alertId}/acknowledge`, { notes });
  return response.data;
};

export const resolveAlert = async (alertId, resolutionNotes) => {
  const response = await api.post(`/alerts/${alertId}/resolve`, { resolution_notes: resolutionNotes });
  return response.data;
};

export const getAlertsSummary = async (hours = 24) => {
  const response = await api.get(`/alerts/summary?hours=${hours}`);
  return response.data;
};

export default api;