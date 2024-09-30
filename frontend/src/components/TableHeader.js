import React from 'react';
import SortComponent from './SortComponent';

const TableHeader = React.memo(({ columns, sortBy, setSortBy }) => {
  const visibleColumns = columns.filter(column => column.visible);

  return (
    <thead>
      <tr>
        <th>Действия</th>
        {visibleColumns.map(column => (
          <th key={column.name}>
            <SortComponent
              column={column}
              sortBy={sortBy}
              setSortBy={setSortBy}
            />
          </th>
        ))}
      </tr>
    </thead>
  );
});

export default React.memo(TableHeader);
