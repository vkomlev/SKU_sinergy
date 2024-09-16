import { useState, useEffect } from 'react';
import { fetchTableData, fetchTableSearchResults, fetchTableMetadata } from '../services/api';

const useTableData = (tableName) => {
  const [data, setData] = useState([]);
  const [metadata, setMetadata] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(20);
  const [sortBy, setSortBy] = useState([]);  // Массив сортировок
  const [filters, setFilters] = useState([]); // Фильтры
  const [query, setQuery] = useState('');    // Поисковый запрос

  const fetchData = async () => {
    setLoading(true);  // Начинаем загрузку
    try {
      let tableData;
      if (query) {
        // Если есть строка поиска — используем поиск
        tableData = await fetchTableSearchResults(tableName, query);
      } else {
        // Преобразуем фильтры в формат для API
        const formattedFilters = filters.reduce((acc, filter) => {
          acc[filter.column] = filter.value;
          return acc;
        }, {});

        // Загружаем данные
        tableData = await fetchTableData(tableName, page, size, sortBy, formattedFilters);
      }
      
      // Загружаем метаданные из API
      const tableMetadata = await fetchTableMetadata(tableName);

      // Устанавливаем полученные данные
      setData(tableData.data || []);
      setMetadata(tableMetadata || null);
      setLoading(false);  // Завершаем загрузку
    } catch (err) {
      setError(err);
      setLoading(false);
      console.error("Ошибка загрузки данных:", err);
    }
  };

  useEffect(() => {
    fetchData();
  }, [page, size, sortBy, filters, query]);

  return { data, metadata, loading, error, page, setPage, size, setSize, sortBy, setSortBy, filters, setFilters, query, setQuery };
};

export default useTableData;
