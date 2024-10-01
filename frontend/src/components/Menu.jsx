import './styles/Menu.css';

export default function Menu({ header, active, setActive, children }) {
  return (
    <div className={active ? 'menu active' : 'menu'} onClick={() => setActive(false)}>
      <div className="menu__content" onClick={e => e.stopPropagation()}>
        <div className="menu__header">{header}</div>
        <ul className="menu__links">
          {children}
        </ul>
      </div>
    </div>
  );
}