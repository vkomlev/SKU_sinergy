import { TextField, Select, MenuItem, InputLabel, FormControl } from '@mui/material'
import LookupField from './LookupField'

// Компонент поля формы, который рендерит различные типы ввода на основе типа поля.

const FormField = ({ field, value, onChange, error }) => {
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
          InputLabelProps={{ shrink: true }} // Добавляет эффект сжатия метки
          placeholder={value ? '' : field.placeholder}  // Показываем placeholder только если нет значения
        />
      )

    case 'select':
      return (
        <FormControl fullWidth error={!!error}>
          <InputLabel>{field.label}</InputLabel>
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