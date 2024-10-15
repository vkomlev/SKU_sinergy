import { TextField, Select, MenuItem, InputLabel, FormControl } from '@mui/material'
import LookupField from './LookupField'
import {formatToDateTimeLocal} from './formatToDateTimeLocal'
import {formatToDate} from './formatToDate'
// Компонент поля формы, который рендерит различные типы ввода на основе типа поля и свойства видимости.
const FormField = ({ field, value, onChange, editable, error }) => {
  const inputLabelProps = { shrink: !!value } // Проверяем, есть ли значение для управления меткой
  switch (field.input_type) {
    case 'text':
      return (
        <TextField
          label={field.label} // Метка поля
          value={value} // Текущее значение
          onChange={editable ? onChange : undefined} // Обработчик изменений
          type='text' // Тип поля
          error={!!error} // Указывает, есть ли ошибка
          helperText={error ? error.message : ''} // Сообщение об ошибке
          fullWidth // Полная ширина поля
          placeholder={value ? '' : field.placeholder}  // Показываем placeholder только если нет значения
          InputLabelProps={inputLabelProps} // Устанавливаем свойства метки
          disabled={!editable}
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
    case 'big_text':
      return (
        <TextField
          label={field.label} // Метка поля
          value={value} // Текущее значение
          onChange={editable ? onChange : undefined} // Обработчик изменений
          multiline // Позволяет вводу многострочного текста
          rows={3} // Начальное количество строк
          error={!!error} // Указывает, есть ли ошибка
          helperText={error ? error.message : ''} // Сообщение об ошибке
          fullWidth // Полная ширина поля
          placeholder={value ? '' : field.placeholder} // Показываем placeholder только если нет значения
          InputLabelProps={inputLabelProps} // Устанавливаем свойства метки
          disabled={!editable}
          sx={{
            '& textarea': {
              color : '#e6e6e6',
              transition: 'background-color 0.2s ease',
              borderRadius: '5px',
            },
            '&:hover textarea': {
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
            },
          }}
        />
      )

    case 'number':
      return (
        <TextField
          label={field.label}
          value={value}
          onChange={editable ? onChange : undefined}
          type="number"
          error={!!error}
          helperText={error ? error.message : ''}
          fullWidth
          placeholder={value ? '' : field.placeholder}  // Показываем placeholder только если нет значения
          InputLabelProps={inputLabelProps} // Устанавливаем свойства метки
          disabled={!editable}
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

    case 'date':
      return (
        <TextField
          label={field.label}
          value={value ? formatToDate(value) : ''} // Преобразуем для отображения
          onChange={(e) => {
            const inputValue = e.target.value; // Получаем значение
            const date = new Date(inputValue);  // Создаем новый объект Date с выбранным временем
            onChange({ target: { value: date.toISOString() } });// Отправляем обновленное значение
            }}
          type="date"
          error={!!error}
          helperText={error ? error.message : ''}
          fullWidth
          InputLabelProps={{ ...inputLabelProps, shrink: true }} // Добавляет эффект сжатия метки
          placeholder={value ? '' : field.placeholder}  // Показываем placeholder только если нет значения
          disabled={!editable}
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
    case 'datetime':
      return (
      <TextField
          label={field.label}
          value={value ? formatToDateTimeLocal(value) : ''} // Преобразуем для отображения
          onChange={(e) => {
            const inputValue = e.target.value; // Получаем значение
            const date = new Date(inputValue);  // Создаем новый объект Date с выбранным временем
            date.setHours(date.getHours() + 2);// Добавляем 2 часа для корректного сохранения
            onChange({ target: { value: date.toISOString() } });// Отправляем обновленное значение
            }}
          type="datetime-local"
          error={!!error}
          helperText={error ? error.message : ''}
          fullWidth
          InputLabelProps={{ shrink: true }}
          disabled={!editable}
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
      );
  
    case 'select':
      return (
        <FormControl fullWidth error={!!error} sx={{
          '& .MuiSelect-root': {
            color: '#e6e6e6', 
          },
          '& .MuiInputLabel-root': {
            color: '#e6e6e6', 
          },
          '& .MuiOutlinedInput-root': {
            '& fieldset': {
              borderColor: '#000000', 
            },
          }
        }}>
          <InputLabel {...inputLabelProps}>{field.label}</InputLabel>
          <Select
          value={value}
          onChange={editable ? onChange : undefined}
          disabled={!editable}>
            {field.options?.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      )
  
    case 'lookup':
      return (
        <LookupField
        label={field.label}
        value={value}
        onChange={editable ? onChange : undefined}
        foreignKey={field.foreign_key} // Передаем foreignKey
        inputType={field.input_type} // Передаем inputType
        error={!!error}
        disabled={!editable}
      />
      )
  
    default:
      return null // Возврат null для неподдерживаемых типов
  }
}
  
export default FormField