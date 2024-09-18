import React, { useState } from 'react';

const FilterComponent = React.memo(({ filters, setFilters, columns }) => {
  const [localFilters, setLocalFilters] = useState(filters);

  const handleFilterChange = (e, column) => {
    const { value } = e.target;
    setLocalFilters({
      ...localFilters,
      [column]: value
    });
  };

  const applyFilters = () => {
    setFilters(localFilters);
  };

  const resetFilters = () => {
    setLocalFilters({});
    setFilters({});
  };

  return (
    <div>
      {columns.map(column => (
        <div key={column.name}>
          <label>{column.label}</label>
          <input
            type="text"
            value={localFilters[column.name] || ''}
            onChange={(e) => handleFilterChange(e, column.name)}
          />
        </div>
      ))}
      <button onClick={applyFilters}>Применить фильтры</button>
      <button onClick={resetFilters}>Сбросить фильтры</button>
    </div>
  );
});

export default FilterComponent;
