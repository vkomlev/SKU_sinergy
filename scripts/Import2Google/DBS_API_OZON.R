# ФОРМИРУЕМ ДАННЫЕ ДЛЯ ЗАЛИВКИ DBS OZON ============================
#=======================================================================

# --- Проверяем, установлены ли требуемые пакеты
#----- Если нет, то устанавливаем их
packages_needed <-c("jsonlite", "googlesheets4","stringr",
                    "tibble","dplyr","lubridate","httr2",
                    "magrittr", "tidyverse")

for (z in packages_needed) {
  
  if (!z %in% installed.packages()) install.packages(z)
  library(z, character.only = TRUE)
}

#--- Описываем объект с названиями полей, чтобы его можно было использовать в кросс-мэпинге

Output.DBS.Class = setClass("Output.DBS.Class", slots = c(
  DBS_Google_URL            = "character", # Адрес гугл-таблицы
  DBS_Google_Sheet          = "character", # Название листа с данными для записи
  Marketplace_Name          = "character", # Название маркетплейса во входном фрейме
  Entity_Name               = "character", # Название кабинета
  Order_ID_Name             = "character", # Номер заказа
  SKU_Name                  = "character", # Артикул
  Item_Name                 = "character",  # Название
  Quantity_Name             = "character", # Количество
  Delivery_Date_Plan_Name   = "character",
  Delivery_Actual_Date_Name = "character", # Актуальная дата доставки
  Delivery_Time_Name        = "character", # Желаемое время доставки
  Delivery_Address_Name     = "character", # Адрес доставки
  Client_Name               = "character", # ФИО Покупателя + телефон
  Lift_Up_Name              = "character", # Подъем на лифте
  Status_Name               = "character", # Статус заказа
  Deliverer_Name            = "character", # Имя доставляльщика
  Mileage_Name              = "character", # Название расстояния
  Fare_Name                 = "character", # Стоимость
  NB_Name                   = "character", # Примечание
  Compensation_Name         = "character", # КОмпенсация
  Difference_Name           = "character", # Разница
  Reserve_1C_Name           = "character", # 1С резерв
  DF                        = "data.frame" # Датафрейм таблицы DBS
), contains = "list" )

DBS_Table <- new("Output.DBS.Class") # Новый экземпляр класса Output.DBS.Class
DBS_Table@DBS_Google_URL <- "https://docs.google.com/spreadsheets/d/1653vVSz3LRsX8nQ7PDlx61JwXaXr9VAcioRROkdfJCM/edit?gid=0#gid=0"
DBS_Table@DBS_Google_Sheet          <- "ГЛАВЛИСТ"
DBS_Table@Marketplace_Name          <- "Площадка"
DBS_Table@Entity_Name               <- "Кабинет"
DBS_Table@Order_ID_Name             <- "Номер заказа"
DBS_Table@SKU_Name                  <- "Артикул"
DBS_Table@Item_Name                 <- "Название"
DBS_Table@Quantity_Name             <- "Количество"
DBS_Table@Delivery_Date_Plan_Name   <- "Дата доставки"
DBS_Table@Delivery_Actual_Date_Name <- "Актуальная дата доставки"
DBS_Table@Delivery_Time_Name        <- "Время доставки"
DBS_Table@Delivery_Address_Name     <- "Адрес доставки"
DBS_Table@Client_Name               <- "ФИО Покупателя, телефон"
DBS_Table@Lift_Up_Name              <- "Подъем на этажи"
DBS_Table@Status_Name               <- "Статус"
DBS_Table@Deliverer_Name            <- "Доставщик"
DBS_Table@Mileage_Name              <- "Расстояние"
DBS_Table@NB_Name                   <- "Примечание"
DBS_Table@Fare_Name                 <- "Стоимость"
DBS_Table@Compensation_Name         <- "Компенсации за доставку от покупателей"
DBS_Table@Difference_Name           <- "Разница"
DBS_Table@Reserve_1C_Name           <- "1С резерв"

DBS_Names <- c(DBS_Table@Marketplace_Name,          DBS_Table@Entity_Name,         DBS_Table@Order_ID_Name,
               DBS_Table@SKU_Name,                  DBS_Table@Item_Name,          DBS_Table@Quantity_Name,   DBS_Table@Delivery_Date_Plan_Name,
               DBS_Table@Delivery_Actual_Date_Name, DBS_Table@Delivery_Time_Name, DBS_Table@Delivery_Address_Name,
               DBS_Table@Client_Name,               DBS_Table@Lift_Up_Name,       DBS_Table@Status_Name,     DBS_Table@Deliverer_Name,
               DBS_Table@Mileage_Name,              DBS_Table@Fare_Name,          DBS_Table@NB_Name,         DBS_Table@Compensation_Name, 
               DBS_Table@Difference_Name,           DBS_Table@Reserve_1C_Name)
DBS_Table@DF <- matrix("",nrow = 1, ncol = length(DBS_Names)) %>% as.data.frame(.)
names(DBS_Table@DF) <- DBS_Names


#___ ТЕСТОВЫЙ ЗАПРОС к ОЗОНУ
ClientID <- "1939513" # Santech.Delivery
API_KEY <- "8345417f-9863-4536-80a8-60d0a478aa75" # АПИ ключ Santech.Delivery (KEY FOR SANTEC.DBS)
# API_KEY <- "7645b972-ad96-4f72-98a5-3568f22caf09" # (KEY FOR KUDRIN)



s <- as.integer(100)

req <- httr2::request("https://api-seller.ozon.ru/v3/posting/fbs/unfulfilled/list") %>% req_headers(., 
                    'Client-Id' = ClientID,
                    'Api-Key'    = API_KEY,
                    'Content-Type' = "application/json") %>% req_method("POST") %>% 
  req_body_json(., list(
  dir = "ASC",
  filter = list(cutoff_from = "2024-10-01T00:00:00Z",
                cutoff_to   = "2024-11-30T00:00:00Z",
                status = "awaiting_packaging"
                ),
  limit = 1000,
  
  offset = as.integer(0),
  
  with = list(analytics_data = TRUE,
              barcodes = TRUE,
              financial_data = TRUE,
              translit = FALSE)
  
)
)

# --- Отправляем запрос

 response <- req %>% req_perform(., verbosity = 3) %>%  httr2::resp_body_json(.)

response_DF <- as.data.frame(do.call(rbind,response$result$postings)) # датафрейм ответа
# --- Забрали с Озона данные о новых заказах (awaiting_packaging)----
# --- теперь готовим таблицу к загрузке для дальнейшего прозвона
if(response$result$count != 0) {
     for(i in 1:response$result$count ){
    
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Marketplace_Name)] <- "OZON"
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Entity_Name)] <- "ИП Евстафьева О. А."
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Order_ID_Name)] <- response_DF[i, which(names(response_DF)== "posting_number") ]
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@SKU_Name)] <- response_DF$products[[i]][[1]]$offer_id
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Item_Name)] <- response_DF$products[[i]][[1]]$name
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Quantity_Name)] <- response_DF$products[[i]][[1]]$quantity
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Delivery_Date_Plan_Name)] <- response_DF[i, ]$analytics_data[[1]]$delivery_date_end
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Delivery_Address_Name)] <- response_DF[i,]$customer[[1]]$address$address_tail
DBS_Table@DF[i,which(names(DBS_Table@DF) == DBS_Table@Delivery_Actual_Date_Name)] <- ""
DBS_Table@DF[i,which(names(DBS_Table@DF) == DBS_Table@Delivery_Time_Name)] <- ""
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Client_Name)] <- response_DF[i,]$customer[[1]]$name
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Delivery_Time_Name)] <- "Автоматическая заливка. Верифицировать"
selector <- response_DF[i,"prr_option"][[1]]
ifelse(selector == "none", DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Lift_Up_Name)]  <- "Не включен", 
                           DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Lift_Up_Name)]  <-"Включен")

DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Status_Name)] <- "Новая"
DBS_Table@DF[i,which(names(DBS_Table@DF)== DBS_Table@Deliverer_Name)] <- "Акоп"


    
  }
  DBS_Table@DF$`Дата доставки` <- lubridate::as_date(DBS_Table@DF$`Дата доставки`)
  
  
  XXX <- DBS_Table@DF
 # googlesheets4::write_sheet(XXX, ss =DBS_Table@DBS_Google_URL,  sheet = DBS_Table@DBS_Google_Sheet)
  googlesheets4::sheet_append(ss =DBS_Table@DBS_Google_URL, data= XXX, sheet = DBS_Table@DBS_Google_Sheet)
  
  
} else print("Запрос вернул нулевой результат. Новых отправлений нет")
