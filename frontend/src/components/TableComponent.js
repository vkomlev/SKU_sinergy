import React, { useCallback, useState } from 'react';
import { getPrimaryKeyField } from '../utils/tableUtils';
import { deleteRecord, fetchRecord, saveRecord, fetchTableData, fetchTableSearchResults } from '../services/api';  
import { useTableFiltersSort } from '../hooks/useTableFiltersSort';
import SearchComponent from './SearchComponent';
import EditForm from './EditForm';
import DropFilterMenuComponent from './DropFilterMenuComponent';
import TableHeader from './TableHeader';
import TableBody from './TableBody';
import PaginationComponent from './PaginationComponent';
import MessageDisplay from './MessageDisplay';
import './styles/TableComponent.css';

const TableComponent = ({ metadata, tableName }) => {
  const [showForm, setShowForm] = useState(false);
  const [editData, setEditData] = useState(null);
  const [formLoading, setFormLoading] = useState(false);
  const [operationMessage, setOperationMessage] = useState(null);

  // Используем обновленный хук с поддержкой поиска
  const { filteredSortedData, setFilteredSortedData, filters, sortBy, setFilters, setSortBy, loading, total, page, setPage, size, setSize, query, setQuery } = useTableFiltersSort(tableName, [], [], fetchTableData, fetchTableSearchResults);

  const updateTableData = useCallback((newData, isEditing, recordId) => {
    const primaryKeyField = getPrimaryKeyField(metadata);
    if (primaryKeyField) {
      if (isEditing) {
        setFilteredSortedData(prevData =>
          prevData.map(item => item[primaryKeyField.name] === recordId ? newData : item)
        );
      } else {
        setFilteredSortedData(prevData => [newData, ...prevData]);
      }
    } else {
      console.error('Не удалось найти поле первичного ключа.');
    }
  }, [metadata, setFilteredSortedData]);

  const handleAddClick = () => {
    setShowForm(true);
    setEditData(null);
    setFormLoading(false);
  };

  const handleEditClick = useCallback(async (recordId) => {
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
  }, [tableName]);

  const handleFormSubmit = useCallback(async (formData) => {
    try {
      const primaryKeyField = getPrimaryKeyField(metadata);  
      if (!primaryKeyField) {
        throw new Error('Не удалось найти поле первичного ключа.');
      }
  
      const recordId = editData ? editData[primaryKeyField.name] : null;
      const savedRecord = await saveRecord(tableName, formData, !!editData, recordId);
  
      updateTableData(savedRecord, !!editData, savedRecord[primaryKeyField.name]);
      setOperationMessage(`Запись ${editData ? 'обновлена' : 'добавлена'} с ID ${savedRecord[primaryKeyField.name]}`);
      setShowForm(false);
    } catch (error) {
      console.error('Ошибка при сохранении данных:', error);
      setOperationMessage('Ошибка при сохранении данных.');
    }
  }, [metadata, editData, tableName, updateTableData]);

  const handleDeleteClick = useCallback(async (recordId) => {
    try {
      await deleteRecord(tableName, recordId);  
      setFilteredSortedData(prevData => prevData.filter(item => item[metadata.columns.find(column => column.primary_key).name] !== recordId));
      setOperationMessage(`Запись с ID ${recordId} успешно удалена.`);
    } catch (error) {
      console.error('Ошибка при удалении данных:', error);
      setOperationMessage(`Ошибка при удалении записи с ID ${recordId}.`);
    }
  }, [tableName, metadata, setFilteredSortedData]);

  const handlePageChange = (newPage) => {
    setPage(newPage);  
  };

  return (
    <div>
      <div className={showForm ? 'content-hidden' : ''}>
        <header>
          <div className="wrap-logo">
            <a href="/">ГК Синергия</a>
          </div>
          <div>
            <SearchComponent setQuery={setQuery} />  {/* Передаем функцию для обновления запроса */}
          </div>
          <div>
            <button onClick={handleAddClick}>Добавить</button>
          </div>
        </header>
        <MessageDisplay statusMessage={operationMessage} />

        {metadata && metadata.columns && (
          <>
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
                  data={filteredSortedData} 
                  columns={metadata.columns} 
                  onEdit={handleEditClick}
                  onDelete={handleDeleteClick}
                  metadata={metadata}
                />
              </table>
            </div>
          </>
        )}

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

      {showForm && (
        <div className="form-container">
          <EditForm
            onClose={() => setShowForm(false)}
            initialData={editData}
            metadata={metadata}
            formLoading={formLoading}
            isEditing={!!editData}
            onSubmit={handleFormSubmit}
          />
        </div>
      )}
    </div>
  );
};

export default TableComponent;
