import React from 'react';
import { Link } from 'react-router-dom';
import { runRScript } from '../services/api'; // Import the function to trigger R script
import './styles/HomePage.css'

const HomePage = () => {
  const tables = [
    { name: 'main_products', alias: 'Товары' },
    { name: 'main_delivery', alias: 'Доставки DBS' },
  ];

  const handleRunRScript = async () => {
    try {
      const scriptPath = 'scripts/Import2Google/MAIN.R'; // Путь к скрипту
      const result = await runRScript(scriptPath);
      
      // Показываем только параметр output из успешного ответа
      if (result && result.output) {
        alert(`Результат выполнения R-скрипта: ${result.output}`);
      } else {
        alert('R-скрипт выполнен, но отсутствует параметр output в ответе.');
      }
    } catch (error) {
      // Обрабатываем ошибку и показываем параметр message
      if (error.response && error.response.data && error.response.data.message) {
        alert(`Ошибка: ${error.response.data.message}`);
      } else {
        alert('Произошла ошибка при запуске R-скрипта. Подробности в консоли.');
      }
    }
  };
  

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
                  {table.alias}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </p>
      <button onClick={handleRunRScript}>Запустить R-скрипт</button> {/* Add button */}
    </div>
  );
};

export default HomePage;
