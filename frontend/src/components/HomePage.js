import React from 'react';
import { Link } from 'react-router-dom';
import './styles/HomePage.css'

const HomePage = () => {
  return (
    <div>

      <h1 className='text'>Добро пожаловать на портал ГК Синергия</h1>
      <p className='text'>
        Перейдите к просмотру таблицы доставок: 
        <Link to="/import_DBS_delivery"> Import_DBS_Delivery</Link>
      </p>

    </div>

  );
};

export default HomePage;
