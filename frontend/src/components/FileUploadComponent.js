// FileUploadComponent.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import config from '../config';

const API_BASE_URL = process.env.REACT_APP_API_URL || config.API_BASE_URL;
const API_URL = `${API_BASE_URL}/api/upload`;

const FileUploadComponent = ({ tableName, onUploadSuccess, onCancel }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) {
      onCancel(); // Если файл не выбран, скрываем форму
    } else {
      setFile(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('Пожалуйста, выберите файл.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploading(true);
      const response = await axios.post(`${API_URL}/${tableName}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setMessage(response.data.message);
      setUploading(false);
      
      if (response.data.status === 'success') {
        onUploadSuccess();
      }
    } catch (error) {
      setMessage('Ошибка при загрузке файла.');
      setUploading(false);
    }
  };

  return (
    <div className="file-upload-component">
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={uploading}>
        {uploading ? 'Загрузка...' : 'Загрузить'}
      </button>
      <button onClick={onCancel} disabled={uploading}>
        Отмена
      </button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default FileUploadComponent;
