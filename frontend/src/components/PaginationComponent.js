import React from 'react';
import './styles/PaginationComponent.css';  // Подключаем стили

const PaginationComponent = ({ page, pageCount, onPageChange }) => {
  // Универсальная функция для изменения страницы
  const changePage = (newPage) => {
    if (newPage > 0 && newPage <= pageCount) {
      console.log(`Changing to page: ${newPage}`);  // Логируем изменение страницы
      onPageChange(newPage);
    }
  };

  const handlePrevious = () => {
    console.log('Previous button clicked');  // Логируем нажатие на кнопку "Назад"
    changePage(page - 1);
  };

  const handleNext = () => {
    console.log('Next button clicked');  // Логируем нажатие на кнопку "Вперед"
    changePage(page + 1);
  };

  return (
    <div className="pagination">
      <button onClick={handlePrevious} disabled={page === 1} className="pagination-button">
        Назад
      </button>
      <span className="pagination-info">
        {page} из {pageCount}
      </span>
      <button onClick={handleNext} disabled={page === pageCount} className="pagination-button">
        Вперед
      </button>
    </div>
  );
};

export default PaginationComponent;
