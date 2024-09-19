import { useState, useEffect } from 'react'
import { TextField, MenuItem } from '@mui/material'
import { fetchLookupOptions } from '../services/api'

// Компонент поля ввода с выбором из списка (lookup).

const LookupField = ({ label, value, onChange, lookupTable, error }) => {
  const [options, setOptions] = useState([]) 
  const [loading, setLoading] = useState(false) 

  useEffect(() => {
    /**
     * Загружает опции выбора из API на основе lookupTable.
     */
    const loadOptions = async () => {
      setLoading(true) // Устанавливаем состояние загрузки

      try {
        const data = await fetchLookupOptions(lookupTable) 
        setOptions(data) // Устанавливаем загруженные опции
      } catch (error) {
        console.error('Ошибка при загрузке опций:', error) // Обработка ошибок
      } finally {
        setLoading(false) // Завершаем загрузку
      }
    }

    loadOptions() 
  }, [lookupTable]) 

  return (
    <TextField
      label={label} 
      select 
      value={value}
      onChange={onChange} 
      error={!!error} 
      helperText={error ? error.message : ''} 
      fullWidth 
    >
      {loading ? (
        <MenuItem disabled>Загрузка...</MenuItem> // Показать индикатор загрузки
      ) : (
        options.map((option) => (
          <MenuItem key={option.value} value={option.value}> // Отображение опций
            {option.label}
          </MenuItem>
        ))
      )}
    </TextField>
  )
}

export default LookupField