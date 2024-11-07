# --- Проверяем, установлены ли требуемые пакеты
#----- Если нет, то устанавливаем их
packages_needed <-c("jsonlite", "googlesheets4","stringr",
                    "tibble","dplyr","lubridate","httr2",
                    "magrittr", "tidyverse")

for (z in packages_needed) {
  
  if (!z %in% installed.packages()) install.packages(z)
  library(z, character.only = TRUE)
}

#------------- Класс для таблицы DBS Доставка ------------------------
GS.Input.Class <- setClass("GS.Input.Class", slots = c(
  URL_GS  = "character", # URL входной Google Sheet таблицы
  Sheet_Name = "character", # Название листа с которого осуществляется импорт
  MarketPlace_Name = "character", #Название столбца Площадка
  Entity = "character", # Название кабинета
  Task_Num = "character", # Номер задания
  SKU = "character", #Артикул
  Item = "character", #Название
  Quantity = "integer", #Количество
  Announced_Date = "character", # Заявленная дата доставки
  Actual_Date= "character", # Актуальная дата доставки
  Time_Interval= "character", #Интервал времени доставки
  Address= "character", # Адрес доставки
  Customer_Name = "character", #ФИО Покупателя и телефон
  Lifting= "character", #  Подъём на этаж
  Deliverer = "character", # Доставщик
  Status = "character", # Статус доставки
  Mileage= "character", # расстояние
  Cost = "character", # Стоимость доставки
  Note = "character", #Примечание
  Compensation = "character", #Сумма компенсации от покупателя
  DF        = "data.frame" #Датафрейм с данными
),

contains = "list")


