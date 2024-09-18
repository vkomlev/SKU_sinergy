import React, { useState } from 'react';

const SearchComponent = React.memo(({ setQuery }) => {  // Получаем setQuery из props
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = () => {
    setQuery(searchTerm);  // Обновляем строку поиска
  };

  return (
    <div className="search-container">
      <input
        type="text"
        placeholder="Поиск..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <button onClick={handleSearch}>Поиск</button>
    </div>
  );
});

export default SearchComponent;
