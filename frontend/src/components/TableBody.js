import React from 'react';

const TableBody = ({ data, columns, onEdit, onDelete }) => {
  const visibleColumns = columns.filter(column => column.visible);

  return (
    <tbody>
      {data.map((row, rowIndex) => (
        <tr key={rowIndex}>
          {/* Кнопки для редактирования и удаления */}
          <td>
            <button onClick={() => onEdit(row.id)}>✏️</button>
            <button onClick={() => onDelete(row.id)}>🗑️</button>
          </td>

          {/* Отображение данных таблицы */}
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

export default TableBody;
