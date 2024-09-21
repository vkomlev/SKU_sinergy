// api.js
import axios from 'axios';
import config from '../config';

const API_BASE_URL = process.env.REACT_APP_API_URL || config.API_BASE_URL;
const API_URL = `${API_BASE_URL}/api/tables`;

const apiRequest = async (method, url, data = null, params = {}) => {
  try {
    const response = await axios({ method, url, data, params });
    return response.data;
  } catch (error) {
    console.error(`Ошибка API (${method} ${url}):`, error);
    throw error;
  }
};

// Используем базовую функцию для всех запросов
export const fetchTableData = async (tableName, page = 1, size = 20, sortBy = [], filters = {}) => {
  const sortParams = sortBy.reduce((acc, sortField, index) => {
    acc[`sort_by${index + 1}`] = `${sortField.field} ${sortField.order}`;
    return acc;
  }, {});
  const filterString = JSON.stringify(filters);
  return apiRequest('GET', `${API_URL}/${tableName}/data`, null, { page, size, ...sortParams, filters: filterString });
};

export const fetchTableMetadata = async (tableName) => apiRequest('GET', `${API_URL}/${tableName}/metadata`);

export const fetchTableSearchResults = async (tableName, query) => apiRequest('GET', `${API_URL}/${tableName}/search`, null, { query });

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
