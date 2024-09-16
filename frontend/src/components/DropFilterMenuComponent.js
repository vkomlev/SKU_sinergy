import React, { useState } from 'react';

const DropFilterMenuComponent = ({ columns, filters, setFilters }) => {
  const [selectedColumn, setSelectedColumn] = useState('');
  const [filterValue, setFilterValue] = useState('');

  // Добавление фильтра
  const addFilter = () => {
    if (!selectedColumn || !filterValue) {
      alert('Выберите столбец и введите значение');
      return;
    }

    const newFilter = {
      column: selectedColumn,
      expression: '=', // Пока используем только '=', возможно расширение в будущем
      value: filterValue,
    };

    // Обновляем массив фильтров, что вызовет обновление данных
    setFilters(prevFilters => [...prevFilters, newFilter]);
    resetFields();
  };

  // Сброс полей
  const resetFields = () => {
    setSelectedColumn('');
    setFilterValue('');
  };

  // Удаление фильтра
  const removeFilter = (index) => {
    setFilters(prevFilters => prevFilters.filter((_, i) => i !== index));
  };

  return (
    <div>
      <span className="title">Фильтры</span>
      <div className="filter-menu">
        <div className="filter-form">
          {/* Выбор столбца */}
          <select value={selectedColumn} onChange={(e) => setSelectedColumn(e.target.value)}>
            <option value="">Выберите столбец</option>
            {columns.map(column => (
              <option key={column.name} value={column.name}>
                {column.label}
              </option>
            ))}
          </select>

          {/* Поле ввода для значения */}
          <input
            type="text"
            value={filterValue}
            onChange={(e) => setFilterValue(e.target.value)}
            placeholder="Введите значение"
          />

          {/* Кнопка добавления фильтра */}
          <button onClick={addFilter}>Добавить фильтр</button>
        </div>

        {/* Список активных фильтров */}
        {Array.isArray(filters) && filters.length > 0 && (
          <ul className="active-filters">
            {filters.map((filter, index) => (
              <li key={index}>
                {columns.find(col => col.name === filter.column)?.label} {filter.expression} {filter.value}
                <button onClick={() => removeFilter(index)}>Удалить</button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default DropFilterMenuComponent;
