import { useState, useEffect } from 'react';
import { TextField } from '@mui/material';
import { fetchTableData } from '../services/api';

const CheckField = ({ label, value, onChange, disabled, error, foreignKey }) => {
    const [loading, setLoading] = useState(false);
    const [fetchError, setFetchError] = useState(null);
    const [displayValue, setDisplayValue] = useState(''); // Значение для отображения

    // Эффект для загрузки значения по ID при изменении value
    useEffect(() => {
        const loadInitialValue = async () => {
            if (!value) return; // Если ID не предоставлен, выходим
            setLoading(true);
            setFetchError(null);

            try {
                const response = await fetchTableData(
                    foreignKey.target_table,
                    1, // Первая страница
                    1000, // Размер страницы
                    [],
                    [{ column: foreignKey.key_field, expression: '=', value }]
                );

                if (response.data && response.data.length > 0) {
                    // Устанавливаем отображаемое значение
                    setDisplayValue(response.data[0][foreignKey.lookup_field]);
                } else {
                    setFetchError('ID не найден');
                    setDisplayValue(''); // Очищаем значение
                }
            } catch (error) {
                console.error('Ошибка при получении значения:', error);
                setFetchError('Ошибка при получении значения');
                setDisplayValue(''); // Очищаем значение
            } finally {
                setLoading(false);
            }
        };

        loadInitialValue(); // Загружаем значение по ID 
    }, [value, foreignKey]);

    // Функция для валидации введенного значения
    const validateValue = async (inputValue) => {
        if (!inputValue) {
            setDisplayValue(''); // Сбрасываем состояние
            return;
        }

        setLoading(true);
        setFetchError(null);

        try {
            const response = await fetchTableData(
                foreignKey.target_table,
                1, // Первая страница
                1000, // Размер страницы
                [],
                [{ column: foreignKey.lookup_field, expression: '=', value: inputValue }] // Поиск по значению
            );

            if (response.data && response.data.length > 0) {
                const fetchedId = response.data[0][foreignKey.key_field]; // Получаем ID
                setDisplayValue(inputValue); // Устанавливаем значение для отображения
                onChange(fetchedId); // Отправляем ID обратно
            } else {
                setFetchError('Значение не найдено');
                setDisplayValue(''); // Очищаем текущее значение
                onChange(''); // Сбрасываем ID
            }
        } catch (error) {
            console.error('Ошибка при валидации значения:', error);
            setFetchError('Ошибка при валидации значения');
            setDisplayValue(''); // Очищаем значение
            onChange(''); // Сбрасываем ID
        } finally {
            setLoading(false);
        }
    };

    // Обработчик для нажатия клавиши
    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            validateValue(displayValue); // Проверяем значение на Enter
        }
    };

    return (
        <>
            <TextField
                label={label}
                value={displayValue} // Отображаем значение
                onChange={(e) => setDisplayValue(e.target.value)} // Устанавливаем состояние
                onKeyDown={handleKeyDown} // Обрабатываем нажатие клавиш
                error={!!error || !!fetchError}
                helperText={fetchError || (error ? error.message : '')}
                disabled={disabled || loading}
                fullWidth
                sx={{
                    '& input': {
                        color: '#e6e6e6',
                        transition: 'background-color 0.2s ease',
                        borderRadius: '5px',
                    },
                    '&:hover input': {
                        backgroundColor: disabled===false ? '' : '#5A567E',
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
                    },
                }}
            />
        </>
    );
};

export default CheckField;