import React, { useEffect, useMemo } from 'react';
import DropFilterMenuComponent from './DropFilterMenuComponent';
import PaginationComponent from './PaginationComponent';
import SearchComponent from './SearchComponent';
import TableHeader from './TableHeader';
import TableBody from './TableBody';
import { applySort, applyFilters } from '../utils/tableUtils';
import './styles/TableComponent.css';

const TableComponent = ({ data, metadata, page, setPage, size, setSize, total, sortBy, setSortBy, filters, setFilters, query, setQuery, loading, error }) => {

  useEffect(() => {
    console.log('TableComponent rendered', { page, size, total, metadata });
  }, [page, size, total, metadata]);

  // Мемоизируем обработанные данные
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

      {/* Компонент меню фильтрации */}
      <DropFilterMenuComponent
        columns={metadata.columns}
        filters={filters}
        setFilters={setFilters}
      />

      {/* Таблица с данными */}
      <div className='big-table'>
        <table className='table'>
          <TableHeader 
            columns={metadata.columns} 
            sortBy={sortBy} 
            setSortBy={setSortBy} 
          />
          <TableBody 
            data={processedData} 
            columns={metadata.columns} 
          />
        </table>
      </div>

      {/* Компонент пагинации */}
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
