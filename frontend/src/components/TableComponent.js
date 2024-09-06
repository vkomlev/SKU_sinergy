import React from 'react';
import FilterComponent from './FilterComponent';
import PaginationComponent from './PaginationComponent';
import SearchComponent from './SearchComponent';
import SortComponent from './SortComponent';

const TableComponent = ({ data, metadata, page, setPage, size, setSize, total, sortBy, setSortBy, filters, setFilters }) => {
  // Проверка на наличие метаданных и данных
  if (!metadata || !metadata.columns) {
    return <div>Загрузка данных...</div>;
  }

  if (data.length === 0) {
    return <div>Нет данных для отображения</div>;
  }

  return (
    <div>
      {/* Компонент поиска */}
      <SearchComponent setFilters={setFilters} />

      {/* Компонент фильтрации */}
      <FilterComponent filters={filters} setFilters={setFilters} columns={metadata.columns} />

      {/* Компонент сортировки */}
      <SortComponent sortBy={sortBy} setSortBy={setSortBy} columns={metadata.columns} />

      {/* Таблица с данными */}
      <table>
        <thead>
          <tr>
            {metadata.columns.map(column => (
              column.visible && <th key={column.name}>{column.label}</th>
            ))}
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
