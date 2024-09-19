export const addFilter = (filters, newFilter) => {
    if (!newFilter.column || !newFilter.value) {
      return filters;  // Не добавляем пустой фильтр
    }
    return [...filters, newFilter];
  };
  
  export const removeFilter = (filters, index) => {
    return filters.filter((_, i) => i !== index);
  };
  