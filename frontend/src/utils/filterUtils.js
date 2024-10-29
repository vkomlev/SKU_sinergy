// frontend\src\utils\filterUtils.js
export const addFilter = (filters, newFilter) => {
  // Определяем, является ли фильтр временным
  const isTemporalExpression = [
    'today', 'yesterday', 'current_week', 'current_month',
    'current_quarter', 'current_year', 'previous_week',
    'previous_month', 'previous_year'
  ].includes(newFilter.expression);

  // Если фильтр не временный и значение отсутствует, не добавляем фильтр
  if (!newFilter.column || (!isTemporalExpression && !newFilter.value)) {
    return filters; 
  }

  return [...filters, newFilter];
};

export const removeFilter = (filters, index) => {
  return filters.filter((_, i) => i !== index);
};
