import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import axios from "axios";
import ARScene from "./components/ARScene";
import MapUploader from "./components/MapUploader";
import { Toaster } from "./components/ui/sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const [currentView, setCurrentView] = useState('upload'); // 'upload' or 'ar'
  const [mapData, setMapData] = useState(null);

  const helloWorldApi = async () => {
    try {
      const response = await axios.get(`${API}/`);
      console.log(response.data.message);
    } catch (e) {
      console.error(e, `errored out requesting / api`);
    }
  };

  useEffect(() => {
    helloWorldApi();
  }, []);

  const handleMapUploaded = (uploadedMap) => {
    setMapData(uploadedMap);
    setCurrentView('ar');
  };

  const handleBackToUpload = () => {
    setCurrentView('upload');
    setMapData(null);
  };

  return (
    <div className="min-h-screen">
      {currentView === 'upload' && (
        <MapUploader onMapUploaded={handleMapUploaded} />
      )}
      {currentView === 'ar' && (
        <ARScene mapData={mapData} onBack={handleBackToUpload} />
      )}
      <Toaster />
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/ar" element={<ARScene />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;