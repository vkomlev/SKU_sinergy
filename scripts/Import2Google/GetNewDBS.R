## GET New DBS Orders from Ozon

# --- Проверяем, установлены ли требуемые пакеты
#----- Если нет, то устанавливаем их
packages_needed <-c("jsonlite", "googlesheets4","stringr",
                    "tibble","dplyr","lubridate","httr2",
                     "tidyverse")

for (z in packages_needed) {
  
  if (!z %in% installed.packages()) install.packages(z)
  library(z, character.only = TRUE)
}

# Описываем объект для запроса данных о новых заказах

Get.Ozon.New.DBS.Class = setClass("Get.Ozon.New.DBS.Class", slots = c(
  Client_Name = "character", #Наименование клиента
  Client_ID = "character", # номер клиента в Озоне
  API_Key   = "character", # API ключ
  date_from = "character", # Дата начала в текстовом формате ISO8601
  date_to   = "character", # Дата окнчания в текстовом формает ISO8601
  limit     = "numeric",   # количество записей в ответе, как правило = 1000
  offset    = "numeric",   # смещение, как правило = 0 
  DF        = "data.frame", # Датафрейм ответа
  count     = "numeric"    # количество записей в ответе
  
), contains = "list" )

# Декларируем метод класса
setGeneric("Read.Data", def = function(x) standardGeneric('Read.Data'))
# Описываем метод класса
setMethod("Read.Data", signature = "Get.Ozon.New.DBS.Class",
          function(x){
            req <- httr2::request("https://api-seller.ozon.ru/v3/posting/fbs/unfulfilled/list") %>% 
              req_headers(.,'Client-Id' = x@Client_ID,
                            'Api-Key'    = x@API_Key,
                            'Content-Type' = "application/json") %>% 
              req_method("POST") %>% 
              req_body_json(., list(
                dir = "ASC",
                filter = list(cutoff_from = x@date_from,
                              cutoff_to   = x@date_to,
                              status = "awaiting_packaging"
                              ),
                limit = x@limit,
                offset = x@offset,
                with = list(analytics_data = TRUE,
                            barcodes = TRUE,
                            financial_data = TRUE,
                            translit = FALSE)
                
              )
              )
            
            # --- Отправляем запрос
            
            response <- req %>% req_perform(., verbosity = 0) %>%  httr2::resp_body_json(.) 
            x@DF <- as.data.frame(do.call(rbind,response$result$postings)) # датафрейм ответа
            x@count <- response$result$count
            
  return(x)
          })

# Описываем класс Get.WB.DBS.Class - для получения новых заказов WB DBS

Get.WB.DBS.Class = setClass("Get.WB.DBS.Class", slots =c(
  
  Client_Name = "character", #Наименование клиента
  API_Key   = "character", # API ключ
  date_from = "character", # Дата начала в текстовом формате Unix Timestamp
  date_to   = "character", # Дата окончания в текстовом формате Unix Timestamp
  next_n    = "numeric",   # пагинация Устанавливает значение, с которого надо получить следующий пакет данных. 
                           # Для получения полного списка данных должен быть равен 0 в первом запросе. 
                           # Для следующих запросов необходимо брать значения из одноимённого поля в ответе.
 
  
  DF        = "data.frame", # Датафрейм ответа
  count     = "numeric"    # количество записей в ответе
))
# === Декларируем метод Read.Data.WB.DBS - читаем новые данные DBS c WB

setGeneric("Read.Data.WB.DBS", def = function(x) standardGeneric('Read.Data.WB.DBS'))

# === Описываем метод Read.Data.WB.DBS
setMethod("Read.Data.WB.DBS", signature = "Get.WB.DBS.Class",
          function(x){
            req <- httr2::request("https://marketplace-api.wildberries.ru/api/v3/orders/new") %>% 
              
              req_headers(.,Authorization = x@API_Key,
                          accept = "application/json") %>% 
              req_method("GET") 
              
              
            
            # --- Отправляем запрос
            
            response <- req %>% req_perform(., verbosity = 3) %>%  httr2::resp_body_json(.) 
            
            
            return(response)
          })
