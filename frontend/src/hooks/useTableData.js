import { useState, useEffect } from 'react';
import { fetchTableData, fetchTableMetadata } from '../services/api';  // Обновим импорт
// Удаляем mockService, так как mock данные больше не нужны

const useTableData = (tableName) => {
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
      // Преобразуем фильтры в нужный формат для API
      const formattedFilters = filters.reduce((acc, filter) => {
        acc[filter.column] = filter.value;
        return acc;
      }, {});

      // Загружаем данные и метаданные из API
      const [tableData, tableMetadata] = await Promise.all([
        fetchTableData(tableName, page, size, sortBy, formattedFilters),
        fetchTableMetadata(tableName)  // Получаем метаданные
      ]);
      
      // Устанавливаем полученные данные и метаданные
      setData(tableData.data || []);
      setMetadata(tableMetadata || null);  // Метаданные из API
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
