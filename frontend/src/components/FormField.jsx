import { TextField, Select, MenuItem, InputLabel, FormControl } from '@mui/material'
import LookupField from './LookupField'
import {formatToDateTimeLocal} from './formatToDateTimeLocal'
// Компонент поля формы, который рендерит различные типы ввода на основе типа поля и свойства видимости.
const FormField = ({ field, value, onChange, error }) => {
  const inputLabelProps = { shrink: !!value } // Проверяем, есть ли значение для управления меткой
  switch (field.input_type) {
    case 'text':
      return (
        <TextField
          label={field.label} // Метка поля
          value={value} // Текущее значение
          onChange={onChange} // Обработчик изменений
          type='text' // Тип поля
          error={!!error} // Указывает, есть ли ошибка
          helperText={error ? error.message : ''} // Сообщение об ошибке
          fullWidth // Полная ширина поля
          placeholder={value ? '' : field.placeholder}  // Показываем placeholder только если нет значения
          InputLabelProps={inputLabelProps} // Устанавливаем свойства метки
          sx={{
            '& input': {
              color: '#e6e6e6',
            },
            '& label': {
              color: '#e6e6e6',
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

    case 'number':
      return (
        <TextField
          label={field.label}
          value={value}
          onChange={onChange}
          type="number"
          error={!!error}
          helperText={error ? error.message : ''}
          fullWidth
          placeholder={value ? '' : field.placeholder}  // Показываем placeholder только если нет значения
          InputLabelProps={inputLabelProps} // Устанавливаем свойства метки
          sx={{
            '& input': {
              color: '#e6e6e6',
            },
            '& label': {
              color: '#e6e6e6',
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
      )

    case 'date':
      return (
        <TextField
          label={field.label}
          value={value}
          onChange={onChange}
          type="date"
          error={!!error}
          helperText={error ? error.message : ''}
          fullWidth
          InputLabelProps={{ ...inputLabelProps, shrink: true }} // Добавляет эффект сжатия метки
          placeholder={value ? '' : field.placeholder}  // Показываем placeholder только если нет значения
          sx={{
            '& input': {
              color: '#e6e6e6',
            },
            '& label': {
              color: '#e6e6e6',
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
          sx={{
            '& input': {
              color: '#e6e6e6',
              },
            '& label': {
              color: '#e6e6e6',
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
            },
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
          <Select value={value} onChange={onChange}>
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
          onChange={onChange}
          lookupTable={field.lookup_table}
          error={!!error}
          placeholder={value ? '' : field.placeholder}  // Показываем placeholder только если нет значения
        />
      )
  
    default:
      return null // Возврат null для неподдерживаемых типов
  }
}
  
export default FormField