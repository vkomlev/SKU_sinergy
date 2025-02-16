## GET New DBS Orders from Ozon

# --- Проверяем, установлены ли требуемые пакеты
#----- Если нет, то устанавливаем их
packages_needed <-c("jsonlite", "googlesheets4","stringr",
                    "tibble","dplyr","lubridate","httr2",
                     "tidyverse","remotes", "datawizard","utc")

for (z in packages_needed) {
  
  if (!z %in% installed.packages()) install.packages(z)
  library(z, character.only = TRUE)
}
# Пропишем пути к методам Озон в векторе OZON_API_Methods_Path

OZON_API_Methods_Paths <- c(get         = "https://api-seller.ozon.ru/v3/posting/fbs/get",
                            unfulfilled = "https://api-seller.ozon.ru/v3/posting/fbs/unfulfilled/list",
                            all_fbs     = "https://api-seller.ozon.ru/v3/posting/fbs/list",
                            all_finance = "https://api-seller.ozon.ru/v3/finance/transaction/list" # Данные по начислениям ОЗОНА
                            )
# Функция, которая считает расстояния от МКАДА до населенного пункта
Get.Distance.from.MKAD <- function(locate, precision){
  distance <- -100
  if(!missing(locate)) {
    
    if(missing(precision)) { 
      precision <- 3 }
    req <-  httr2::request("https://synergyia.ru/api/mkad_distance") %>% 
      req_method(., "POST") %>%
      req_url_query(., location= locate, key_max = precision)
    
    
    response <- req %>% req_perform(., verbosity = 0) %>%  httr2::resp_body_json(.) 
    distance <- round(response$distance/1000,0)
  }
  return(distance)
}


# ФУНКЦИЯ, которая запрашивает у WB список всех артикулов, заведенных на аккаунт с ключом APIKEY

GET.All.WB.SKUs <- function(API_KEY) {
result <- NULL
.DF_names <- c("nmID", "vendorCode", "discount","clubDiscount","price")

if(!missing(API_KEY)) {
# Делаем последовательные запросы к WB, потому что метод не возвращает свыше 1000 записей
.limit <- 1000
.offset <- 0
WB.SKU.DF <- NULL
n <- 1
repeat {
# Первый запрос
req_all_SKUs <- httr2::request("https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter") %>% 
                req_headers(.,Authorization = API_KEY,accept = "application/json") %>%
                req_url_query(., limit = .limit, offset = .offset)
response  <- req_all_SKUs %>% req_perform(., verbosity = 0) %>%  httr2::resp_body_json(.)
if (length(response$data$listGoods) == 0) {break}

ifelse(!is.null(WB.SKU.DF), WB.SKU.DF <- do.call(rbind, response$data$listGoods) %>% as.data.frame(.) %>%  select(., all_of(c("nmID", "vendorCode", "sizes","discount", "clubDiscount"))) %>%
            rbind(WB.SKU.DF, .),  
            WB.SKU.DF <- do.call(rbind, response$data$listGoods) %>% as.data.frame(.) %>%  select(., all_of(c("nmID", "vendorCode", "sizes","discount", "clubDiscount"))))


.offset <- .offset + .limit

}
for(j in 1:nrow(WB.SKU.DF)) {
  WB.SKU.DF[j, "sizes"] <-   WB.SKU.DF[, "sizes"][[j]][[1]][["price"]]
} # Этот цикл проставляет цены 
}
names(WB.SKU.DF)[which(names(WB.SKU.DF)=="sizes")] <- "price"
return(as.data.frame(WB.SKU.DF))
}  

# Функция Kill_All_WB_Discounts - убивает все скидки

Kill_All_WB_Discounts <- function(API_KEY, .prices_discounts){
result <- NULL  
  if(!missing(API_KEY)& (length(.prices_discounts)!=0)){
    .limit <- 1000
    .offset <- 0 
  repeat {
    
    
  }
  }
}

# Функция, которая считает Запрашивает у WB список заказов и возвращает датафрейм

Get.DBS.From.WB <- function(API_KEY, date_From, date_To){
 result <- NULL
 if(!missing(date_From) & (!missing(date_To))){
   # преобразуем даты в формат UnixTimeStamp
  
   From_Date <- as.POSIXct(date_From, tz = "Etc/GMT-3") |> as.numeric()
   To_Date   <- as.POSIXct(date_To, tz = "Etc/GMT-3")   |> as.numeric()
   # Делаем запрос к ВБ, выгружаем ВСЕ заказы DBS за период
   # Формируем запрос
   req_all_orders <- httr2::request("https://marketplace-api.wildberries.ru/api/v3/orders") %>% req_headers(., Authorization = API_KEY,accept = "application/json")
   
   req_all_orders <- req_url_query(req_all_orders, limit = 1000, "next" = "0", dateFrom = From_Date, dateTo = To_Date)
   response       <- req_all_orders %>% req_perform(., verbosity = 0) %>%  httr2::resp_body_json(.)
   # Помещаем ответ в датафрейм
   all_orders <- do.call(rbind, response$orders) %>% as.data.frame() %>% filter(., deliveryType == "dbs")
   
  # Статусы заказов, полученные в предыдущем щаге
   id_strings <- paste(all_orders$id, collapse = ",")
   # Готовим запрос по нужным нам id заказов
   req_statuses <- httr2::request("https://marketplace-api.wildberries.ru/api/v3/orders/status") %>%
     req_headers(.,Authorization = API_KEY,
                 accept = "application/json") %>% 
     req_method(., "POST") %>%  req_body_raw(., body = paste('{"orders" : [', id_strings,']}', collapse = ""), type = "application/json")
   
   status_response <- req_statuses %>% req_perform(., verbosity = 0) %>%  httr2::resp_body_json(.)
   # Делаем правое объединение с ответом на запрос, полученным в предыдущем шаге
   result <- do.call(rbind, status_response$orders) %>% as.data.frame(.) %>% filter(., wbStatus == "waiting") %>% 
                         right_join(x =all_orders, y = .,  by = "id", multiple = "all")
   # Нужно получить названия и телефоны клиента, делаем это отдельными запросами
   #_________________________________________________________________________________________________________________
   # Получаем контакты клиента
   req_client <- httr2::request("https://marketplace-api.wildberries.ru/api/v3/dbs/orders/client") %>%
     req_headers(.,Authorization = API_KEY,
                 accept = "application/json") %>% 
     req_method(., "POST") %>%  req_body_json(., data = list(orders=result$id))
   
   response2 <- req_client %>% req_perform(., verbosity = 0) %>%  httr2::resp_body_json(.)
   
   client_data <- do.call(rbind, response2$orders) %>% as.data.frame()
   result <- left_join(x= result, y = client_data, join_by(id == orderID), multiple = "all")
   result <- result %>%  add_column(., ItemName = "")
   # Получаем название товара
   for(j in 1:nrow(result)){
   body_str <- paste('{"settings" : { "filter" : { "textSearch" : "',as.character(result[j,"nmId"]), '", "withPhoto" : 1 }}}')
     request1 <- httr2::request("https://suppliers-api.wildberries.ru/content/v2/get/cards/list") %>%
              req_headers(., Authorization = API_KEY) %>% 
              req_method(., "POST") %>%
              req_body_raw(., body = body_str, type = "application/json")
   
   response <- request1 %>% req_perform(., verbosity = 0) %>%  httr2::resp_body_json(.)
  ifelse(length(response$cards) != 0, result[j, "ItemName"] <- response$cards[[1]]$title, result[j, "ItemName"] <- "")
   
   }
   
   }
  
  return(result)
}

#=================== Функция, которая считывает из Google Sheets
# данные об уже заведенных заказах и сравнивает их с теми, что содержатся в новом датафрейме
# и добавляет только те записи, которых нет в начальном датафрейме

New.Records.To.DF <-  function(GoogleSheets.URL, GoogleSheets.Name, GoogleSheets.Range, NewDF, id.Name ) {
  
Existing_Orders <- as.data.frame(googlesheets4::range_read(ss = GoogleSheets.URL, sheet = GoogleSheets.Name, range = GoogleSheets.Range))
Z <- data_merge(NewDF, Existing_Orders, by = id.Name, join = "anti")
return(Z)
} 

# Функция запроса всех начислений по конкретному API

Get.Ozon.Finace.Info = function(Client_ID, API_KEY, date_From = NULL, date_To=NULL){
  result <- NULL
  
  if(!missing(Client_ID) & !missing(API_KEY)){
     if(missing(date_To)) {date_To = today() }
     if(missing(date_From)) {date_From = date_To - 30}
    
    
    date_From <- paste(as.character(date_From), "T00:00:00Z", sep = "")
    date_To <- paste(as.character(date_To), "T00:00:00Z", sep = "")
    
    # запрос к сайту ОЗОН
    req <- httr2::request(OZON_API_Methods_Paths["all_finance"]) %>% 
      req_headers(.,'Client-Id' = Client_ID,
                     'Api-Key'  = API_KEY,
                  'Content-Type' = "application/json") %>% 
      req_method("POST") %>% 
      req_body_json(., list(
        filter = list(
          date = list(
          from = date_From,
          to   = date_To),
          transaction_type = "all"
        ),
        page = 1,
        page_size = 1000
      )
      )
       # -- Отправляем запрос
    
    response <- req %>% req_perform(., verbosity = 0) %>%  httr2::resp_body_json(.) 
    
    
  }
  
}

# Описываем объект для запроса данных о новых заказах

Get.Ozon.New.DBS.Class = setClass("Get.Ozon.New.DBS.Class", slots = c(
  Client_Name    = "character",   # Наименование клиента
  Client_ID      = "character",   # номер клиента в Озоне
  API_Key        = "character",   # API ключ
  date_from      = "character",   # Дата начала в текстовом формате ISO8601
  date_to        = "character",   # Дата окнчания в текстовом формает ISO8601
  limit          = "numeric",     # количество записей в ответе, как правило = 1000
  offset         = "numeric",     # смещение, как правило = 0 
  DF             = "data.frame",  # Датафрейм ответа
  method         = "character",   # Метод API, который мы собираемся вызвать: "get", "unfulfilled" или "ready". По умолчанию используем unfulfilled
  count          = "numeric",     # количество записей в ответе
  single_posting = "character"    # номер отправления для получения данных по нему 
  
), contains = "list" )

# описываем объект для расчет расстояний от МКАДа

Get.from.MKAD.Distance = setClass("Get.from.MKAD.Distance", slots = c(
  End_Point = "character", # Адрес конечной точки, может задаваться как формальный адрес, так и координатами
  Mileage   = "numeric",    # расстояние
  mak_keys  = "numeric" # по какому количеству съездов считать расстояние
),
contains = "list")

# Декларируем метод класса
setGeneric("Read.Data", def = function(x) standardGeneric('Read.Data'))


#=========================================================================
setMethod("Read.Data", signature = "Get.Ozon.New.DBS.Class",
          function(x){
            
            switch( x@method,
                    "unfulfilled" = {
            
            req <- httr2::request(OZON_API_Methods_Paths["unfulfilled"]) %>% 
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
                              ) )
                    },
            # Если нужно получить готовые к отправке заказы (но не в статусе "Доставляется")
            "ready" = {
              req <- httr2::request(OZON_API_Methods_Paths["all_fbs"]) %>% 
                req_headers(.,'Client-Id' = x@Client_ID,
                            'Api-Key'    = x@API_Key,
                            'Content-Type' = "application/json") %>% 
                req_method("POST") %>% 
                req_body_json(., list(
                  dir = "ASC",
                  filter = list(since = x@date_from,
                                to   =  x@date_to,
                                status = "awaiting_deliver"
                  ),
                  limit = x@limit,
                  offset = x@offset,
                  with = list(analytics_data = TRUE,
                              barcodes = TRUE,
                              financial_data = TRUE,
                              translit = FALSE)
                ) )
              
            },
            # Поиск конкретного отправления
            "get" = {
              req <- httr2::request(OZON_API_Methods_Paths["get"]) %>% 
                     req_headers(.,'Client-Id'   = x@Client_ID,
                                    'Api-Key'    = x@API_Key,
                                    'Content-Type' = "application/json") %>% 
                req_method("POST") %>% 
                req_body_json(., list(
                posting_number = x@single_posting
                ),
                with = list(analytics_data = TRUE,
                            barcodes = TRUE,
                            financial_data = TRUE,
                            translit = FALSE)) 
              
              
            },
            # by default
            { req <- httr2::request("https://api-seller.ozon.ru/v3/posting/fbs/unfulfilled/list") %>% 
              req_headers(.,'Client-Id' = x@Client_ID,
                          'Api-Key'    = x@API_Key,
                          'Content-Type' = "application/json") %>% 
              req_method("POST") %>% 
              req_body_json(., list(
                dir = "ASC",
                filter = list(cutoff_from = x@date_from,
                              cutoff_to   = x@date_to #,
                              #status = "awaiting_packaging"
                ),
                limit = x@limit,
                offset = x@offset,
                with = list(analytics_data = TRUE,
                            barcodes = TRUE,
                            financial_data = TRUE,
                            translit = FALSE)
                              ) )
              
            }
            )
            # --- Отправляем запрос
            
            response <- req %>% req_perform(., verbosity = 0) %>%  httr2::resp_body_json(.) 
            ifelse( x@method != "get", x@DF <- as.data.frame(do.call(rbind,response$result$postings)),
                                       x@DF <-  as.data.frame(rbind(response$result))             )
            
            x@count <- nrow(x@DF)
            
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
), contains = "list")
# === Декларируем метод Read.Data.WB.DBS - читаем новые данные DBS c WB

setGeneric("Read.Data.WB.DBS", def = function(x) standardGeneric('Read.Data.WB.DBS'))

# === Описываем метод Read.Data.WB.DBS
setMethod("Read.Data.WB.DBS", signature = "Get.WB.DBS.Class",
          function(x){
            req <- httr2::request("https://marketplace-api.wildberries.ru/api/v3/orders") %>% 
              
              req_headers(.,Authorization = x@API_Key,
                          accept = "application/json") %>% 
              req_method("GET") 
              
              
            
            # --- Отправляем запрос
            
            response <- req %>% req_perform(., verbosity = 3) %>%  httr2::resp_body_json(.) 
            x@DF     <- as.data.frame(do.call(rbind, response$orders))
            
            return(x@DF)
          })


#____________________________________________________________________________________________
Get.WB.Item.Class = setClass("Get.WB.Item.Class", slots = c(
  Client_Name = "character", #Наименование клиента
  API_Key   = "character", # API ключ
  SKU       = "character", # артикул, по которому надо получить наименование
  Name      = "character",  # Название артикула
  DF        ="data.frame"
  
), contains = "list")

setGeneric("Get.WB.Item.Name", def = function(x) standardGeneric('Get.WB.Item.Name'))
# === Описываем метод Read.Data.WB.DBS
# === Метод поиска наименования по ID товара ========================================
setMethod("Get.WB.Item.Name", signature = "Get.WB.Item.Class",
          function(x){
            req <- httr2::request("https://content-api.wildberries.ru/content/v2/get/cards/list") %>% 
              
              req_headers(.,Authorization = x@API_Key,
                          accept = "application/json") %>% 
              req_method("POST") %>%
              req_body_json(., list(
                settings = list(
                filter = list(
                  objectIDs = x@SKU
                )  
                )
              ))
            
            
            # --- Отправляем запрос
            
            response <- req %>% req_perform(., verbosity = 3) %>%  httr2::resp_body_json(.) 
            x@DF     <- as.data.frame(do.call(rbind, response$orders))
            
            return(x@DF)
          })

