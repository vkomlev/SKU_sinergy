import * as Yup from 'yup'

// Создает схему валидации на основе полей формы.

const createValidationSchema = (fields) => {
    const schemaFields = {}

    // Итерируемся по всем полям и создаем соответствующую валидацию
    fields?.forEach(field => {
        let fieldValidation 

        // Валидация для целочисленных значений
        if (field.type === 'integer') {
            fieldValidation = Yup.number()
                .typeError(`${field.label} должно быть числом.`) // Сообщение об ошибке для неверного типа

            // Если поле обязательное
            if (field.required) {
                fieldValidation = fieldValidation.required(`Это поле обязательно для заполнения.`)
            }

            // Условия для минимального и максимального значения
            if (field.min) {
                fieldValidation = fieldValidation.min(field.min, `Значение должно быть не меньше, чем ${field.min}.`)
            }
            if (field.max) {
                fieldValidation = fieldValidation.max(field.max, `Значение должно быть не больше, чем ${field.max}.`)
            }
        } else {
            // Валидация для строковых значений (включая URL и Email)
            fieldValidation = Yup.string()

            // Проверка на обязательность
            if (field.required) {
                fieldValidation = fieldValidation.required(`Это поле обязательно для заполнения.`)
            }

            // Проверка на корректность URL
            if (field.url) {
                fieldValidation = fieldValidation.url(`Неверный формат URL.`)
            }

            // Проверка на корректность Email
            if (field.type === 'email') {
                fieldValidation = fieldValidation.email('Неверный формат электронной почты.')
            }
        }


        schemaFields[field.name] = fieldValidation
    })

    // Возврат полной схемы валидации
    return Yup.object().shape(schemaFields)
}

export default createValidationSchema
