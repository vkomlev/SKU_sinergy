import requests
import pandas as pd


class WildberriesData:

    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://marketplace-api.wildberries.ru/api"

    def get_orders(self, date_from = None, date_to = None):
        """
        Получает список заказов из Wildberries API в формате DataFrame.
        """
        from app.utils.helpers import unix_timestamp
        url = self.url + "/v3/orders"
        headers = {"Authorization": self.api_key, "accept": "application/json"}
        params = {
            "limit": 1000,
            "next": "0",
        }
        if date_from:
            params["dateFrom"] = unix_timestamp(date_from)
        if date_to:
            params["dateTo"] = unix_timestamp(date_to)

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        orders = response.json().get("orders", [])
        df_orders = pd.DataFrame(orders)
        df_orders['price'] = df_orders['price']/100
        df_orders['convertedPrice'] = df_orders['convertedPrice']/100
        return df_orders[df_orders["deliveryType"] == "dbs"]


    def get_order_statuses(self, order_ids):
        """
        Получает статусы заказов из Wildberries API в формате DataFrame.
        """
        url = self.url + "/v3/orders/status"
        headers = {
            "Authorization": self.api_key,
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        body = {"orders": order_ids}
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        statuses = response.json().get("orders", [])
        return pd.DataFrame(statuses)


    def get_client_contacts(self, order_ids):
        """
        Получает контактные данные клиента из Wildberries API в формате DataFrame.
        """
        url = self.url + "/v3/dbs/orders/client"
        headers = {
            "Authorization": self.api_key,
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        body = {"orders": order_ids}
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        client_data = response.json().get("orders", [])
        return pd.DataFrame(client_data)


    def get_item_name(self, nm_id):
        """
        Получает название товара из Wildberries API по nmId.
        """
        url = "https://suppliers-api.wildberries.ru/content/v2/get/cards/list"
        headers = {"Authorization": self.api_key, "Content-Type": "application/json"}
        body = {"settings": {"filter": {"textSearch": str(nm_id), "withPhoto": 1}}}
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        cards = response.json().get("cards", [])
        return cards[0]["title"] if cards else ""


    def get_full_order_data(self, date_from = None, date_to = None):
        """
        Основная функция, собирающая все данные: заказы, статусы, контакты, названия товаров.
        """
        # Получаем заказы
        orders_df = self.get_orders(date_from, date_to)
        
        if orders_df.empty:
            return pd.DataFrame()  # Если нет заказов, возвращаем пустой DataFrame

        # Получаем статусы заказов
        order_ids = orders_df["id"].tolist()
        statuses_df = self.get_order_statuses( order_ids)
        result = pd.merge(orders_df, statuses_df, on="id", how="right")

        # Фильтруем только нужные статусы
        result = result[result["wbStatus"] == "waiting"]

        # Получаем контактные данные клиентов
        client_contacts_df = self.get_client_contacts(result["id"].tolist())
        result = pd.merge(result, client_contacts_df, left_on="id", right_on="orderID", how="left")

        # Добавляем названия товаров
        result["ItemName"] = result["nmId"].apply(lambda nm_id: self.get_item_name(nm_id))

        return result



