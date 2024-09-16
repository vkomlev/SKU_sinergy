import axios from 'axios';

const API_URL = '/api/tables';  // Относительный путь

export const fetchTableData = async (tableName, page = 1, size = 20, sortBy = [], filters = {}) => {
  // Преобразование массива сортировок в параметры вида sort_by1, sort_by2 и т.д.
  const sortParams = sortBy.reduce((acc, sortField, index) => {
    acc[`sort_by${index + 1}`] = `${sortField.field} ${sortField.order}`;  // Пример: id_dbs desc
    return acc;
  }, {});

  // Преобразование фильтров в строку
  const filterString = JSON.stringify(filters);

  const response = await axios.get(`${API_URL}/${tableName}/data`, {
    params: {
      page,
      size,
      ...sortParams,
      filters: filterString
    }
  });

  return response.data;  // Ожидаем, что сервер возвращает объект { data: [], total: ... }
};
