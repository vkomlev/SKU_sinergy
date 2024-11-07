# Запрос финансовых данных по заказу
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


#___ ЗАПРОС к ОЗОНУ
ClientID <- "1939513" # Santech.Delivery
API_KEY <- "8345417f-9863-4536-80a8-60d0a478aa75" # АПИ ключ Santech.Delivery (KEY FOR SANTEC.DBS)
# API_KEY <- "7645b972-ad96-4f72-98a5-3568f22caf09" # (KEY FOR KUDRIN)


pack_id <- "69046217-0157-1"

s <- as.integer(100)

req <- httr2::request("https://api-seller.ozon.ru/v3/finance/transaction/list") %>% req_headers(., 
                                                                                                    'Client-Id' = ClientID,
                                                                                                    'Api-Key'    = API_KEY,
                                                                                                    'Content-Type' = "application/json") %>% req_method("POST") %>% 
  req_body_json(., list(
    
    filter= list(
      date = list( from = "2024-10-01T00:00:00Z",
                   to =    "2024-10-31T00:00:00Z"),
      
    posting_number = pack_id,
    transaction_type = "all"
  ),
  page_size = 1000,
  page = 1
  ))
  

# --- Отправляем запрос

response <- req %>% req_perform(., verbosity = 3) %>%  httr2::resp_body_json(.)

response_DF2 <- as.data.frame(do.call(rbind,response$result$postings)) # датафрейм ответа
# --- Забрали с Озона данные о новых заказах (awaiting_packaging)----
# --- теперь готовим таблицу к загрузке для дальнейшего прозвона
