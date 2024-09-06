import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import TableComponent from './components/TableComponent';
import useTableData from './hooks/useTableData';  // Хук для работы с таблицей

const App = () => {
  // Получаем данные для таблицы Import_DBS_Delivery
  const { data, metadata, page, setPage, size, setSize, total, sortBy, setSortBy, filters, setFilters } = useTableData('import_DBS_delivery', false); // false, потому что работаем с API, а не mock данными

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
              setPage={setPage}
              size={size}
              setSize={setSize}
              total={total}
              sortBy={sortBy}
              setSortBy={setSortBy}
              filters={filters}
              setFilters={setFilters}
            />
          }
        />
      </Routes>
    </Router>
  );
};

export default App;