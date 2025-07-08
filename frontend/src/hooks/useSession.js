import { useState, useEffect } from 'react';
import { createSession, getSession, generateDeviceId } from '../services/api';

export const useSession = () => {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    initializeSession();
  }, []);

  const initializeSession = async () => {
    try {
      setLoading(true);
      
      // Check if we have a stored session
      const storedSessionId = localStorage.getItem('ar_adventure_session_id');
      
      if (storedSessionId) {
        try {
          const existingSession = await getSession(storedSessionId);
          setSession(existingSession);
          setLoading(false);
          return;
        } catch (error) {
          console.log('Stored session not found, creating new one');
          localStorage.removeItem('ar_adventure_session_id');
        }
      }
      
      // Create new session
      const deviceId = generateDeviceId();
      const newSession = await createSession(deviceId);
      
      setSession(newSession);
      localStorage.setItem('ar_adventure_session_id', newSession.id);
      
    } catch (error) {
      console.error('Error initializing session:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const clearSession = () => {
    localStorage.removeItem('ar_adventure_session_id');
    setSession(null);
    initializeSession();
  };

  return {
    session,
    loading,
    error,
    clearSession,
    refreshSession: initializeSession
  };
};