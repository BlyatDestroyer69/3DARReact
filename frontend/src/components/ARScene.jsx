import React, { useEffect, useRef, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { X, Camera, Info, Leaf, TreePine, Flower2, Scan, MapPin } from 'lucide-react';

const ARScene = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [selectedCheckpoint, setSelectedCheckpoint] = useState(null);
  const [arStarted, setArStarted] = useState(false);
  const [cameraPermission, setCameraPermission] = useState(null);
  const [mapDetected, setMapDetected] = useState(false);
  const [scanning, setScanning] = useState(false);

  const checkpoints = [
    {
      id: 1,
      name: "Fern Valley",
      position: { x: 20, y: 25 },
      plant: {
        name: "Bird's Nest Fern",
        scientific: "Asplenium nidus",
        description: "A large epiphytic fern native to tropical regions. Its distinctive nest-like shape helps collect water and organic debris.",
        facts: ["Can grow up to 1.5 meters wide", "Epiphytic - grows on other plants", "Popular as houseplant"],
        rarity: "Common"
      },
      color: "#22c55e"
    },
    {
      id: 2,
      name: "Bamboo Grove",
      position: { x: 70, y: 40 },
      plant: {
        name: "Giant Bamboo",
        scientific: "Dendrocalamus giganteus",
        description: "One of the largest bamboo species in the world. It can grow extremely fast and is used for construction.",
        facts: ["Can grow up to 3 feet per day", "Reaches heights of 100+ feet", "Stronger than steel in tensile strength"],
        rarity: "Uncommon"
      },
      color: "#eab308"
    },
    {
      id: 3,
      name: "Orchid Point",
      position: { x: 45, y: 15 },
      plant: {
        name: "Wild Orchid",
        scientific: "Vanda hookeriana",
        description: "A beautiful epiphytic orchid species endemic to Southeast Asia. Known for its fragrant flowers.",
        facts: ["Blooms year-round", "Requires high humidity", "Protected species"],
        rarity: "Rare"
      },
      color: "#a855f7"
    },
    {
      id: 4,
      name: "Dipterocarp Trail",
      position: { x: 35, y: 60 },
      plant: {
        name: "Meranti Tree",
        scientific: "Shorea sp.",
        description: "A tall tropical hardwood tree, part of the dipterocarp family. Important for timber and ecosystem.",
        facts: ["Can live over 100 years", "Provides canopy shelter", "Seeds have wing-like structures"],
        rarity: "Common"
      },
      color: "#dc2626"
    },
    {
      id: 5,
      name: "Pitcher Plant Bog",
      position: { x: 80, y: 70 },
      plant: {
        name: "Tropical Pitcher Plant",
        scientific: "Nepenthes rafflesiana",
        description: "A carnivorous plant with modified leaves that form pitcher-shaped traps to catch insects.",
        facts: ["Carnivorous plant", "Pitchers can hold 200ml of water", "Endemic to Southeast Asia"],
        rarity: "Rare"
      },
      color: "#f59e0b"
    }
  ];

  useEffect(() => {
    if (arStarted) {
      startCamera();
    }
  }, [arStarted]);

  useEffect(() => {
    if (mapDetected) {
      // Simulate map detection after 3 seconds
      const timer = setTimeout(() => {
        setMapDetected(true);
        setScanning(false);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [scanning]);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment' }
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
      
      // Simulate map detection
      setScanning(true);
      setTimeout(() => {
        setMapDetected(true);
        setScanning(false);
      }, 3000);
      
    } catch (error) {
      console.error('Error accessing camera:', error);
      setCameraPermission(false);
    }
  };

  const requestCameraPermission = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      setCameraPermission(true);
      setArStarted(true);
      // Stop the stream as we'll restart it in AR mode
      stream.getTracks().forEach(track => track.stop());
    } catch (error) {
      console.error('Camera permission denied:', error);
      setCameraPermission(false);
    }
  };

  const getRarityColor = (rarity) => {
    switch (rarity) {
      case 'Common': return 'bg-green-500';
      case 'Uncommon': return 'bg-yellow-500';
      case 'Rare': return 'bg-purple-500';
      default: return 'bg-gray-500';
    }
  };

  const getPlantIcon = (name) => {
    if (name.includes('Fern')) return <Leaf className="w-4 h-4" />;
    if (name.includes('Bamboo') || name.includes('Tree')) return <TreePine className="w-4 h-4" />;
    if (name.includes('Orchid') || name.includes('Pitcher')) return <Flower2 className="w-4 h-4" />;
    return <Leaf className="w-4 h-4" />;
  };

  if (!arStarted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-900 via-green-800 to-green-700 flex items-center justify-center p-4">
        <Card className="w-full max-w-md bg-white/90 backdrop-blur-sm shadow-2xl">
          <CardHeader className="text-center">
            <div className="mx-auto mb-4 p-3 bg-green-100 rounded-full">
              <Camera className="w-8 h-8 text-green-600" />
            </div>
            <CardTitle className="text-2xl font-bold text-green-800">AR Adventure</CardTitle>
            <CardDescription className="text-green-600">
              Explore Bukit Kiara's flora in augmented reality
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="text-center text-sm text-gray-600">
              <p className="mb-2">🗺️ Point your camera at the Bukit Kiara map</p>
              <p className="mb-2">🌿 Discover interactive plant checkpoints</p>
              <p className="mb-4">📱 Works on mobile and desktop</p>
            </div>
            
            {cameraPermission === false && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-700 text-sm">
                  Camera access is required for AR experience. Please enable camera permission.
                </p>
              </div>
            )}
            
            <Button 
              onClick={requestCameraPermission} 
              className="w-full bg-green-600 hover:bg-green-700 text-white"
              size="lg"
            >
              <Camera className="w-5 h-5 mr-2" />
              Start AR Experience
            </Button>
            
            <div className="text-xs text-gray-500 text-center">
              Make sure you have good lighting and hold the map steady
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="relative w-full h-screen bg-black overflow-hidden">
      {/* Camera Feed */}
      <video
        ref={videoRef}
        className="absolute inset-0 w-full h-full object-cover"
        autoPlay
        playsInline
        muted
      />
      
      {/* AR Overlay Canvas */}
      <canvas
        ref={canvasRef}
        className="absolute inset-0 w-full h-full pointer-events-none"
      />
      
      {/* UI Overlay */}
      <div className="absolute top-4 left-4 right-4 z-20 flex justify-between items-start">
        <div className="bg-black/50 backdrop-blur-sm rounded-lg p-3">
          <h1 className="text-white font-bold text-lg">AR Adventure</h1>
          <p className="text-white/80 text-sm">
            {scanning ? 'Scanning map...' : mapDetected ? 'Map detected!' : 'Point at the map'}
          </p>
        </div>
        
        <Button
          onClick={() => setArStarted(false)}
          variant="secondary"
          size="sm"
          className="bg-black/50 backdrop-blur-sm hover:bg-black/70 text-white border-white/20"
        >
          <X className="w-4 h-4" />
        </Button>
      </div>
      
      {/* Scanning Indicator */}
      {scanning && (
        <div className="absolute inset-0 flex items-center justify-center z-10">
          <div className="bg-black/50 backdrop-blur-sm rounded-lg p-6 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto mb-3"></div>
            <p className="text-white text-sm">Scanning for map...</p>
          </div>
        </div>
      )}
      
      {/* Scanning Frame */}
      {scanning && (
        <div className="absolute inset-0 flex items-center justify-center z-10 pointer-events-none">
          <div className="border-2 border-white/50 rounded-lg w-80 h-60 relative">
            <div className="absolute top-0 left-0 w-6 h-6 border-t-4 border-l-4 border-green-400 rounded-tl-lg"></div>
            <div className="absolute top-0 right-0 w-6 h-6 border-t-4 border-r-4 border-green-400 rounded-tr-lg"></div>
            <div className="absolute bottom-0 left-0 w-6 h-6 border-b-4 border-l-4 border-green-400 rounded-bl-lg"></div>
            <div className="absolute bottom-0 right-0 w-6 h-6 border-b-4 border-r-4 border-green-400 rounded-br-lg"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <Scan className="w-8 h-8 text-white/70 animate-pulse" />
            </div>
          </div>
        </div>
      )}
      
      {/* AR Checkpoints Overlay */}
      {mapDetected && (
        <div className="absolute inset-0 z-15 pointer-events-none">
          {checkpoints.map((checkpoint) => (
            <div
              key={checkpoint.id}
              className="absolute pointer-events-auto cursor-pointer transform -translate-x-1/2 -translate-y-1/2"
              style={{
                left: `${checkpoint.position.x}%`,
                top: `${checkpoint.position.y}%`,
              }}
              onClick={() => setSelectedCheckpoint(checkpoint)}
            >
              <div className="relative">
                {/* Animated pulse ring */}
                <div 
                  className="absolute inset-0 rounded-full animate-ping"
                  style={{ backgroundColor: checkpoint.color + '40' }}
                ></div>
                
                {/* Main checkpoint marker */}
                <div 
                  className="w-12 h-12 rounded-full shadow-lg border-2 border-white flex items-center justify-center relative z-10"
                  style={{ backgroundColor: checkpoint.color }}
                >
                  <MapPin className="w-6 h-6 text-white" />
                </div>
                
                {/* Checkpoint label */}
                <div className="absolute top-14 left-1/2 transform -translate-x-1/2 whitespace-nowrap">
                  <div className="bg-black/80 backdrop-blur-sm text-white px-2 py-1 rounded text-xs font-medium">
                    {checkpoint.name}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
      
      {/* Instructions */}
      <div className="absolute bottom-4 left-4 right-4 z-20">
        <div className="bg-black/50 backdrop-blur-sm rounded-lg p-3 text-center">
          <p className="text-white text-sm">
            {!mapDetected ? (
              <>🎯 Point camera at the Bukit Kiara map to reveal checkpoints</>
            ) : (
              <>👆 Tap the colored pins to discover plants • 🌿 {checkpoints.length} species to find</>
            )}
          </p>
        </div>
      </div>
      
      {/* Checkpoint Information Modal */}
      {selectedCheckpoint && (
        <div className="absolute inset-0 z-30 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
          <Card className="w-full max-w-lg bg-white shadow-2xl">
            <CardHeader className="pb-3">
              <div className="flex justify-between items-start">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    {getPlantIcon(selectedCheckpoint.plant.name)}
                    <CardTitle className="text-lg">{selectedCheckpoint.plant.name}</CardTitle>
                    <Badge className={`${getRarityColor(selectedCheckpoint.plant.rarity)} text-white`}>
                      {selectedCheckpoint.plant.rarity}
                    </Badge>
                  </div>
                  <CardDescription className="italic text-sm">
                    {selectedCheckpoint.plant.scientific}
                  </CardDescription>
                </div>
                <Button
                  onClick={() => setSelectedCheckpoint(null)}
                  variant="ghost"
                  size="sm"
                  className="text-gray-500 hover:text-gray-700"
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-semibold text-gray-800 mb-2 flex items-center gap-2">
                  <Info className="w-4 h-4" />
                  About This Plant
                </h4>
                <p className="text-gray-600 text-sm leading-relaxed">
                  {selectedCheckpoint.plant.description}
                </p>
              </div>
              
              <div>
                <h4 className="font-semibold text-gray-800 mb-2">Interesting Facts</h4>
                <ul className="space-y-1">
                  {selectedCheckpoint.plant.facts.map((fact, index) => (
                    <li key={index} className="text-sm text-gray-600 flex items-start gap-2">
                      <span className="text-green-500 mt-1">•</span>
                      {fact}
                    </li>
                  ))}
                </ul>
              </div>
              
              <div className="pt-2 border-t">
                <p className="text-xs text-gray-500 text-center">
                  Checkpoint: {selectedCheckpoint.name}
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default ARScene;