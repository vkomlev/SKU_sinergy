import React from 'react';
import { Link } from 'react-router-dom';
import './styles/HomePage.css'

const HomePage = () => {
  const tables = [
    { name: 'main_products', alias: 'Товары' },
    { name: 'main_delivery', alias: 'Доставки DBS' },
  ];
  return (
    <div>

      <h1 className='text'>Добро пожаловать на портал ГК Синергия</h1>
      <p className='text'>
        <h2>Перейдите к просмотру данных:</h2> 
        <div className='content'>
          <ul>
            {tables.map((table) => (
              <li key={table.name}>
                <Link to={`/${table.name}`}>
                  {table.alias} {/* Отображаем псевдоним */}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </p>

    </div>

  );
};

export default HomePage;
