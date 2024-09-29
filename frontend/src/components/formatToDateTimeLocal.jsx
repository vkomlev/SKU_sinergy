export const formatToDateTimeLocal = (isoString) => {
    const date = new Date(isoString);
    date.setHours(date.getHours() - 2);// Вычитаем 2 часа для корректности
    // Получаем нужные компоненты
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); 
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    // Форматируем строку в формате YYYY-MM-DDTHH:MM
    return `${year}-${month}-${day}T${hours}:${minutes}`;
};