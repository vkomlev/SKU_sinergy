import { useState, useEffect } from 'react';
import { fetchTableData } from '../services/api';
import { fetchMockMetadata } from '../services/mockService';

const useTableData = (tableName, isMock = false) => {
  const [data, setData] = useState([]);
  const [metadata, setMetadata] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(20);
  const [sortBy, setSortBy] = useState([]);  // Массив сортировок
  const [filters, setFilters] = useState([]); // Инициализируем как массив

  // Функция для получения данных
  const fetchData = async () => {
    setLoading(true);  // Начинаем загрузку
    try {
      // Преобразование фильтров в формат для API
      const formattedFilters = filters.reduce((acc, filter) => {
        acc[filter.column] = filter.value;
        return acc;
      }, {});

      // Загружаем данные из API
      const tableData = await fetchTableData(tableName, page, size, sortBy, formattedFilters);
      
      // Загружаем метаданные из mock
      const mockMetadata = await fetchMockMetadata();
      
      // Устанавливаем полученные данные
      setData(tableData.data || []);
      setMetadata(mockMetadata || null);  // Метаданные из mock файла
      setLoading(false);  // Завершаем загрузку
    } catch (err) {
      setError(err);
      setLoading(false);
      console.error("Ошибка загрузки данных:", err);
    }
  };

  // Вызываем fetchData при изменении страницы, размера, сортировки или фильтров
  useEffect(() => {
    fetchData();
  }, [page, size, sortBy, filters]);

  return { data, metadata, loading, error, page, setPage, size, setSize, sortBy, setSortBy, filters, setFilters };
};

export default useTableData;
