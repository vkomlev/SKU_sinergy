import React from 'react';
import './styles/PaginationComponent.css';

const PaginationComponent = ({ page, pageCount, onPageChange }) => {
  // Функция для обработки перехода на предыдущую страницу
  const handlePrevious = () => {
    if (page > 1) {
      console.log('Переход на предыдущую страницу');
      onPageChange(page - 1);
    }
  };

  // Функция для обработки перехода на следующую страницу
  const handleNext = () => {
    if (page < pageCount) {
      console.log('Переход на следующую страницу');
      onPageChange(page + 1);
    }
  };

  return (
    <div className="pagination">
      <button
        className="pagination-button"
        onClick={handlePrevious}
        disabled={page === 1}
      >
        Назад
      </button>
      <span className="pagination-info">
        Страница {page} из {pageCount}
      </span>
      <button
        className="pagination-button"
        onClick={handleNext}
        disabled={page === pageCount}
      >
        Вперед
      </button>
    </div>
  );
};

export default PaginationComponent;
