import { useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { Button, Grid } from '@mui/material';
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
            <form onSubmit={handleSubmit(onSubmit)}>
                <Grid container spacing={2}>
                    {/* Динамическое создание полей на основе метаданных */}
                    {metadata?.columns?.map((field) => (
                        <Grid item xs={12} sm={6} key={field.name}>
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
                    ))}
                </Grid>
                <br />
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
                <Button variant="outlined" color="default" onClick={onClose}>
                Закрыть
                </Button>
            </form>
        </div>
    );
});

export default EditForm;
