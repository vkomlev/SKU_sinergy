import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div>
      <h1>Добро пожаловать на портал ГК Синергия</h1>
      <p>
        Перейдите к просмотру таблицы доставок: 
        <Link to="/import_DBS_delivery"> Import_DBS_Delivery</Link>
      </p>
    </div>
  );
};

export default HomePage;
