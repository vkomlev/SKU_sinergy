import React from 'react';
import { getPrimaryKeyValue } from '../utils/tableUtils';

const TableBody = React.memo(({ data, columns, onEdit, onDelete, metadata }) => {
  const visibleColumns = columns.filter(column => column.visible);

  return (
    <tbody>
      {data.map((row, rowIndex) => {
        const primaryKeyValue = getPrimaryKeyValue(row, metadata);  // Получаем значение ключа
        //console.log('Primary Key Value для строки:', primaryKeyValue);  // Логируем значение ключа  
        return (
          <tr key={rowIndex}>
            {/* Кнопки для редактирования и удаления */}
            <td>
              <button onClick={() => onEdit(primaryKeyValue)}>✏️</button>
              <button onClick={() => onDelete(primaryKeyValue)}>🗑️</button>
            </td>

            {/* Отображение данных таблицы */}
            {visibleColumns.map(column => (
              <td key={column.name}>
                {row[column.name]}
              </td>
            ))}
          </tr>
        );
      })}
    </tbody>
  );
});

export default TableBody;
