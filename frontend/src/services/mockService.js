import mockData from '../mock/Import_DBS_Delivery_Data.json';  // Данные таблицы
import mockMetadata from '../mock/Import_DBS_Delivery_Metadata.json';  // Метаданные таблицы

// Функция для фильтрации данных
const applyFilters = (data, filters) => {
  if (!filters) return data;
  return data.filter(row => {
    return Object.entries(filters).every(([key, value]) => {
      return row[key].toString().includes(value);
    });
  });
};

// Функция для сортировки данных
const applySorting = (data, sortBy) => {
  if (!sortBy || sortBy.length === 0) return data;
  
  return [...data].sort((a, b) => {
    for (const { field, order } of sortBy) {
      if (a[field] > b[field]) return order === 'asc' ? 1 : -1;
      if (a[field] < b[field]) return order === 'asc' ? -1 : 1;
    }
    return 0;
  });
};

// Функция для получения mock данных с учетом фильтров и сортировки
export const fetchMockData = async ({ page = 1, size = 20, sortBy = [], filters = {} }) => {
  let data = mockData;

  // Применение фильтров
  data = applyFilters(data, filters);

  // Применение сортировки
  data = applySorting(data, sortBy);

  // Пагинация данных
  const start = (page - 1) * size;
  const end = start + size;

  return {
    data: data.slice(start, end),
    total: data.length,
    page,
    size
  };
};

// Функция для получения метаданных (не изменяется)
export const fetchMockMetadata = async () => {
  return mockMetadata;
};
