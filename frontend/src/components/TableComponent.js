import React, { useEffect, useMemo } from 'react';
import DropFilterMenuComponent from './DropFilterMenuComponent';
import PaginationComponent from './PaginationComponent';
import SearchComponent from './SearchComponent';
import SortComponent from './SortComponent';
import { applySort, applyFilters } from '../utils/tableUtils';
import './styles/TableComponent.css';

const TableComponent = ({ data, metadata, page, setPage, size, setSize, total, sortBy, setSortBy, filters, setFilters, query, setQuery, loading, error }) => {

  useEffect(() => {
    console.log('TableComponent rendered', { page, size, total, metadata });
  }, [page, size, total, metadata]);

  // Применяем мемоизацию для данных
  const processedData = useMemo(() => {
    return applySort(applyFilters(data, filters), sortBy);
  }, [data, filters, sortBy]);

  const handlePageChange = (newPage) => {
    setPage(newPage);  
  };

  if (loading) {
    return <div>Загрузка данных...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (processedData.length === 0 && !loading) {
    return <div>Нет данных для отображения</div>;
  }

  const visibleColumns = metadata.columns.filter(column => column.visible);

  return (
    <div>
      <header>
        <div className="wrap-logo">
          <a>ГК Синергия</a>
        </div>
        <div>
          <SearchComponent setQuery={setQuery} />
        </div>
        <nav>
          <a>Добавить</a>
        </nav>
      </header>

      <DropFilterMenuComponent
        columns={metadata.columns}
        filters={filters}
        setFilters={setFilters}
      />

      <div className='big-table'>
        <table className='table'>
          <thead>
            <tr>
              {visibleColumns.map(column => (
                <th key={column.name}>
                  <SortComponent
                    sortBy={sortBy}
                    setSortBy={setSortBy}
                    columns={[column]}
                  />
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {processedData.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {visibleColumns.map(column => (
                  <td key={column.name}>
                    {row[column.name]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <PaginationComponent
        page={page}
        pageCount={Math.ceil(total / size)}
        onPageChange={handlePageChange}
      />

      <select value={size} onChange={(e) => setSize(Number(e.target.value))}>
        <option value={10}>10</option>
        <option value={25}>25</option>
        <option value={50}>50</option>
        <option value={100}>100</option>
      </select>
    </div>
  );
};

export default TableComponent;
