import React from 'react';

const SortComponent = ({ sortBy, setSortBy, columns }) => {
  const handleSortChange = (column) => {
    const existingSort = sortBy.find(sort => sort.field === column.name);
    if (existingSort) {
      const newOrder = existingSort.order === 'asc' ? 'desc' : 'asc';
      setSortBy(
        sortBy.map(sort =>
          sort.field === column.name ? { ...sort, order: newOrder } : sort
        )
      );
    } else {
      setSortBy([...sortBy, { field: column.name, order: 'asc' }]);
    }
  };

  const resetSort = () => {
    setSortBy([]);  // Сбрасываем сортировку
  };

  return (
    <div>
      {columns.map(column => (
        <button key={column.name} onClick={() => handleSortChange(column)}>
          {column.label} ({sortBy.find(sort => sort.field === column.name)?.order || 'none'})
        </button>
      ))}

      {/* Кнопка сброса сортировки */}
      <button onClick={resetSort} style={{ marginLeft: '10px' }}>
        Сбросить сортировку
      </button>
    </div>
  );
};

export default SortComponent;
