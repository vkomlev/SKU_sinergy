import React from 'react';
import SortComponent from './SortComponent';

const TableHeader = ({ columns, sortBy, setSortBy }) => {
  const visibleColumns = columns.filter(column => column.visible);

  return (
    <thead>
      <tr>
        <th>Действия</th>
        {visibleColumns.map(column => (
          <th key={column.name}>
            <SortComponent
              sortBy={sortBy}
              setSortBy={setSortBy}
              columns={[column]}
            />
          </th>
        ))}
      </tr>
    </thead>
  );
};

export default React.memo(TableHeader);  // Мемоизируем, чтобы избежать лишних рендеров
