import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import TableComponent from './components/TableComponent';
import useTableData from './hooks/useTableData';

const App = () => {
  const { data, metadata, page, updatePage, size, setSize, total, sortBy, setSortBy, filters, setFilters, query, setQuery, loading } = useTableData('import_DBS_delivery');

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
              setPage={updatePage}  // Передаем updatePage как setPage
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
            />
          }
        />
      </Routes>
    </Router>
  );
};

export default App;
