import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import HomePage from './components/HomePage';
import TableComponent from './components/TableComponent';
import './App.css';

const App = () => {
  // Массив объектов, включающих имя таблицы и псевдоним
  const tables = [
    { name: 'import_DBS_delivery', alias: 'Импорт Доставка DBS' },
    { name: 'import_orders_ozon', alias: 'Импорт Заказы OZON' },
    { name: 'third_table', alias: 'Третья таблица' }
  ];

  return (
    <Router>
      <div>
        <nav>
          <ul>
            {tables.map((table) => (
              <li key={table.name}>
                <Link to={`/${table.name}`}>{table.alias}</Link> {/* Отображаем псевдоним */}
              </li>
            ))}
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<HomePage />} />
          {tables.map((table) => (
            <Route
              key={table.name}
              path={`/${table.name}`}
              element={<TableComponentWrapper tableName={table.name} />}
            />
          ))}
        </Routes>
      </div>
    </Router>
  );
};

// Обертка для TableComponent, передающая имя таблицы
const TableComponentWrapper = ({ tableName }) => {
  return <TableComponent tableName={tableName} />;
};

export default App;
