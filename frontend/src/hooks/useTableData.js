import { useState, useEffect, useCallback } from 'react';
import { fetchTableData, fetchTableSearchResults, fetchTableMetadata } from '../services/api';

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

  const updatePage = (newPage) => {
    console.log('Page updated to:', newPage);
    setPage(newPage);
  };

  const fetchMetadata = useCallback(async () => {
    try {
      console.log('Fetching table metadata...');
      const tableMetadata = await fetchTableMetadata(tableName);
      console.log('Metadata received:', tableMetadata);
      setMetadata(tableMetadata);
    } catch (err) {
      console.error('Error fetching metadata:', err);
    }
  }, [tableName]);  // Добавляем tableName как зависимость

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
      console.log('Table data received:', tableData);
      setData(tableData.data || []);
      setTotal(tableData.total);
      setLoading(false);
    } catch (err) {
      setError(err);
      setLoading(false);
      console.error("Error fetching table data:", err);
    }
  }, [tableName, page, size, sortBy, filters, query]);  // Указываем зависимости

  useEffect(() => {
    console.log('Fetching data due to state change:', { page, size, sortBy, filters, query });
    fetchData();
    if (!metadata) {
      fetchMetadata();
    }
  }, [page, size, sortBy, filters, query, fetchData, fetchMetadata, metadata]);  // Добавляем необходимые зависимости

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
