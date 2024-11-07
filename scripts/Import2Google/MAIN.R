source("GetNewDBS.R", encoding = 'UTF-8')

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

New_DBS_DF <- new("Get.Ozon.New.DBS.Class")

Client_Input_Data <- data.frame(Client_Name  = "ИП Евстафьева О. А.", Client_ID = "1939513", API_KEY = "8345417f-9863-4536-80a8-60d0a478aa75") %>%
                      add_row(.,Client_Name  = "ИП Цициашвили Э. К.", Client_ID = "1939564", API_KEY = "233f3887-9bff-4ee3-903c-b874ceef11ab" )

#-- Датафрейм  выходной таблицы
DBS_Names <- c(DBS_Table@Marketplace_Name,          DBS_Table@Entity_Name,         DBS_Table@Order_ID_Name,
               DBS_Table@SKU_Name,                  DBS_Table@Item_Name,          DBS_Table@Quantity_Name,   DBS_Table@Delivery_Date_Plan_Name,
               DBS_Table@Delivery_Actual_Date_Name, DBS_Table@Delivery_Time_Name, DBS_Table@Delivery_Address_Name,
               DBS_Table@Client_Name,               DBS_Table@Lift_Up_Name,       DBS_Table@Status_Name,     DBS_Table@Deliverer_Name,
               DBS_Table@Mileage_Name,              DBS_Table@Fare_Name,          DBS_Table@NB_Name,         DBS_Table@Compensation_Name, 
               DBS_Table@Difference_Name,           DBS_Table@Reserve_1C_Name)
DBS_Table@DF <- matrix("",nrow = 1, ncol = length(DBS_Names)) %>% as.data.frame(.)
names(DBS_Table@DF) <- DBS_Names

#------------------------------------------------------



for( k in 1:nrow(Client_Input_Data)) {
New_DBS_DF@Client_Name <- Client_Input_Data[k,"Client_Name"]
New_DBS_DF@Client_ID <- Client_Input_Data[k, "Client_ID"]
New_DBS_DF@API_Key   <- Client_Input_Data[k, "API_KEY"]

New_DBS_DF@date_from <- "2024-10-01T00:00:00Z"
New_DBS_DF@date_to   <- "2024-11-30T00:00:00Z"
New_DBS_DF@limit     <- 1000
New_DBS_DF@offset    <- 0
# Делаем запрос к АПИ ОЗОНА и обрабатываем его
message(paste("Запускаем обработку заказов Озона. Клиент:  ",Client_Input_Data[k,"Client_Name"]))
New_DBS_DF       <- Read.Data(x = New_DBS_DF)

# --- теперь готовим таблицу к загрузке для дальнейшего прозвона
if(New_DBS_DF@count != 0) {
  for(i in 1:New_DBS_DF@count ){
    
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Marketplace_Name)]           <- "OZON"
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Entity_Name)]                <-   New_DBS_DF@Client_Name
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Order_ID_Name)]              <- New_DBS_DF@DF[i, which(names(New_DBS_DF@DF)== "posting_number") ]
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@SKU_Name)]                   <- New_DBS_DF@DF$products[[i]][[1]]$offer_id
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Item_Name)]                  <- New_DBS_DF@DF$products[[i]][[1]]$name
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Quantity_Name)]              <- New_DBS_DF@DF$products[[i]][[1]]$quantity # Поле "Количество"
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Delivery_Date_Plan_Name)]    <- New_DBS_DF@DF[i, ]$analytics_data[[1]]$delivery_date_end
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Delivery_Address_Name)]      <- New_DBS_DF@DF[i,]$customer[[1]]$address$address_tail
    DBS_Table@DF[i,which(names(DBS_Table@DF) == DBS_Table@Delivery_Actual_Date_Name)] <- ""
    DBS_Table@DF[i,which(names(DBS_Table@DF) == DBS_Table@Delivery_Time_Name)]        <- ""
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Client_Name)]                <- New_DBS_DF@DF[i,]$customer[[1]]$name
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Delivery_Time_Name)] <- "Автоматическая заливка. Верифицировать"
    selector <- New_DBS_DF@DF[i,"prr_option"][[1]]
    ifelse(selector == "none", DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Lift_Up_Name)]  <- "Не включен", 
           DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Lift_Up_Name)]  <-"Включен")
    
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Status_Name)] <- "Новая"
    DBS_Table@DF[i,which(names(DBS_Table@DF)== DBS_Table@Deliverer_Name)] <- "Акоп"
    # xxx <- DBS_Table@DF # Отладочная переменная
    
    }
  DBS_Table@DF$`Дата доставки` <- lubridate::as_date(DBS_Table@DF$`Дата доставки`)
  
  
  # googlesheets4::write_sheet(XXX, ss =DBS_Table@DBS_Google_URL,  sheet = DBS_Table@DBS_Google_Sheet)
  googlesheets4::sheet_append(ss = DBS_Table@DBS_Google_URL, data= DBS_Table@DF, sheet = DBS_Table@DBS_Google_Sheet)
  DBS_Table@DF <- DBS_Table@DF[0,] # обнуляем датафрейм
  
  } else message("Запрос вернул нулевой результат. Новых отправлений нет.")

}