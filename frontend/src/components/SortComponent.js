// SortComponent.js
import React from 'react';

const SortComponent = React.memo(({ sortBy, setSortBy, columns }) => {
  const handleSort = () => {
    const currentSort = sortBy.find(sort => sort.field === columns[0].name);
    const newSortOrder = currentSort?.order === 'asc' ? 'desc' : 'asc';
    setSortBy([{ field: columns[0].name, order: newSortOrder }]);
  };

  const currentSort = sortBy.find(sort => sort.field === columns[0].name);

  return (
    <div onClick={handleSort} style={{ cursor: 'pointer' }}>
      {columns[0].label}
      {currentSort && (currentSort.order === 'asc' ? ' 🔼' : ' 🔽')}
    </div>
  );
});

export default SortComponent;
