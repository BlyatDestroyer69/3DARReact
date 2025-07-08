import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Upload, Map, Camera, CheckCircle } from 'lucide-react';

const MapUploader = ({ onMapUploaded }) => {
  const [dragActive, setDragActive] = useState(false);
  const [uploadedMap, setUploadedMap] = useState(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file) => {
    if (file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const mapData = {
          name: file.name,
          url: e.target.result,
          size: file.size,
          type: file.type
        };
        setUploadedMap(mapData);
        if (onMapUploaded) {
          onMapUploaded(mapData);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const useSampleMap = () => {
    const sampleMap = {
      name: 'Bukit Kiara Trail Map',
      url: '/api/sample-map', // This will be the provided map
      size: 'Sample',
      type: 'image/jpeg'
    };
    setUploadedMap(sampleMap);
    if (onMapUploaded) {
      onMapUploaded(sampleMap);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-800 to-green-800 flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl bg-white/90 backdrop-blur-sm shadow-2xl">
        <CardHeader className="text-center">
          <div className="mx-auto mb-4 p-3 bg-blue-100 rounded-full">
            <Map className="w-8 h-8 text-blue-600" />
          </div>
          <CardTitle className="text-3xl font-bold text-gray-800">AR Map Setup</CardTitle>
          <CardDescription className="text-gray-600">
            Upload your map image to create an AR adventure experience
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          
          {/* Sample Map Option */}
          <div className="p-4 bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-lg">
            <h3 className="font-semibold text-gray-800 mb-2 flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-green-600" />
              Quick Start with Sample Map
            </h3>
            <p className="text-sm text-gray-600 mb-3">
              Use the provided Bukit Kiara trail map to get started immediately
            </p>
            <Button 
              onClick={useSampleMap}
              className="w-full bg-green-600 hover:bg-green-700 text-white"
            >
              <Map className="w-4 h-4 mr-2" />
              Use Bukit Kiara Sample Map
            </Button>
          </div>

          {/* Upload Area */}
          <div 
            className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-all duration-200 ${
              dragActive 
                ? 'border-blue-400 bg-blue-50' 
                : 'border-gray-300 hover:border-gray-400'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              type="file"
              accept="image/*"
              onChange={handleFileInput}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />
            
            <div className="flex flex-col items-center gap-4">
              <div className="p-3 bg-gray-100 rounded-full">
                <Upload className="w-8 h-8 text-gray-600" />
              </div>
              <div>
                <p className="text-lg font-semibold text-gray-800">
                  Drop your map image here
                </p>
                <p className="text-sm text-gray-600 mt-1">
                  or click to browse files
                </p>
              </div>
              <div className="flex gap-2">
                <Badge variant="outline">JPG</Badge>
                <Badge variant="outline">PNG</Badge>
                <Badge variant="outline">GIF</Badge>
              </div>
            </div>
          </div>

          {/* Uploaded Map Preview */}
          {uploadedMap && (
            <div className="p-4 bg-gray-50 rounded-lg">
              <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-green-600" />
                Map Ready for AR
              </h3>
              <div className="bg-white rounded-lg p-3 shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-gray-800">{uploadedMap.name}</p>
                    <p className="text-sm text-gray-500">
                      {typeof uploadedMap.size === 'number' 
                        ? `${(uploadedMap.size / 1024 / 1024).toFixed(2)} MB` 
                        : uploadedMap.size}
                    </p>
                  </div>
                  <Badge className="bg-green-100 text-green-800">
                    Ready
                  </Badge>
                </div>
              </div>
            </div>
          )}

          {/* Instructions */}
          <div className="space-y-3">
            <h3 className="font-semibold text-gray-800">How it works:</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg">
                <div className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">1</div>
                <div>
                  <p className="font-medium text-gray-800">Upload Map</p>
                  <p className="text-sm text-gray-600">Choose your trail map image</p>
                </div>
              </div>
              <div className="flex items-start gap-3 p-3 bg-purple-50 rounded-lg">
                <div className="flex-shrink-0 w-6 h-6 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold">2</div>
                <div>
                  <p className="font-medium text-gray-800">Scan Map</p>
                  <p className="text-sm text-gray-600">Point camera at the map</p>
                </div>
              </div>
              <div className="flex items-start gap-3 p-3 bg-green-50 rounded-lg">
                <div className="flex-shrink-0 w-6 h-6 bg-green-600 text-white rounded-full flex items-center justify-center text-sm font-bold">3</div>
                <div>
                  <p className="font-medium text-gray-800">Explore AR</p>
                  <p className="text-sm text-gray-600">Discover interactive checkpoints</p>
                </div>
              </div>
            </div>
          </div>

          {/* Action Button */}
          {uploadedMap && (
            <Button 
              onClick={() => onMapUploaded && onMapUploaded(uploadedMap)}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white"
              size="lg"
            >
              <Camera className="w-5 h-5 mr-2" />
              Start AR Adventure
            </Button>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default MapUploader;