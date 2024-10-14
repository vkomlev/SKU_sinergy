import { useState, useEffect } from 'react'
import { TextField, MenuItem,  Menu  } from '@mui/material';
import { fetchTableData } from '../services/api'

// Компонент поля ввода с выбором из списка (lookup).
const LookupField = ({ label, value, onChange, inputType, foreignKey, disabled, error }) => {
  const [options, setOptions] = useState([]) 
  const [loading, setLoading] = useState(false) 
  const [fetchError, setFetchError] = useState(null) 
  const [open, setOpen] = useState(false)

  useEffect(() => {

    const loadOptions = async () => {
      setLoading(true) // Устанавливаем состояние загрузки
      setFetchError(null) 
      try {
        if (!foreignKey || !foreignKey.target_table || !foreignKey.target_column || !foreignKey.key_field || !foreignKey.lookup_field) {
          throw new Error('Некорректные данные для лукапа: отсутствует foreign_key')
        }
const response = await fetchTableData(foreignKey.target_table)

      const data = response.data
        setOptions(data) // Устанавливаем загруженные опции
        console.log("Полученные данные для lookup:", data)
      } catch (error) {
        console.error('Ошибка при загрузке опций:', error) // Обработка ошибок
        setFetchError(error.message) 
      } finally {
        setLoading(false) // Завершаем загрузку
      }
    }

    if (inputType === 'lookup' && foreignKey) {
      loadOptions() 
    }
  }, [inputType, foreignKey]) 
  const handleOptionClick = (option) => {
    onChange(option[foreignKey.key_field]);
    setOpen(false);
  };

  // Если inputType не 'lookup' или отсутствует foreignKey, рендерим обычное поле редактирования
  if (inputType !== 'lookup' || !foreignKey) {
    return (
      <TextField
        label={label}
        value={value}
        onChange={onChange}
        error={!!error || !!fetchError}
        helperText={error ? error.message : fetchError}
        disabled={disabled}
        fullWidth
        sx={{
          '& input': {
            color: '#e6e6e6',
            transition: 'background-color 0.2s ease',
            borderRadius: '5px',
          },
          '&:hover input': {
            backgroundColor: disabled ? '': '#5A567E', 
            borderRadius: '5px',
          },
          '& label': {
            color: '#e6e6e6',
          },
          '&:hover label': {
            color: '#346ACF', // Цвет метки при наведении
          },
          '& .MuiInputBase-root': {
            borderColor: '#346ACF', // Цвет границы для поля ввода
            '&:hover fieldset': {
              borderColor: '#346ACF', // Цвет границы при наведении
            },
          },
          '& .MuiOutlinedInput-root': {
            '& fieldset': {
              borderColor: '#000000', // Цвет границы
            },
          }
        }}
      />
    )
  }

  return (
    <TextField
      label={label}
      select
      value={value || ''}
      onChange={(e) => onChange(e.target.value)}
      error={!!error || !!fetchError}
      helperText={error ? error.message : fetchError}
      disabled={disabled}
      fullWidth
      sx={{
        '& label': {
          color: '#e6e6e6',
        },
        '&:hover label': {
          color: '#346ACF', // Цвет метки при наведении
        },
        '& .MuiInputBase-root': {
          borderColor: '#346ACF', // Цвет границы для поля ввода
          '&:hover fieldset': {
            borderColor: '#346ACF', // Цвет границы при наведении
          },
        },
        '& .MuiOutlinedInput-root': {
          '& fieldset': {
            borderColor: '#000000', // Цвет границы
          },
        }
      }}
      SelectProps={{
        MenuProps: {
          PaperProps: {
            style: {
              maxHeight: 250, //устанавливаем максимальную высоту, превышает - появляется прокрутка 
              overflowY: 'auto',
              backgroundColor: '#292839',
              color: '#e6e6e6'
            },
          },
        },
      }}
    >
      {loading ? (
        <MenuItem disabled>Загрузка...</MenuItem>
      ) : options.length > 0 ? (
        options.map((option) => (
          <MenuItem
            key={option[foreignKey.target_column]}
            value={option[foreignKey.key_field]}
            sx={{
              backgroundColor: '#292839',
              '&:hover, &:focus': {
                backgroundColor: '#1a1924',
              },
              '&.Mui-selected': {
                backgroundColor: '#1a1924',
              }
            }}
          >
            <span style={{ color: '#e6e6e6'}}>{option[foreignKey.lookup_field]}</span>
          </MenuItem>
        ))
      ) : (
        <MenuItem disabled>Нет доступных опций</MenuItem>
      )}
    </TextField>
  );
}

export default LookupField;