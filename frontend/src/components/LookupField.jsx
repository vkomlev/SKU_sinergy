import { useState, useEffect } from 'react';
import { TextField, MenuItem } from '@mui/material';
import { fetchTableData } from '../services/api';

// Компонент поля ввода с выбором из списка (lookup).
const LookupField = ({ label, value, onChange, inputType, foreignKey, disabled, error }) => {
  const [options, setOptions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fetchError, setFetchError] = useState(null);

  const loadAllOptions = async () => {
    setLoading(true);
    setFetchError(null);

    try {
      if (!foreignKey || !foreignKey.target_table || !foreignKey.key_field || !foreignKey.lookup_field) {
        throw new Error('Некорректные данные для лукапа: отсутствует foreign_key');
      }

      let allData = [];
      let currentPage = 1;
      let hasMoreData = true;
      const pageSize = 20; // Размер страницы, можно изменить при необходимости

      while (hasMoreData) {
        const response = await fetchTableData(foreignKey.target_table, currentPage, pageSize);
        allData = [...allData, ...response.data];

        if (response.data.length < pageSize) {
          hasMoreData = false; // Если полученные данные меньше размера страницы, заканчиваем загрузку
        } else {
          currentPage += 1; // Переходим к следующей странице
        }
      }

      setOptions(allData); // Устанавливаем загруженные опции
      console.log("Полученные данные для lookup:", allData);
    } catch (error) {
      console.error('Ошибка при загрузке опций:', error); // Обработка ошибок
      setFetchError(error.message);
    } finally {
      setLoading(false); // Завершаем загрузку
    }
  };

  useEffect(() => {
    if (inputType === 'lookup' && foreignKey) {
      loadAllOptions();
    }
  }, [inputType, foreignKey]);

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
            backgroundColor: disabled ? '' : '#5A567E',
            borderRadius: '5px',
          },
          '& label': {
            color: '#e6e6e6',
          },
          '&:hover label': {
            color: '#346ACF',
          },
          '& .MuiInputBase-root': {
            borderColor: '#346ACF',
            '&:hover fieldset': {
              borderColor: '#346ACF',
            },
          },
          '& .MuiOutlinedInput-root': {
            '& fieldset': {
              borderColor: '#000000',
            },
          }
        }}
      />
    );
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
          color: '#346ACF',
        },
        '& .MuiInputBase-root': {
          borderColor: '#346ACF',
          '&:hover fieldset': {
            borderColor: '#346ACF',
          },
        },
        '& .MuiOutlinedInput-root': {
          '& fieldset': {
            borderColor: '#000000',
          },
        }
      }}
      SelectProps={{
        MenuProps: {
          PaperProps: {
            style: {
              maxHeight: 350,
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
            key={option[foreignKey.key_field]}
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