import React, { useEffect, useMemo, useState } from 'react'; 
import { applySort, applyFilters } from '../utils/tableUtils';
import { deleteRecord, fetchRecord, saveRecord } from '../services/api';
import SearchComponent from './SearchComponent';
import EditForm from './EditForm';
import DropFilterMenuComponent from './DropFilterMenuComponent';
import TableHeader from './TableHeader';
import TableBody from './TableBody';
import PaginationComponent from './PaginationComponent';
import './styles/TableComponent.css';

const TableComponent = ({ data, localData, metadata, page, setPage, size, setSize, total, sortBy, setSortBy, filters, setFilters, query, setQuery, loading, loadingMetadata, error, columns, tableName }) => {

  const [showForm, setShowForm] = useState(false);
  const [editData, setEditData] = useState(null);
  const [formLoading, setFormLoading] = useState(false);

  useEffect(() => {
    console.log('TableComponent rendered', { page, size, total, metadata });
  }, [page, size, total, metadata]);

  // Открыть форму для добавления новой записи
  const handleAddClick = () => {
    setShowForm(true);
    setEditData(null);
    setFormLoading(false);
  };

  // Открыть форму для редактирования записи
  const handleEditClick = async (recordId) => {
    setFormLoading(true);
    try {
      const record = await fetchRecord(tableName, recordId);
      setEditData(record);
      setShowForm(true);
      setFormLoading(false);
    } catch (error) {
      console.error('Ошибка при загрузке данных для редактирования:', error);
      setFormLoading(false);
    }
  };

  // Обработка сохранения формы
  const handleFormSubmit = async (formData) => {
    console.log("Форма отправлена с данными:", formData);
    try {
      const isEditing = !!editData;
      await saveRecord(tableName, formData, isEditing);
      setShowForm(false);
    } catch (error) {
      console.error('Ошибка при сохранении данных:', error);
    }
  };

  // Удаление записи
  const handleDeleteClick = async (recordId) => {
    await deleteRecord(tableName, recordId);
  };

  // Обработка данных таблицы с фильтрацией и сортировкой
  const processedData = useMemo(() => {
    if (loading || loadingMetadata) {
      console.log('Using locally sorted data during loading state');
      return applySort(applyFilters(localData || [], filters), sortBy);
    }
    console.log('Processing server data with filters and sorting');
    return applySort(applyFilters(data || [], filters), sortBy);
  }, [data, localData, filters, sortBy, loading, loadingMetadata]);

  const handlePageChange = (newPage) => {
    console.log('Page changed to:', newPage);
    setPage(newPage);  
  };

  return (
    <div>
      {/* Скрываем остальные элементы страницы, если форма открыта */}
      <div className={showForm ? 'content-hidden' : ''}>
        <header>
          <div className="wrap-logo">
            <a href="/">ГК Синергия</a>
          </div>
          <div>
            <SearchComponent setQuery={setQuery} />
          </div>
          <div>
            <button onClick={handleAddClick}>Добавить</button>
          </div>
        </header>

        <DropFilterMenuComponent
          columns={metadata.columns}
          filters={filters}
          setFilters={setFilters}
        />

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
              onEdit={handleEditClick}
              onDelete={handleDeleteClick}
            />
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

      {/* Отображаем форму поверх остальных элементов */}
      {showForm && (
        <div className="form-container">
          <EditForm
            onClose={() => setShowForm(false)}
            initialData={editData}
            metadata={metadata}
            formLoading={formLoading}
            onSubmit={handleFormSubmit}
          />
        </div>
      )}
    </div>
  );
};

export default TableComponent;
