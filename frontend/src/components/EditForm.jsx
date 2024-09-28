import { useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { Button, Grid, Box, Typography } from '@mui/material';
import FormField from './FormField';
import createValidationSchema from './Validation';
import React from 'react';
import './styles/EditForm.css';

// Компонент формы для отображения и обработки пользовательских данных.

const EditForm = React.memo(({ metadata, defaultValues, onSubmit, onDelete, isEditing, onClose, initialData  }) => {
    // Создаем валидационную схему на основе метаданных
    const validationSchema = createValidationSchema(metadata.columns);

    // Инициализация хуков для управления формой
    const { control, handleSubmit, formState: { errors }, reset } = useForm({
        resolver: yupResolver(validationSchema),
        defaultValues: defaultValues || {},
    });

    useEffect(() => {
        console.log("Полученные данные для формы:", initialData);  // Логируем данные, которые передаем в форму
        reset(initialData);  // Сбрасываем форму с данными для редактирования
      }, [initialData, reset]);

      return (
        <div className="scrollable-form">
        <header className="form-header">
            <Typography variant="h5" gutterBottom align="center">
                {isEditing ? 'Редактировать данные' : 'Добавить данные'}
            </Typography>
            <div>
                <Button className="checkmark-button" onClick={handleSubmit(onSubmit)} aria-label="Сохранить" />
                <Button onClick={onClose} className="close-button-header" aria-label="Закрыть" />
            </div>
            </header>
            <form onSubmit={handleSubmit(onSubmit)}>
                <Grid container spacing={2}>
                    {/* Динамическое создание полей на основе метаданных */}
                    {metadata?.columns?.map((field) => (
                        // Проверяем visible для каждого поля
                        field.visible && (
                            <Grid item xs={12} sm={4} key={field.name}>
                                <Controller
                                    name={field.name}
                                    control={control}
                                    render={({ field: { onChange, onBlur, value }, fieldState: { error } }) => (
                                        <FormField
                                            field={field}
                                            value={value}
                                            onChange={onChange}
                                            onBlur={onBlur}
                                            error={error}
                                        />
                                    )}
                                />
                            </Grid>
                        )
                    ))}
                </Grid>
                <br />
                <Box className="buttons-container">
                    <Button type="submit" variant="contained" color="primary">
                        {isEditing ? 'Сохранить' : 'Добавить'}
                    </Button>
                    {isEditing && (
                        <Button
                            variant="contained"
                            color="secondary"
                            onClick={onDelete}
                        >
                            Удалить
                        </Button>
                    )}
                    {/* Добавляем кнопку закрытия */}
                    <Button variant="outlined" color="default" onClick={onClose} className='close-button'>
                        Закрыть
                    </Button>
                </Box>
            </form>
        </div>
    );
});

export default EditForm;
