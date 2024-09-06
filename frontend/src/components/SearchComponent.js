import React, { useState } from 'react';

const SearchComponent = ({ setFilters }) => {
  const [query, setQuery] = useState('');

  const handleSearch = () => {
    setFilters(prevFilters => ({
      ...prevFilters,
      globalSearch: query
    }));
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Поиск..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleSearch}>Искать</button>
    </div>
  );
};

export default SearchComponent;
