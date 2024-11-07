source("GetNewDBS.R", encoding = 'UTF-8')

WB_Input_Data <- data.frame(Client_Name  = "ИП Кудрин В. В.", API_KEY = "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQxMDE2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc0NDkyMjIxNCwiaWQiOiIwMTkyOTk5Zi02YzUzLTcyZmItOTM3NC01NTlmOTQ1NmVkODkiLCJpaWQiOjE0NTQ3NTg4Niwib2lkIjo0MDYzMTMwLCJzIjozMDk2LCJzaWQiOiI0YzViMWY1YS0wYmI5LTQzZmMtOWZlNC05M2JjZjI1MTc2YzgiLCJ0IjpmYWxzZSwidWlkIjoxNDU0NzU4ODZ9.CCIjDbIoIadFpMWOo0Z2hO9O6-CxKuMZNvzJ8vLnJMnDImgQfihWjWeP5X50mubX3hH7-YFLUymx6dilEXe8Ng" )

WB.DBS.Answer <- new("Get.WB.DBS.Class")
WB.DBS.Answer@Client_Name <- WB_Input_Data$Client_Name[1]
WB.DBS.Answer@API_Key <- WB_Input_Data$API_KEY[1]

readWB <- Read.Data.WB.DBS(x=WB.DBS.Answer)