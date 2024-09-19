import { useState, useEffect, useCallback, useMemo } from 'react';
import { fetchTableData, fetchTableSearchResults, fetchTableMetadata } from '../services/api';
import { debounce } from '../utils/debounce';

const useTableData = (tableName) => {
  const [data, setData] = useState([]);
  const [metadata, setMetadata] = useState(null);
  const [loading, setLoading] = useState(false);  // Изначально не загружаем данные
  const [loadingMetadata, setLoadingMetadata] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(20);
  const [total, setTotal] = useState(0);
  const [sortBy, setSortBy] = useState([]);
  const [filters, setFilters] = useState([]);
  const [query, setQuery] = useState('');

  // Локально применяем сортировку, пока данные не обновлены с сервера
  const [localData, setLocalData] = useState([]);

  const fetchData = useCallback(async () => {
    if (loadingMetadata || !metadata) {
      console.log('Skipping data fetch until metadata is loaded');
      return;
    }
    setLoading(true);
    try {
      console.log('Fetching table data from server...');
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
      console.log('Data fetched:', tableData);
      setData(tableData.data || []);
      setLocalData(tableData.data || []);  // Обновляем локальные данные
      setTotal(tableData.total);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Ошибка загрузки данных таблицы');
      setLoading(false);
    }
  }, [tableName, page, size, sortBy, filters, query, metadata, loadingMetadata]);

  const debouncedFetchData = useMemo(() => debounce(fetchData, 300), [fetchData]);

  const updatePage = (newPage) => {
    console.log('Updating page:', newPage);
    setPage(newPage);
  };

  const fetchMetadata = useCallback(async () => {
    if (metadata || !loadingMetadata) {
      console.log('Metadata already fetched, skipping...');
      return;
    }
    try {
      console.log('Fetching table metadata...');
      const tableMetadata = await fetchTableMetadata(tableName);
      console.log('Metadata fetched:', tableMetadata);
      setMetadata(tableMetadata);
      setLoadingMetadata(false);
    } catch (err) {
      console.error('Error fetching metadata:', err);
      setError('Ошибка загрузки метаданных');
      setLoadingMetadata(false);
    }
  }, [tableName, metadata, loadingMetadata]);

  useEffect(() => {
    console.log('Fetching data and metadata');
    fetchMetadata();
    debouncedFetchData();
  }, [page, size, sortBy, filters, query, debouncedFetchData, fetchMetadata]);

  return {
    data,         // Данные с сервера
    localData,    // Локально отсортированные данные
    metadata,
    loading,
    loadingMetadata,
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
