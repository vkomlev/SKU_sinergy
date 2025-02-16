source("GetNewDBS_v2.R", encoding = 'UTF-8')

Output.DBS.Class = setClass("Output.DBS.Class", slots = c(
  DBS_Google_URL            = "character", # Адрес гугл-таблицы
  DBS_Google_Sheet          = "character", # Название листа с данными для записи
  Marketplace_Name          = "character", # Название маркетплейса во входном фрейме
  Entity_Name               = "character", # Название кабинета
  Order_ID_Name             = "character", # Номер заказа
  Order_ID_Google_Range     = "character", #  Столбец Google-таблицы с номером заказа
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
  Compensation_Name         = "character", # Компенсация
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
DBS_Table@Order_ID_Google_Range     <- "C:C"
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

Client_Finance_Data <- Client_Input_Data %>% add_row(.,Client_Name  = "ИП Кудрин В.В.", Client_ID = "2203553", API_KEY = "bdfe541e-98a9-45ef-a94d-4a17109c2577" )

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
# Приводим дату к виду, который нравится Озону в формате UTC   
New_DBS_DF@date_from <- paste(as.character(today()-14), "T00:00:00Z", sep="")
New_DBS_DF@date_to   <- paste(as.character(today()+5), "T00:00:00Z", sep="")
New_DBS_DF@limit     <- 1000
New_DBS_DF@offset    <- 0
New_DBS_DF@count <- 0
New_DBS_DF@method <- "ready" # Запрашиваем готовые к отгрузке отправления
# Делаем запрос к АПИ ОЗОНА и обрабатываем его
message(paste("Запускаем обработку заказов Озона. Клиент:  ",Client_Input_Data[k,"Client_Name"]))
New_DBS_DF      <- Read.Data(x = New_DBS_DF)

# --- теперь готовим таблицу к загрузке для дальнейшего прозвона
if(New_DBS_DF@count != 0) {
  for(i in 1:New_DBS_DF@count ){
    # Подтягиваем контакты клиента и стоимость доставки отдельным запросом
    temp_DBS <- New_DBS_DF
    temp_DBS@method <- "get"
    # Получаем номер отправления
    temp_DBS@single_posting <- as.character(New_DBS_DF@DF[i, which(names(New_DBS_DF@DF)== "posting_number") ])
    temp_DBS <- Read.Data((temp_DBS))
    
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Marketplace_Name)]           <- "OZON"
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Entity_Name)]                <-   New_DBS_DF@Client_Name
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Order_ID_Name)]              <- New_DBS_DF@DF[i, which(names(New_DBS_DF@DF)== "posting_number") ]
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@SKU_Name)]                   <- New_DBS_DF@DF$products[[i]][[1]]$offer_id
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Item_Name)]                  <- New_DBS_DF@DF$products[[i]][[1]]$name
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Quantity_Name)]              <- New_DBS_DF@DF$products[[i]][[1]]$quantity # Поле "Количество"
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Delivery_Date_Plan_Name)]    <- New_DBS_DF@DF[i, ]$analytics_data[[1]]$delivery_date_end
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Delivery_Address_Name)]      <- New_DBS_DF@DF[i,]$customer[[1]]$address$address_tail
    DBS_Table@DF[i,which(names(DBS_Table@DF) == DBS_Table@Delivery_Actual_Date_Name)] <- ""
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Client_Name)]                <- paste(temp_DBS@DF$addressee[[1]][["name"]], paste(" Телефон (подменный): +", paste(
                                                                                               substr(temp_DBS@DF$addressee[[1]][["phone"]],1,1),
                                                                                               substr(temp_DBS@DF$addressee[[1]][["phone"]],2,4),
                                                                                               substr(temp_DBS@DF$addressee[[1]][["phone"]],5,7),
                                                                                               substr(temp_DBS@DF$addressee[[1]][["phone"]],8,9),
                                                                                               substr(temp_DBS@DF$addressee[[1]][["phone"]],10,11),sep = "-"), sep = ""),sep ="\n")
    
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Delivery_Time_Name)] <- "Автоматическая заливка. Верифицировать"
    selector <- New_DBS_DF@DF[i,"prr_option"][[1]]
    ifelse(selector == "none", DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Lift_Up_Name)]  <- "Не включен", 
           DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Lift_Up_Name)]  <-"Включен")
    
    DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Status_Name)] <- "Новая"
   DBS_Table@DF[i,which(names(DBS_Table@DF)== DBS_Table@Deliverer_Name)] <- "Акоп"
    # Расстояние от МКАД
    
DBS_Table@DF[i, which(names(DBS_Table@DF) == DBS_Table@Mileage_Name)]  <- paste('{"lat" : ',New_DBS_DF@DF[i,]$customer[[1]]$address$latitude, ', "lng" :',
          New_DBS_DF@DF[i,]$customer[[1]]$address$longitude,"}", sep='') %>% Get.Distance.from.MKAD(., precision = 3 )
    
    DBS_Table@DF[i, which(names(DBS_Table@DF) == DBS_Table@Compensation_Name)] <- temp_DBS@DF$delivery_price[[1]] %>% as.integer(.)
   
    }
  DBS_Table@DF$`Дата доставки` <- lubridate::as_date(DBS_Table@DF$`Дата доставки`)
  
  
  # ниже SSS - отладка
  # SSS <- DBS_Table@DF
  message("Получаем данные по уже заведенным заказам")
  Existing_Orders <- as.data.frame(googlesheets4::range_read(ss = DBS_Table@DBS_Google_URL, sheet = DBS_Table@DBS_Google_Sheet,range = DBS_Table@Order_ID_Google_Range))
  DBS_Table@DF <- datawizard::data_merge(DBS_Table@DF, Existing_Orders, by = "Номер заказа", join = "anti")
  
  
  
  if(!is.na(DBS_Table@DF$Артикул[1])) googlesheets4::sheet_append(ss = DBS_Table@DBS_Google_URL, data= DBS_Table@DF, sheet = DBS_Table@DBS_Google_Sheet)
  

   DBS_Table@DF <- DBS_Table@DF[0,] # обнуляем датафрейм
  
  } else message("Запрос DBS OZON вернул нулевой результат. Новых отправлений нет.")

}

# Запускаем просмотр заданий WB

message("Начинаем проверку заданий Вайлдберриз")

WB_Input_Data <- data.frame(Client_Name = "ИП Цициашвили Э. К.", API_KEY = "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQxMTE4djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc0ODkxNTA2NSwiaWQiOiIwMTkzODc5ZC03ZTdlLTczOWEtODg3Zi1jNWZhNWZiYmVjZWMiLCJpaWQiOjIzMjk2OTk1LCJvaWQiOjE0MDI3MjEsInMiOjc5MzQsInNpZCI6IjBiZjJlNjcyLWQyY2MtNGM4MC1iNzNmLTYzYTY2YmJlMmM2OSIsInQiOmZhbHNlLCJ1aWQiOjIzMjk2OTk1fQ.CeGQSeh7oOvjorAFwZw7Ib_LGH9Fdw0eAUnVApKZ1PjCUX5OYhjQIEz-5cbtEegc47PPBjqCXuEI_ud-wotmuw")


for( k in 1:nrow(WB_Input_Data)){
  message(paste("Запускаем обработку заказов Wildberries. Клиент: ", WB_Input_Data[k,1]))
  WB.DBS <- Get.DBS.From.WB(WB_Input_Data[k,"API_KEY"], as.character(Sys.Date()-10), as.character(Sys.Date()+2))

#Заполняем АКОП-Таблицу

if(nrow(WB.DBS) != 0) {
for( i in 1:nrow(WB.DBS)) {
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Marketplace_Name)]   <- "Wildberries"
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Entity_Name)]        <- WB_Input_Data[k,1]
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Order_ID_Name)]      <- WB.DBS[i, "id"]
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@SKU_Name)]           <- WB.DBS[i, "article"]
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Item_Name)]          <- WB.DBS[i, "ItemName"]
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Quantity_Name)]              <- 1 # На WB количество всегда = 1 в одном заказе
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Delivery_Date_Plan_Name)]    <- WB.DBS[i,"createdAt"]
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Delivery_Address_Name)]      <- WB.DBS[i,"address"][[1]]$fullAddress
DBS_Table@DF[i,which(names(DBS_Table@DF) == DBS_Table@Delivery_Actual_Date_Name)] <- ""
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Delivery_Time_Name)]         <- "Автоматическая заливка. Верифицировать"
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Client_Name)]                <- paste(WB.DBS[i, "firstName"], WB.DBS[i, "fullName"], 
  paste( " Телефон (подменный): ", paste(
  substr(WB.DBS[i,"phone"],1,2),
  substr(WB.DBS[i,"phone"],3,5),
  substr(WB.DBS[i,"phone"],6,8),
  substr(WB.DBS[i,"phone"],9,10),
  substr(WB.DBS[i,"phone"],11,12),sep = "-"), sep = ""),
  paste("доп.: ",WB.DBS[i,"phoneCode"]),sep ="\n")

DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Lift_Up_Name)]     <-   "Включен" # На ВБ подъем всегда включен в стоимость
DBS_Table@DF[i, which(names(DBS_Table@DF)==DBS_Table@Status_Name)]      <- "Новая"
DBS_Table@DF[i,which(names(DBS_Table@DF)== DBS_Table@Deliverer_Name)]   <- "Акоп"
  
# Расстояние от МКАД

DBS_Table@DF[i, which(names(DBS_Table@DF) == DBS_Table@Mileage_Name)]  <- paste('{"lat" : ',WB.DBS[i, "address"][[1]]$latitude, ', "lng" :',
                                                                                WB.DBS[i, "address"][[1]]$longitude,"}", sep='') %>% Get.Distance.from.MKAD(., precision = 7 )
  

}
  DBS_Table@DF$`Дата доставки` <- lubridate::as_date(DBS_Table@DF$`Дата доставки`)
  
  # Считываем диапазон заказов, уже имеющихся в таблице
  
  message("Получаем данные по уже заведенным заказам")
  Existing_Orders <- as.data.frame(googlesheets4::range_read(ss = DBS_Table@DBS_Google_URL, sheet = DBS_Table@DBS_Google_Sheet,range = DBS_Table@Order_ID_Google_Range))
  DBS_Table@DF <- data_merge(DBS_Table@DF, Existing_Orders, by = "Номер заказа", join = "anti")
  
  # ниже SSS - отладка
  # SSS <- DBS_Table@DF
  
  if(!is.na(DBS_Table@DF$Артикул[1])) googlesheets4::sheet_append(ss = DBS_Table@DBS_Google_URL, data= DBS_Table@DF, sheet = DBS_Table@DBS_Google_Sheet)
  
} else message("Запрос DBS Wildberries вернул нулевой результат. Новых отправлений нет.")

}