// api.js
import axios from 'axios';

import config from '../config'; // Импортируем локальный конфиг

const API_BASE_URL = process.env.REACT_APP_API_URL || config.API_BASE_URL; // Используем переменную окружения в продакшн

const API_URL = `${API_BASE_URL}/api/tables`;  // Относительный путь

// Функция для получения данных таблицы
export const fetchTableData = async (tableName, page = 1, size = 20, sortBy = [], filters = {}) => {
  // Преобразование параметров сортировки в параметры для API
  const sortParams = sortBy.reduce((acc, sortField, index) => {
    acc[`sort_by${index + 1}`] = `${sortField.field} ${sortField.order}`;
    return acc;
  }, {});

  // Преобразование фильтров в строку
  const filterString = JSON.stringify(filters);

  console.log('API Request Params:', { tableName, page, size, sortParams, filterString });

  try {
    const response = await axios.get(`${API_URL}/${tableName}/data`, {
      params: {
        page,
        size,
        ...sortParams,  // Добавляем параметры сортировки
        filters: filterString  // Добавляем строку фильтров
      }
    });

    console.log('API Response:', response.data);

    return response.data;  // Предполагается, что сервер возвращает { data: [], total: number }
  } catch (error) {
    console.error('Ошибка загрузки данных таблицы:', error);
    throw error;
  }
};

// Функция для получения метаданных таблицы
export const fetchTableMetadata = async (tableName) => {
  try {
    const response = await axios.get(`${API_URL}/${tableName}/metadata`);
    console.log('API Metadata Response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Ошибка загрузки метаданных таблицы:', error);
    throw error;
  }
};

// Функция для поиска
export const fetchTableSearchResults = async (tableName, query) => {
  try {
    const response = await axios.get(`${API_URL}/${tableName}/search`, {
      params: { query }
    });

    console.log('API Search Response:', response.data);

    return response.data;  // Предполагается, что сервер возвращает { data: [], total: number }
  } catch (error) {
    console.error('Ошибка поиска по таблице:', error);
    throw error;
  }
};

export const saveRecord = async (tableName, data, isEditing) => {
  const url = isEditing
    ? `${API_URL}/${tableName}/records/${data.id}`
    : `${API_URL}/${tableName}/records`
  const method = isEditing ? 'PUT' : 'POST'
  const response = await axios({
    method,
    url,
    data,
  })
  return response.data
}

export const deleteRecord = async (tableName, recordId) => {
  const response = await axios.delete(`/api/tables/${tableName}/records/${recordId}`)
  return response.data
}

export const fetchLookupOptions = async (lookupTable) => {
  const response = await axios.get(`/api/tables/${lookupTable}/lookup`)
  return response.data
}

export const fetchRecord = async (tableName, recordId) => {
  const response = await axios.get(`/api/tables/${tableName}/records/${recordId}`)
  return response.data
}