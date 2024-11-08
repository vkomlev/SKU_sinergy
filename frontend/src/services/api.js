// api.js
import axios from 'axios';
import config from '../config';

const API_BASE_URL = process.env.REACT_APP_API_URL || config.API_BASE_URL;
const API_URL = `${API_BASE_URL}/api/tables`;

const apiRequest = async (method, url, data = null, params = {}, showView = false) => {
  try {
    // Добавляем параметр showview, если он установлен
    const finalParams = showView ? { ...params, showview: true } : params;

    const response = await axios({ method, url, data, params: finalParams });
    return response.data;
  } catch (error) {
    console.error(`Ошибка API (${method} ${url}):`, error);
    throw error;
  }
};

// Используем базовую функцию для всех запросов
// В запросы метаданных и данных для отображения добавляем параметр showview = true
export const fetchTableData = async (tableName, page = 1, size = 20, sortBy = [], filters = {}, showView = false) => {
  const sortParams = sortBy.reduce((acc, sortField, index) => {
    acc[`sort_by${index + 1}`] = `${sortField.field} ${sortField.order}`;
    return acc;
  }, {});
  const filterString = JSON.stringify(filters);
  return apiRequest('GET', `${API_URL}/${tableName}/data`, null, { page, size, ...sortParams, filters: filterString }, showView);
};

export const fetchTableMetadata = async (tableName, showView = false) => apiRequest('GET', `${API_URL}/${tableName}/metadata`, null, {}, showView);

export const fetchTableSearchResults = async (tableName, query, showView = true) => apiRequest('GET', `${API_URL}/${tableName}/search`, null, { query }, showView);

export const saveRecord = async (tableName, data, isEditing, recordId) => {
  const url = isEditing ? `${API_URL}/${tableName}/records/${recordId}` : `${API_URL}/${tableName}/records`;
  const method = isEditing ? 'PUT' : 'POST';
  return apiRequest(method, url, data);
};

export const deleteRecord = async (tableName, recordId) => apiRequest('DELETE', `${API_URL}/${tableName}/records/${recordId}`);


export const fetchLookupOptions = async (lookupTable) => {
  const response = await axios.get(`${API_URL}/${lookupTable}/lookup`)
  return response.data
}

export const fetchRecord = async (tableName, recordId) => apiRequest('GET', `${API_URL}/${tableName}/records/${recordId}`);

// Обновленная функция в frontend\src\services\api.js
export const runRScript = async (scriptPath) => {
  const url = `${API_BASE_URL}/api/run-r-script?path=${encodeURIComponent(scriptPath)}`; // Добавляем параметры в строку запроса
  try {
    const response = await axios.post(url); // Используем метод GET
    return response.data;
  } catch (error) {
    console.error(`Ошибка при запуске R-скрипта (${scriptPath}):`, error);
    throw error;
  }
};

