import React, { useState } from 'react';
import { addFilter, removeFilter } from '../utils/filterUtils';  // Импортируем утилиты для фильтрации
import './styles/DropFilterMenuComponent.css';  // Подключаем стили

const DropFilterMenuComponent = React.memo(({ columns, filters, setFilters, resetFiltersSort }) => {
  const [selectedColumn, setSelectedColumn] = useState('');
  const [filterValue, setFilterValue] = useState('');

  const handleAddFilter = () => {
    const newFilter = {
      column: selectedColumn,
      expression: '=',  // Пока используем только '='
      value: filterValue,
    };
    setFilters(addFilter(filters, newFilter));  // Используем утилиту для добавления фильтра
    resetFields();
  };

  const handleRemoveFilter = (index) => {
    setFilters(removeFilter(filters, index));  // Используем утилиту для удаления фильтра
  };

  const resetFields = () => {
    setSelectedColumn('');
    setFilterValue('');
  };

  return (
    <div>
      <span className="title">Фильтры</span>
      <div className="filter-menu">
        <div className="filter-form">
          <select value={selectedColumn} onChange={(e) => setSelectedColumn(e.target.value)}>
            <option value="">Выберите столбец</option>
            {columns.map(column => (
              <option key={column.name} value={column.name}>
                {column.label}
              </option>
            ))}
          </select>
          <input
            type="text"
            value={filterValue}
            onChange={(e) => setFilterValue(e.target.value)}
            placeholder="Введите значение"
          />
          <button onClick={handleAddFilter}>Добавить фильтр</button>
          <button onClick={resetFiltersSort}>Сбросить фильтры и сортировку</button>
        </div>

        {Array.isArray(filters) && filters.length > 0 && (
          <ul className="active-filters">
            {filters.map((filter, index) => (
              <li key={index}>
                {columns.find(col => col.name === filter.column)?.label} {filter.expression} {filter.value}
                <button onClick={() => handleRemoveFilter(index)}>Удалить</button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
});

export default DropFilterMenuComponent;
