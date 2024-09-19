import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import TableComponent from './components/TableComponent';
import useTableData from './hooks/useTableData';

const App = () => {
  const tableName = 'import_DBS_delivery';  // Имя таблицы
  const { data, metadata, page, updatePage, size, setSize, total, sortBy, setSortBy, filters, setFilters, query, setQuery, loading } = useTableData(tableName);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route
          path="/import_DBS_delivery"
          element={
            <TableComponent
              data={data}
              metadata={metadata}
              page={page}
              setPage={updatePage}
              size={size}
              setSize={setSize}
              total={total}
              sortBy={sortBy}
              setSortBy={setSortBy}
              filters={filters}
              setFilters={setFilters}
              query={query}
              setQuery={setQuery}
              loading={loading}
              tableName={tableName}  /* Передача имени таблицы в компонент */
            />
          }
        />
      </Routes>
    </Router>
  );
};

export default App;
