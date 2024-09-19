import React from 'react';

const TableBody = ({ data, columns }) => {
  const visibleColumns = columns.filter(column => column.visible);

  return (
    <tbody>
      {data.map((row, rowIndex) => (
        <tr key={rowIndex}>
          {visibleColumns.map(column => (
            <td key={column.name}>
              {row[column.name]}
            </td>
          ))}
        </tr>
      ))}
    </tbody>
  );
};

export default React.memo(TableBody);  // Мемоизируем для оптимизации
