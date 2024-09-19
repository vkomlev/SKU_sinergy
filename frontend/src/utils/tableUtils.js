// tableUtils.js

// Функция для обработки сортировки
export const applySort = (data, sortBy) => {
    if (!sortBy || sortBy.length === 0) return data;
  
    return [...data].sort((a, b) => {
      const { field, order } = sortBy[0];
      if (order === 'asc') {
        return a[field] > b[field] ? 1 : -1;
      } else {
        return a[field] < b[field] ? 1 : -1;
      }
    });
  };
  
  // Функция для применения фильтров
  export const applyFilters = (data, filters) => {
    if (!filters || filters.length === 0) return data;
  
    return data.filter(row => {
      return filters.every(filter => {
        const cellValue = row[filter.column];
        return cellValue != null && cellValue.toString().includes(filter.value);  // Добавляем проверку на null/undefined
      });
    });
  };

  // Получить значение первичного ключа из строки
export const getPrimaryKeyValue = (row, metadata) => {
  // Находим колонку, которая является первичным ключом
  const primaryKeyColumn = metadata.columns.find(column => column.primary_key);
  
  if (primaryKeyColumn) {
    return row[primaryKeyColumn.name];  // Возвращаем значение ключа
  }
  
  console.warn('Primary key not found in metadata');
  return null;  // Если ключ не найден, возвращаем null
};
  