import { useState, useEffect } from 'react'
import { TextField, MenuItem } from '@mui/material'
import { fetchTableData } from '../services/api'

// Компонент поля ввода с выбором из списка (lookup).
const LookupField = ({ label, value, onChange, inputType, foreignKey, editable, error }) => {
  const [options, setOptions] = useState([]) 
  const [loading, setLoading] = useState(false) 
  const [fetchError, setFetchError] = useState(null) 

  useEffect(() => {

    const loadOptions = async () => {
      setLoading(true) // Устанавливаем состояние загрузки
      setFetchError(null) 
      try {
        if (!foreignKey || !foreignKey.target_table || !foreignKey.target_column || !foreignKey.key_field || !foreignKey.lookup_field) {
          throw new Error('Некорректные данные для лукапа: отсутствует foreign_key')
        }

        const data = await fetchTableData(foreignKey.target_table) 
        setOptions(data) // Устанавливаем загруженные опции
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
  }, [inputType, foreignKey]) // Зависимости изменены, чтобы добавлять foreignKey

  // Если inputType не 'lookup' или отсутствует foreignKey, рендерим обычное поле редактирования
  if (inputType !== 'lookup' || !foreignKey) {
    return (
      <TextField
        label={label}
        value={value}
        onChange={onChange}
        error={!!error || !!fetchError}
        helperText={error ? error.message : fetchError}
        disabled={!editable}
        fullWidth
        sx={{
          '& input': {
            color: '#e6e6e6',
            transition: 'background-color 0.2s ease',
            borderRadius: '5px',
          },
          '&:hover input': {
            backgroundColor: editable ? '': '#5A567E', 
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
      value={value}
      onChange={onChange}
      error={!!error || !!fetchError}
      helperText={error ? error.message : fetchError}
      disabled={!editable}
      fullWidth
      sx={{
        '& input': {
          color: '#e6e6e6',
          transition: 'background-color 0.2s ease',
          borderRadius: '5px',
        },
        '&:hover input': {
          backgroundColor: editable ? '': '#5A567E', 
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
    >
      {loading ? (
        <MenuItem disabled>Загрузка...</MenuItem>
      ) : options.length > 0 ? (
        options.map((option) => (
          <MenuItem key={option[foreignKey.key_field]} value={option[foreignKey.key_field]}>
            {option[foreignKey.lookup_field]}
          </MenuItem>
        ))
      ) : (
        <MenuItem disabled>Нет доступных опций</MenuItem>
      )}
    </TextField>
  )
}

export default LookupField