import { useState, useEffect, useCallback } from 'react';

export const useTableFiltersSort = (tableName, initialSortBy = [], initialFilters = [], fetchTableData, fetchTableSearchResults) => {
  const [filters, setFilters] = useState(initialFilters);
  const [sortBy, setSortBy] = useState(initialSortBy);
  const [filteredSortedData, setFilteredSortedData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);  
  const [page, setPage] = useState(1);    
  const [size, setSize] = useState(20);   
  const [query, setQuery] = useState('');  // Добавляем состояние для строки поиска

  // Обновлена логика для получения данных: если есть query, запрашиваем searchResults
  const updateTableData = useCallback(async () => {
    setLoading(true);
    try {
      let response;
      if (query) {
        // Если есть запрос, используем API для поиска
        response = await fetchTableSearchResults(tableName, query, true);  // Добавлен параметр showView = true
      } else {
        // Иначе получаем обычные данные
        response = await fetchTableData(tableName, page, size, sortBy, filters, true);  // Добавлен параметр showView = true
      }
      setFilteredSortedData(response.data);  // Обновляем данные
      setTotal(response.total);  // Обновляем количество записей
    } catch (error) {
      console.error('Ошибка при загрузке данных:', error);
    } finally {
      setLoading(false);
    }
  }, [tableName, page, size, sortBy, filters, query, fetchTableData, fetchTableSearchResults]);

  useEffect(() => {
    updateTableData();
  }, [sortBy, filters, query, tableName, updateTableData]);

  // Общая функция для сброса фильтров и сортировки
  const resetFiltersSort = () => {
    setFilters([]);  // Сброс фильтров
    setSortBy([]);   // Сброс сортировки
    setPage(1);      // Возвращаем на первую страницу
  };

  return {
    filteredSortedData,
    setFilteredSortedData,
    filters,
    sortBy,
    setFilters,
    setSortBy,
    loading,
    total,
    page,
    setPage,
    size,
    setSize,
    query,       // Возвращаем состояние строки поиска
    setQuery,     // Функция для обновления строки поиска
    resetFiltersSort  
  };
};