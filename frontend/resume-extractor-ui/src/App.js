import axios from 'axios';
import React, { useEffect, useState } from 'react';
import './App.css';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [expandedIndex, setExpandedIndex] = useState(null);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    console.log('File to upload:', file);
    console.log('API Base URL:', API_BASE);
    console.log('File type:', file.type);
    console.log('File size:', file.size);
    
    const formData = new FormData();
    formData.append('file', file);
    
    // Log the raw form data
    console.log('Form data:', formData);
    
    try {
      console.log('Starting upload...');
      const response = await axios.post(`${API_BASE}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          console.log('Upload progress:', Math.round((progressEvent.loaded / progressEvent.total) * 100), '%');
        }
      });
      console.log('Upload response:', response.data);
      setResult(response.data);
      fetchHistory();
    } catch (error) {
      console.error("Upload failed:", error.response?.data || error.message);
      console.error("Error details:", {
        status: error.response?.status,
        statusText: error.response?.statusText,
        headers: error.response?.headers,
        config: error.config
      });
      alert("Upload failed. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  const fetchHistory = async () => {
    try {
      const res = await axios.get('/history');
      setHistory(res.data);
    } catch (e) {
      console.error("Error loading history", e);
      console.error("History error details:", {
        status: e.response?.status,
        statusText: e.response?.statusText,
        headers: e.response?.headers,
        config: e.config
      });
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="container">
      <h1>Resume Skill Extractor</h1>

      <div className="upload-section">
        <input type="file" accept="application/pdf" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={!file || loading}>
          {loading ? "Processing..." : "Upload"}
        </button>
      </div>

      {result && (
        <div className="result-section">
          <h2>Latest Upload</h2>
          <DisplayResult data={result} />
        </div>
      )}

      <h2>Past Uploads</h2>
      <div className="history-section">
        {history.map((item, index) => (
          <div key={index} className="history-item">
            <button onClick={() => setExpandedIndex(index === expandedIndex ? null : index)}>
              {new Date(item.timestamp).toLocaleString()}
            </button>
            {expandedIndex === index && <DisplayResult data={item} />}
          </div>
        ))}
      </div>
    </div>
  );
}

function DisplayResult({ data }) {
  return (
    <div className="record">
      <p><strong>Name:</strong> {data.name}</p>
      <p><strong>Email:</strong> {data.email}</p>
      <p><strong>Phone:</strong> {data.phone}</p>
      <p><strong>Skills:</strong> {data.skills?.join(', ')}</p>
      <div>
        <strong>Experience:</strong>
        <ul>
          {data.experience?.map((exp, i) => (
            <li key={i}>{exp}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
