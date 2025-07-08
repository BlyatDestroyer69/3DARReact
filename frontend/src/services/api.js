import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Session Management
export const createSession = async (deviceId) => {
  try {
    const response = await axios.post(`${API}/sessions`, null, {
      params: { device_id: deviceId }
    });
    return response.data;
  } catch (error) {
    console.error('Error creating session:', error);
    throw error;
  }
};

export const getSession = async (sessionId) => {
  try {
    const response = await axios.get(`${API}/sessions/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('Error getting session:', error);
    throw error;
  }
};

// Plant Management
export const getPlants = async () => {
  try {
    const response = await axios.get(`${API}/plants`);
    return response.data;
  } catch (error) {
    console.error('Error fetching plants:', error);
    throw error;
  }
};

export const getPlant = async (plantId) => {
  try {
    const response = await axios.get(`${API}/plants/${plantId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching plant:', error);
    throw error;
  }
};

// Checkpoint Management
export const getCheckpoints = async (trailId = null, sessionId = null) => {
  try {
    const params = {};
    if (trailId) params.trail_id = trailId;
    if (sessionId) params.session_id = sessionId;
    
    const response = await axios.get(`${API}/checkpoints`, { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching checkpoints:', error);
    throw error;
  }
};

export const getCheckpoint = async (checkpointId, sessionId = null) => {
  try {
    const params = {};
    if (sessionId) params.session_id = sessionId;
    
    const response = await axios.get(`${API}/checkpoints/${checkpointId}`, { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching checkpoint:', error);
    throw error;
  }
};

// Discovery System
export const discoverCheckpoint = async (sessionId, checkpointId) => {
  try {
    const response = await axios.post(`${API}/discoveries`, null, {
      params: { 
        session_id: sessionId,
        checkpoint_id: checkpointId 
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error discovering checkpoint:', error);
    throw error;
  }
};

// Achievement System
export const getAchievements = async () => {
  try {
    const response = await axios.get(`${API}/achievements`);
    return response.data;
  } catch (error) {
    console.error('Error fetching achievements:', error);
    throw error;
  }
};

// Progress Tracking
export const getProgress = async (sessionId) => {
  try {
    const response = await axios.get(`${API}/progress/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching progress:', error);
    throw error;
  }
};

// Trail Management
export const getTrails = async () => {
  try {
    const response = await axios.get(`${API}/trails`);
    return response.data;
  } catch (error) {
    console.error('Error fetching trails:', error);
    throw error;
  }
};

export const getTrail = async (trailId) => {
  try {
    const response = await axios.get(`${API}/trails/${trailId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching trail:', error);
    throw error;
  }
};

// Map Management
export const uploadMap = async (name, trailId, file) => {
  try {
    const formData = new FormData();
    formData.append('name', name);
    formData.append('trail_id', trailId);
    formData.append('file', file);
    
    const response = await axios.post(`${API}/maps`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading map:', error);
    throw error;
  }
};

export const getMap = async (trailId) => {
  try {
    const response = await axios.get(`${API}/maps/${trailId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching map:', error);
    throw error;
  }
};

// Settings Management
export const getSettings = async (sessionId) => {
  try {
    const response = await axios.get(`${API}/settings/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching settings:', error);
    throw error;
  }
};

export const updateSettings = async (sessionId, settings) => {
  try {
    const response = await axios.put(`${API}/settings/${sessionId}`, settings);
    return response.data;
  } catch (error) {
    console.error('Error updating settings:', error);
    throw error;
  }
};

// Helper function to generate device ID
export const generateDeviceId = () => {
  return `device_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
};

// Health check
export const healthCheck = async () => {
  try {
    const response = await axios.get(`${API}/health`);
    return response.data;
  } catch (error) {
    console.error('Error checking health:', error);
    throw error;
  }
};