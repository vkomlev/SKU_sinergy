export const formatToDate = (isoString) => {
    const date = new Date(isoString);
    // Получаем нужные компоненты
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); 
    const day = String(date.getDate()).padStart(2, '0');
    // Форматируем строку в формате YYYY-MM-DD
    return `${year}-${month}-${day}`
}