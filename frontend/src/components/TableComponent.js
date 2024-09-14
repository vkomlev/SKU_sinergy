import React from 'react';
import DropFilterMenuComponent from './DropFilterMenuComponent';
import PaginationComponent from './PaginationComponent';
import SearchComponent from './SearchComponent';  // Импортируем компонент поиска
import SortComponent from './SortComponent';  // Импортируем компонент сортировки
import './styles/TableComponent.css';

const TableComponent = ({ data, metadata, page, setPage, size, setSize, total, sortBy, setSortBy, filters, setFilters, query, setQuery }) => {
  if (!metadata || !metadata.columns) {
    return <div>Загрузка данных...</div>;
  }

  if (data.length === 0) {
    return <div>Нет данных для отображения</div>;
  }

  return (
    <div>
      <header>
        <div className="wrap-logo">
          <a>ГК Синергия</a>
        </div>
        <div>
          <SearchComponent setQuery={setQuery} />  {/* Передаем setQuery для управления поиском */}
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
          <thead>
            <tr>
              <SortComponent
                sortBy={sortBy}
                setSortBy={setSortBy}
                columns={metadata.columns}
              />
            </tr>
          </thead>
          <tbody>
            {data.map(row => (
              <tr key={row.id_dbs}>
                {metadata.columns.map(column => (
                  column.visible && <td key={column.name}>{row[column.name]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Компонент пагинации */}
      <PaginationComponent
        page={page}
        pageCount={Math.ceil(total / size)}
        onPageChange={setPage}
      />

      {/* Выбор размера страницы */}
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
