import {useState} from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import HomePage from './components/HomePage';
import TableComponent from './components/TableComponent';
import './App.css';
import Menu from './components/Menu.jsx';

const App = () => {
  const [isMenuActive, setMenuActive] = useState(false); 
  // Массив объектов, включающих имя таблицы и псевдоним
  const tables = [
    { name: 'main_products', alias: 'Товары' },
    { name: 'main_delivery', alias: 'Доставки DBS' },
  ];

  return (
    <Router>
      <div>
        <div className="menu-button-container">
          <div className="hamburger-icon" onClick={() => setMenuActive(!isMenuActive)}/> {/* Иконка гамбургера */}
        </div>
  
        <Menu active={isMenuActive} setActive={setMenuActive} header={"Выберите данные"}>  {/* Компонент меню */}
          <ul>
            {tables.map((table) => (
              <li key={table.name}>
                <Link to={`/${table.name}`} onClick={() => setMenuActive(false)}>
                  {table.alias} {/* Отображаем псевдоним */}
                </Link>
              </li>
            ))}
          </ul>
        </Menu>

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