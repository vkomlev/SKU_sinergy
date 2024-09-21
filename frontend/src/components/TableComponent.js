import React, { useEffect, useMemo, useState } from 'react';
import { applySort, applyFilters } from '../utils/tableUtils';
import { deleteRecord, fetchRecord, saveRecord } from '../services/api';
import SearchComponent from './SearchComponent';
import EditForm from './EditForm';
import DropFilterMenuComponent from './DropFilterMenuComponent';
import TableHeader from './TableHeader';
import TableBody from './TableBody';
import PaginationComponent from './PaginationComponent';
import MessageDisplay from './MessageDisplay';
import './styles/TableComponent.css';

const TableComponent = ({ data, localData, metadata, page, setPage, size, setSize, total, sortBy, setSortBy, filters, setFilters, query, setQuery, loading, loadingMetadata, error, columns, tableName }) => {

  const [showForm, setShowForm] = useState(false);
  const [editData, setEditData] = useState(null);
  const [formLoading, setFormLoading] = useState(false);
  const [tableData, setTableData] = useState(data || []);  // Локальное состояние для данных таблицы
  const [operationMessage, setOperationMessage] = useState(null); // Состояние для хранения сообщения


  useEffect(() => {
    setTableData(data);  // Обновляем локальные данные при загрузке с сервера
  }, [data]);

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
      const record = await fetchRecord(tableName, recordId);  // Запрос на получение данных записи
      setEditData(record);
      setShowForm(true);
      setFormLoading(false);
    } catch (error) {
      console.error('Ошибка при загрузке данных для редактирования:', error);
      setFormLoading(false);
    }
  };

  // Обработка добавления/редактирования записи
  const handleFormSubmit = async (formData) => {
    console.log("Форма отправлена с данными:", formData);
    try {
      const isEditing = !!editData;  // Определяем, идет ли процесс редактирования
      
      // Получаем имя поля, которое является первичным ключом из метаданных
      const primaryKeyField = metadata.columns.find(column => column.primary_key);
      const recordId = isEditing && primaryKeyField ? editData[primaryKeyField.name] : null;
  
      console.log("ID записи для редактирования:", recordId);
  
      // Сохранение записи
      const savedRecord = await saveRecord(tableName, formData, isEditing, recordId);  // API-запрос
  
      // Проверяем, что у новой записи есть ID
      const newRecordId = savedRecord[primaryKeyField.name];
      if (!newRecordId) {
        console.error("Ошибка: У новой записи нет ID.");
        setOperationMessage('Ошибка при добавлении новой записи. ID не получен.');
        return;
      }
  
      // Обновляем таблицу в зависимости от того, добавляется или редактируется запись
      if (isEditing) {
        // Редактирование записи: находим запись в локальном состоянии и обновляем её
        setTableData(prevData =>
          prevData.map(item => item[primaryKeyField.name] === recordId ? savedRecord : item)
        );
        setOperationMessage(`Запись с ID ${recordId} успешно обновлена.`);
      } else {
        // Добавление новой записи: добавляем её в локальное состояние
        setTableData(prevData => [savedRecord, ...prevData]);
        setOperationMessage(`Запись успешно добавлена с ID ${newRecordId}.`);
      }
  
      setShowForm(false);
    } catch (error) {
      console.error('Ошибка при сохранении данных:', error);
      setOperationMessage('Ошибка при сохранении данных.');
    }
  };
  
  

  // Удаление записи
  const handleDeleteClick = async (recordId) => {
    try {
      await deleteRecord(tableName, recordId);  // Удаление записи через API
  
      // Удаляем запись из локального состояния
      setTableData(prevData => prevData.filter(item => item[metadata.columns.find(column => column.primary_key).name] !== recordId));
      setOperationMessage(`Запись с ID ${recordId} успешно удалена.`);
    } catch (error) {
      console.error('Ошибка при удалении данных:', error);
      setOperationMessage(`Ошибка при удалении записи с ID ${recordId}.`);
    }
  };
  
  

  const handlePageChange = (newPage) => {
    console.log('Page changed to:', newPage);
    setPage(newPage);  
  };

  // Обработка данных с учётом наличия метаданных
  const processedData = useMemo(() => {
    if (loading || loadingMetadata || !metadata || !metadata.columns) {
      console.log('Using locally sorted data during loading state');
      return applySort(applyFilters(localData || [], filters), sortBy);
    }
    console.log('Processing server data with filters and sorting');
    return applySort(applyFilters(tableData || [], filters), sortBy);
  }, [tableData, localData, filters, sortBy, loading, loadingMetadata, metadata]);

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
        <MessageDisplay statusMessage={operationMessage} />
        {/* Проверяем наличие колонок перед рендерингом элементов таблицы */}
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
                  data={processedData} 
                  columns={metadata.columns} 
                  onEdit={handleEditClick}
                  onDelete={handleDeleteClick}
                  metadata={metadata}  // Передаём метаданные для получения ключа
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

      {/* Отображаем форму поверх остальных элементов */}
      {showForm && (
        <div className="form-container">
          <EditForm
            onClose={() => setShowForm(false)}
            initialData={editData}  // Передаём данные для редактирования в форму
            metadata={metadata}
            formLoading={formLoading}
            isEditing={!!editData}  // Передаём флаг isEditing: true, если есть данные для редактирования
            onSubmit={handleFormSubmit}
          />
        </div>
      )}
    </div>
  );
};

export default TableComponent;
