import datetime
import json
import os
import time
import xml.etree.ElementTree as ET

import requests
from tqdm import tqdm

class BGGPlaysRetriever:
    """Retrieve logged plays from the BoardGameGeek XMLAPI2 for a given game"""

    BASE_URL = "https://boardgamegeek.com/xmlapi2/plays"

    def __init__(self, api_key: str, request_delay: float = 5, timeout: int = 30):
        self.api_key = api_key
        self.request_delay = request_delay
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _generate_date_list(self, start_date: str, end_date: str) -> list:
        """Create a list of date strings between start and end date"""
        date_start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        date_end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        n_days = (date_end - date_start).days + 1
        
        dates = [
            (date_start + datetime.timedelta(days=i)).strftime("%Y-%m-%d") 
            for i in range(n_days)
            ]
        
        return dates

    def retrieve_daily_total(self, game_id: int, date: str) -> int:
        """
        Prompt the BGG API for given date and return the total plays
        """
        params = {
            "id": game_id,
            "date": date,
            "page": 1
        }
        
        try:
            response = self.session.get(
                self.BASE_URL, 
                params=params, 
                timeout=self.timeout,
                )
            
            # The BGG API returns 202 when a request is queued for processing
            # wait until 200 is returned to get the data
            # https://boardgamegeek.com/thread/1188687/export-collections-has-been-updated-xmlapi-develop
            while response.status_code == 202:
                time.sleep(self.request_delay)
                response = self.session.get(
                    self.BASE_URL, 
                    params=params, 
                    timeout=self.timeout
                    )
            
            response.raise_for_status()
            data = ET.fromstring(response.content)
            
            return int(data.get("total", 0))
            
        except requests.exceptions.RequestException as e:
            print(f"Request error for {date}: {e}")
            return 0
        finally:
            time.sleep(self.request_delay)

    def retrieve_game_plays(
            self, 
            game_id: int, 
            start_date: str, 
            end_date: str
            ) -> dict:
        """
        Retrieve the total plays per day for the given game and return total per day
        """
        daily_totals = {}
        dates = self._generate_date_list(start_date, end_date)

        for date in tqdm(dates):
            total_plays = self.retrieve_daily_total(game_id, date)
            daily_totals[date] = total_plays

        return daily_totals

    def save_to_json(self, data: dict, filepath: str):
        """Save the results to JSON file on provided path"""
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    # BGG ID for Wingspan
    # https://boardgamegeek.com/item/correction/boardgame/266192
    WINGSPAN_ID = 266192
    OUTPUT_PATH = "../data/processed/wingspan_plays_bgg.json"

    # dates formatted per BGG API requirements (YYYY-MM-DD)
    START_DATE = "2026-02-22"
    END_DATE = "2026-03-23"
    API_KEY = os.environ.get("BGG_API_KEY", "")

    fetcher = BGGPlaysRetriever(API_KEY)
    
    wingspan_plays = fetcher.retrieve_game_plays(
        WINGSPAN_ID, 
        START_DATE, 
        END_DATE
        )
    fetcher.save_to_json(wingspan_plays, OUTPUT_PATH)