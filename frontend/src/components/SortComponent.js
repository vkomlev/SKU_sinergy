import React from 'react';

const SortComponent = ({ sortBy, setSortBy, columns }) => {

  // Функция для обработки кликов по заголовкам столбцов
  const handleSortChange = (column) => {
    const existingSort = sortBy.find(sort => sort.field === column.name);

    if (!existingSort) {
      // Если сортировки по этому столбцу нет — сортируем по возрастанию
      setSortBy([{ field: column.name, order: 'asc' }]);
    } else if (existingSort.order === 'asc') {
      // Если сортировка по возрастанию — переключаем на убывание
      setSortBy([{ field: column.name, order: 'desc' }]);
    } else {
      // Если сортировка по убыванию — удаляем сортировку
      setSortBy([]);
    }
  };

  // Функция для получения иконки сортировки
  const getSortIcon = (column) => {
    const existingSort = sortBy.find(sort => sort.field === column.name);
    if (!existingSort) return null;
    return existingSort.order === 'asc' ? '▲' : '▼'; // Иконки для сортировки
  };

  return (
    <>
      {columns.map(column => (
        <th key={column.name} onClick={() => handleSortChange(column)}>
          {column.label} {getSortIcon(column)} {/* Отображаем значок сортировки */}
        </th>
      ))}
    </>
  );
};

export default SortComponent;
