import React, { useState } from 'react';
import { addFilter, removeFilter } from '../utils/filterUtils'; // Импортируем утилиты для фильтрации
import './styles/DropFilterMenuComponent.css'; // Подключаем стили

const DropFilterMenuComponent = React.memo(({ columns, filters, setFilters, resetFiltersSort }) => {
  const [selectedColumn, setSelectedColumn] = useState('');
  const [filterExpression, setFilterExpression] = useState('=');
  const [filterValue, setFilterValue] = useState('');
  const [filterValueFrom, setFilterValueFrom] = useState('');
  const [filterValueTo, setFilterValueTo] = useState('');

  // Объект для перевода выражений
  const expressionTranslations = {
    '=': 'равно',
    '!=': 'не равно',
    '>': 'больше',
    '<': 'меньше',
    '>=': 'больше или равно',
    '<=': 'меньше или равно',
    'between': 'между',
    'contains': 'содержит',
    'not contains': 'не содержит',
    'starts with': 'начинается с',
    'ends with': 'заканчивается на',
    'today': 'сегодня',
    'yesterday': 'вчера',
    'current_week': 'текущая неделя',
    'current_month': 'текущий месяц',
    'current_quarter': 'текущий квартал',
    'current_year': 'текущий год',
    'previous_week': 'предыдущая неделя',
    'previous_month': 'предыдущий месяц',
    'previous_year': 'предыдущий год',
  };

  // Получение возможных выражений на основе типа данных выбранного столбца
  const getExpressionsByType = (input_type) => {
    switch (input_type) {
      case 'number':
        return ['=', '!=', '>', '<', '>=', '<=', 'between'];
      case 'big_text':
      case 'text':
        return ['=', '!=', 'contains', 'not contains', 'starts with', 'ends with'];
      case 'date':
      case 'datetime':
        return [
          '=', '!=', '>', '<', '>=', '<=', 'between',
          'today', 'yesterday', 'current_week', 'current_month',
          'current_quarter', 'current_year', 'previous_week',
          'previous_month', 'previous_year'
        ];
      default:
        return ['=']; // По умолчанию
    }
  };

  // Установка выражений в зависимости от выбранного столбца
  const expressions = selectedColumn
    ? getExpressionsByType(columns.find(col => col.name === selectedColumn)?.input_type)
    : [];

  const handleAddFilter = () => {
    const newFilter = {
      column: selectedColumn,
      expression: filterExpression,
    };

    // Если выражение не является временным, добавляем значение
    const isTemporalExpression = [
      'today', 'yesterday', 'current_week', 'current_month',
      'current_quarter', 'current_year', 'previous_week',
      'previous_month', 'previous_year'
    ].includes(filterExpression);

    if (!isTemporalExpression) {
      newFilter.value = filterExpression === 'between' ? [filterValueFrom, filterValueTo] : filterValue;
    }

    console.log('Добавляем фильтр:', newFilter);
    setFilters(addFilter(filters, newFilter)); // Используем утилиту для добавления фильтра
    resetFields();
  };

  const handleRemoveFilter = (index) => {
    setFilters(removeFilter(filters, index)); // Используем утилиту для удаления фильтра
  };

  const resetFields = () => {
    setSelectedColumn('');
    setFilterExpression('=');
    setFilterValue('');
    setFilterValueFrom('');
    setFilterValueTo('');
  };

  // Поле ввода значения для фильтра
  const renderInputField = () => {
    const selectedColumnData = columns.find(col => col.name === selectedColumn);

    if (!selectedColumnData) return null;

    const isTemporalExpression = [
      'today', 'yesterday', 'current_week', 'current_month',
      'current_quarter', 'current_year', 'previous_week',
      'previous_month', 'previous_year'
    ].includes(filterExpression);

    // Обработка выражения "between"
    if (filterExpression === 'between') {
      return (
        <div>
          <input
            type={selectedColumnData.input_type === 'date' ? 'date' : 'text'}
            placeholder="От"
            onChange={(e) => setFilterValueFrom(e.target.value)}
          />
          <input
            type={selectedColumnData.input_type === 'date' ? 'date' : 'text'}
            placeholder="До"
            onChange={(e) => setFilterValueTo(e.target.value)}
          />
        </div>
      );
    }

    // Если выражение является временным, не отображаем поле ввода
    if (isTemporalExpression) {
      return (
        <div>
          <span/> 
        </div>
      );
    }

    switch (selectedColumnData.input_type) {
      case 'number':
        return (
          <input
            type="number"
            value={filterValue}
            onChange={(e) => setFilterValue(e.target.value)}
            placeholder="Введите число"
          />
        );
      case 'date':
        return (
          <input
            type="date"
            value={filterValue}
            onChange={(e) => setFilterValue(e.target.value)}
          />
        );
      case 'big_text':
      case 'text':
      default:
        return (
          <input
            type="text"
            value={filterValue}
            onChange={(e) => setFilterValue(e.target.value)}
            placeholder="Введите значение"
          />
        );
    }
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

          {/* Выбор выражения фильтра */}
          <select value={filterExpression} onChange={(e) => setFilterExpression(e.target.value)}>
            {expressions.map(expression => (
              <option key={expression} value={expression}>
                {expressionTranslations[expression]} {/* Отображаем русский аналог выражения */}
              </option>
            ))}
          </select>

          {/* Поле ввода значения для фильтра */}
          {renderInputField()}
  
          <button onClick={handleAddFilter}>Добавить фильтр</button>
          <button onClick={resetFiltersSort}>Сбросить фильтры и сортировку</button>
        </div>
 
        {Array.isArray(filters) && filters.length > 0 && (
          <ul className="active-filters">
            {filters.map((filter, index) => (
              <li key={index}>
                {columns.find(col => col.name === filter.column)?.label} {expressionTranslations[filter.expression] || filter.expression} {filter.value && Array.isArray(filter.value) ? filter.value.join(' и ') : filter.value}
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