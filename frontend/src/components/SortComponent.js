import React from 'react';

const SortComponent = React.memo(({ column, sortBy, setSortBy }) => {
  const handleSort = () => {
    const currentSort = sortBy.find(sort => sort.field === column.name);
    const newSortOrder = currentSort?.order === 'asc' ? 'desc' : 'asc';
    setSortBy([{ field: column.name, order: newSortOrder }]);
  };

  const currentSort = sortBy.find(sort => sort.field === column.name);

  return (
    <div onClick={handleSort} style={{ cursor: 'pointer', display: 'flex', alignItems: 'center' }}>
      {column.label}
      {currentSort && (
        <span className="sort-icon" style={{ marginLeft: '8px', fontSize: '18px', color: '#f0f0f0' }}>
          {currentSort.order === 'asc' ? '▲' : '▼'}
        </span>
      )}
    </div>
  );
});

export default SortComponent;
