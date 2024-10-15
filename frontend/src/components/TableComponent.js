import React, { useCallback, useState } from 'react';
import { getPrimaryKeyField } from '../utils/tableUtils';
import { deleteRecord, fetchRecord, saveRecord, fetchTableData, fetchTableSearchResults } from '../services/api';  
import { useTableFiltersSort } from '../hooks/useTableFiltersSort';
import { useTableMetadata } from '../hooks/useTableMetadata';  // Импортируем хук метаданных
import SearchComponent from './SearchComponent';
import EditForm from './EditForm';
import DropFilterMenuComponent from './DropFilterMenuComponent';
import TableHeader from './TableHeader';
import TableBody from './TableBody';
import PaginationComponent from './PaginationComponent';
import MessageDisplay from './MessageDisplay';
import FileUploadComponent from './FileUploadComponent';
import './styles/TableComponent.css';

const TableComponent = ({ tableName, onDataReload, ...props }) => {
  const [showForm, setShowForm] = useState(false);
  const [editData, setEditData] = useState(null);
  const [formLoading, setFormLoading] = useState(false);
  const [operationMessage, setOperationMessage] = useState(null);
  const [showUpload, setShowUpload] = useState(false); // Состояние для отображения компонента загрузки
  // Используем хук для метаданных с showView = true для отображения таблицы
  const { metadata: tableMetadata, loadingMetadata: loadingTableMetadata } = useTableMetadata(tableName, true);

  // Используем хук для метаданных с showView = false для формы редактирования
  const { metadata: formMetadata, loadingMetadata: loadingFormMetadata } = useTableMetadata(tableName, false);

  // Используем хук для работы с фильтрами, сортировкой и данными
  const { 
    filteredSortedData, 
    setFilteredSortedData, 
    filters, 
    sortBy, 
    setFilters, 
    setSortBy, 
    loading, 
    total, 
    page, 
    setPage, 
    size, 
    setSize, 
    query, 
    setQuery,
    resetFiltersSort   
  } = useTableFiltersSort(tableName, [], [], fetchTableData, fetchTableSearchResults);

  const updateTableData = useCallback((newData, isEditing, recordId) => {
    const primaryKeyField = getPrimaryKeyField(tableMetadata);
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
  }, [tableMetadata, setFilteredSortedData]);

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
      const primaryKeyField = getPrimaryKeyField(formMetadata);  
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
  }, [formMetadata, editData, tableName, updateTableData]);

  const handleDeleteClick = useCallback(async (recordId) => {
    try {
      await deleteRecord(tableName, recordId);  
      setFilteredSortedData(prevData => prevData.filter(item => item[tableMetadata.columns.find(column => column.primary_key).name] !== recordId));
      setOperationMessage(`Запись с ID ${recordId} успешно удалена.`);
    } catch (error) {
      console.error('Ошибка при удалении данных:', error);
      setOperationMessage(`Ошибка при удалении записи с ID ${recordId}.`);
    }
  }, [tableName, tableMetadata, setFilteredSortedData]);

  const handlePageChange = (newPage) => {
    setPage(newPage);  
  };

  const handleReset = () => {
    resetFiltersSort();  // Сбрасываем фильтры и сортировку
  };

  if (loadingTableMetadata || !tableMetadata) {
    return <div>Загрузка метаданных...</div>;
  }

  const handleUploadSuccess = () => {
    setShowUpload(false);
    // Обновляем таблицу после успешной загрузки данных
    onDataReload();
  };

  const handleCancelUpload = () => {
    setShowUpload(false);  // Закрываем форму при отмене
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
            <button onClick={() => setShowUpload(true)}>Загрузить</button>
          </div>
        </header>
        <MessageDisplay statusMessage={operationMessage} />
        {showUpload && (
        <FileUploadComponent
          tableName={tableName}
          onUploadSuccess={handleUploadSuccess}
          onCancel={handleCancelUpload}  // Обрабатываем отмену загрузки
        />
        )}
        {tableMetadata && tableMetadata.columns && (
          <>
            <DropFilterMenuComponent
              columns={tableMetadata.columns}
              filters={filters}
              setFilters={setFilters}
              resetFiltersSort={resetFiltersSort} 
            />
            <div className='big-table'>
              <table className='table'>
                <TableHeader 
                  columns={tableMetadata.columns} 
                  sortBy={sortBy} 
                  setSortBy={setSortBy} 
                />
                <TableBody 
                  data={filteredSortedData} 
                  columns={tableMetadata.columns} 
                  onEdit={handleEditClick}
                  onDelete={handleDeleteClick}
                  metadata={tableMetadata}
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
            metadata={formMetadata}
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