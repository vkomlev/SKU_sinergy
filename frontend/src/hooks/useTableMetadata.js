import { useState, useEffect } from 'react';
import { fetchTableMetadata } from '../services/api';

export const useTableMetadata = (tableName, showView = false) => {
  const [metadata, setMetadata] = useState(null);
  const [loadingMetadata, setLoadingMetadata] = useState(true);

  useEffect(() => {
    const loadMetadata = async () => {
      try {
        const tableMetadata = await fetchTableMetadata(tableName, showView);  // Передаем showView
        setMetadata(tableMetadata);
      } catch (error) {
        console.error('Ошибка загрузки метаданных:', error);
      } finally {
        setLoadingMetadata(false);
      }
    };

    loadMetadata();
  }, [tableName, showView]);

  return { metadata, loadingMetadata };
};