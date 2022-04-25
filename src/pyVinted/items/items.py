from pyVinted.items.item import Item
from pyVinted.requester import requester
from urllib.parse import urlparse, parse_qsl
from requests.exceptions import HTTPError
from typing import List, Dict
class Items:

    def search(self, url, nbrItems: int = 20, page: int =1) -> List[Item]:
        """
        Retrieves items from a given search url on vited.

        Args:
            url (str): The url of the research on vinted.
            nbrItems (int): Number of items to be returned (default 20).
            page (int): Page number to be returned (default 1).

        """
        VINTED_API_URL = f"https://www.vinted.fr/api/v2"
        VINTED_PRODUCTS_ENDPOINT = "catalog/items"
        params = self.parseUrl(url, nbrItems, page)
        url = f"{VINTED_API_URL}/{VINTED_PRODUCTS_ENDPOINT}"
        print(url)
        try:
            response = requester.get(url=url, params=params)
            response.raise_for_status()
            items = response.json()
            items = items["items"]
            return [Item(_item) for _item in items]

        except HTTPError as err:
            raise err


    def parseUrl(self, url, nbrItems=20, page=1) -> Dict:
        """
        Parse Vinted search url to get parameters the for api call.

        Args:
            url (str): The url of the research on vinted.
            nbrItems (int): Number of items to be returned (default 20).
            page (int): Page number to be returned (default 1).

        """
        querys = parse_qsl(urlparse(url).query)

        params = {
            "search_text": "+".join(
                map(str, [tpl[1] for tpl in querys if tpl[0] == "search_text"])
            ),
            "catalog_ids": ",".join(
                map(str, [tpl[1] for tpl in querys if tpl[0] == "catalog[]"])
            ),
            "color_ids": ",".join(
                map(str, [tpl[1] for tpl in querys if tpl[0] == "color_id[]"])
            ),
            "brand_ids": ",".join(
                map(str, [tpl[1] for tpl in querys if tpl[0] == "brand_id[]"])
            ),
            "size_ids": ",".join(
                map(str, [tpl[1] for tpl in querys if tpl[0] == "size_id[]"])
            ),
            "material_ids": ",".join(
                map(str, [tpl[1] for tpl in querys if tpl[0] == "material_id[]"])
            ),
            "status_ids": ",".join(
                map(str, [tpl[1] for tpl in querys if tpl[0] == "status[]"])
            ),
            "country_ids": ",".join(
                map(str, [tpl[1] for tpl in querys if tpl[0] == "country_id[]"])
            ),
            "city_ids": ",".join(
                map(str, [tpl[1] for tpl in querys if tpl[0] == "city_id[]"])
            ),
            "is_for_swap": ",".join(
                map(str, [1 for tpl in querys if tpl[0] == "disposal[]"])
            ),
            "currency": ",".join(
                map(str, [tpl[1] for tpl in querys if tpl[0] == "currency"])
            ),
            "price_to": ",".join(
                map(str, [tpl[1] for tpl in querys if tpl[0] == "price_to"])
            ),
            "price_from": ",".join(
                map(str, [tpl[1] for tpl in querys if tpl[0] == "price_from"])
            ),
            "page": page,
            "per_page": nbrItems,
            "order": ",".join(
                map(str, [tpl[1] for tpl in querys if tpl[0] == "order"])
            ),
        }

        return params
