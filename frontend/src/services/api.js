import axios from 'axios';

const API_URL = '/api/tables';  // Относительный путь

// Функция для получения данных таблицы
export const fetchTableData = async (tableName, page = 1, size = 20, sortBy = [], filters = {}) => {
  const sortParams = sortBy.reduce((acc, sortField, index) => {
    acc[`sort_by${index + 1}`] = `${sortField.field} ${sortField.order}`;
    return acc;
  }, {});
  
  const filterString = JSON.stringify(filters);

  const response = await axios.get(`${API_URL}/${tableName}/data`, {
    params: { page, size, ...sortParams, filters: filterString }
  });

  return response.data;
};

// Функция для получения метаданных таблицы
export const fetchTableMetadata = async (tableName) => {
  const response = await axios.get(`${API_URL}/${tableName}/metadata`);
  return response.data;
};

// Функция для поиска
export const fetchTableSearchResults = async (tableName, query) => {
  const response = await axios.get(`${API_URL}/${tableName}/search`, {
    params: { query }
  });

  return response.data;
};
