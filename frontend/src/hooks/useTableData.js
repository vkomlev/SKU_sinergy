import { useState, useEffect, useCallback, useMemo } from 'react';
import { fetchTableData, fetchTableSearchResults, fetchTableMetadata } from '../services/api';
import { debounce } from '../utils/debounce';  // Импортируем утилиту дебаунсинга

const useTableData = (tableName) => {
  const [data, setData] = useState([]);
  const [metadata, setMetadata] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(20);
  const [total, setTotal] = useState(0);
  const [sortBy, setSortBy] = useState([]);
  const [filters, setFilters] = useState([]);
  const [query, setQuery] = useState('');

  // Функция для получения данных
  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      let tableData;
      if (query) {
        tableData = await fetchTableSearchResults(tableName, query);
      } else {
        const formattedFilters = filters.reduce((acc, filter) => {
          acc[filter.column] = filter.value;
          return acc;
        }, {});
        tableData = await fetchTableData(tableName, page, size, sortBy, formattedFilters);
      }
      setData(tableData.data || []);
      setTotal(tableData.total);
      setLoading(false);
    } catch (err) {
      setError('Ошибка загрузки данных таблицы');
      setLoading(false);
    }
  }, [tableName, page, size, sortBy, filters, query]);

  // Меморизируем debouncedFetchData только после инициализации fetchData
  const debouncedFetchData = useMemo(() => debounce(fetchData, 300), [fetchData]);

  const updatePage = (newPage) => {
    setPage(newPage);
  };

  const fetchMetadata = useCallback(async () => {
    try {
      const tableMetadata = await fetchTableMetadata(tableName);
      setMetadata(tableMetadata);
    } catch (err) {
      setError('Ошибка загрузки метаданных');
    }
  }, [tableName]);

  // Используем debouncedFetchData вместо прямого вызова fetchData
  useEffect(() => {
    debouncedFetchData();
    if (!metadata) {
      fetchMetadata();
    }
  }, [page, size, sortBy, filters, query, debouncedFetchData, fetchMetadata, metadata]);

  return {
    data,
    metadata,
    loading,
    error,
    page,
    updatePage,
    size,
    setSize,
    total,
    sortBy,
    setSortBy,
    filters,
    setFilters,
    query,
    setQuery,
  };
};

export default useTableData;
