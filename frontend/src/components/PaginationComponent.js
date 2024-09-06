import React from 'react';
import ReactPaginate from 'react-paginate';

const PaginationComponent = ({ page, pageCount, onPageChange }) => {
  const handlePageClick = (data) => {
    onPageChange(data.selected + 1); // Нумерация страниц начинается с 0, добавляем +1
  };

  return (
    <div>
      <ReactPaginate
        previousLabel={'<'}
        nextLabel={'>'}
        breakLabel={'...'}
        pageCount={pageCount}
        marginPagesDisplayed={2}
        pageRangeDisplayed={5}
        onPageChange={handlePageClick}
        containerClassName={'pagination'}
        activeClassName={'active'}
        forcePage={page - 1}  // Для управления текущей страницей
      />
    </div>
  );
};

export default PaginationComponent;
