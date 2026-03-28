import datetime
import json
import time

import pandas as pd
import requests
from tqdm import tqdm


class WikipediaPageviewRetriever:
    """Retrieve daily pageview data from the Wikimedia REST API for a given list of birds"""

    BASE_URL = (
        "https://wikimedia.org/api/rest_v1/metrics/pageviews/"
        "per-article/{lang}.wikipedia/all-access/user/{name}/"
        "{interval}/{start_date}/{end_date}")

    def __init__(
            self, 
            user_agent: str, 
            request_delay: float = 0.5, 
            timeout: int = 30
            ):
        self.user_agent = user_agent
        self.request_delay = request_delay
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})

    def _generate_date_template(self, start_date: str, end_date: str) -> dict:
        """Create a default dictionary the given date range mapping to None"""
        
        date_start = datetime.datetime.strptime(start_date, "%Y%m%d")
        date_end = datetime.datetime.strptime(end_date, "%Y%m%d")
        n_days = (date_end - date_start).days + 1
        
        dates = {
            (date_start + datetime.timedelta(days=i)).strftime("%Y%m%d00"): None 
            for i in range(n_days)
        }

        return dates

    def retrieve_bird_data(
            self, 
            lang: str, 
            name: str, 
            start_date: str, 
            end_date: str, 
            interval: str="daily"
            ) -> list[dict] | None:
        """
        Prompts the API for a provided bird name and date range
        
        args:
            name: The name of the bird. 
                Preferably the scientific name to avoid ambiguity, but can also use common names
            start_date: The start date for the pageview data in YYYYMMDD format
            end_date: The end date for the pageview data in YYYYMMDD format
            interval: interval for retrieved data, defaults to "daily"
        returns:
            list of pageview data items if successful, or None if there was an error was encountered
        """
        url = self.BASE_URL.format(
            lang=lang, 
            name=name, 
            interval=interval, 
            start_date=start_date, 
            end_date=end_date
            )
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json().get("items")
        except requests.exceptions.RequestException as e:
            print(f"Request error for {name}: {e}")
            return None
        finally:
            time.sleep(self.request_delay)

    def process_bird_list(
            self, 
            bird_names: pd.DataFrame, 
            start_date: str, 
            end_date: str, 
            languages: list[str]
            ) -> dict:
        """
        Process the given list of birds to retrieve their pageviews
        
        args:
            bird_names: a DataFrame containing the columns "EnglishName" and "ScientificName"
            start_date: the start date for the pageview data in YYYYMMDD format
            end_date: the end date for the pageview data in YYYYMMDD format
            languages: list of languages to be queried

        returns:
            dictionary mapping the given common name to a dictionary of date-pageview pairs, 
            or None if data could not be retrieved
        """
        
        results = {}
        dates = self._generate_date_template(start_date, end_date)

        for bird in tqdm(bird_names[["EnglishName", "ScientificName"]].to_dict("records")):
            # retrieve pageviews for scientific name to prevent disambiguation issues with common names
            # e.g, "Killdeer"
            # wikipedia does not care about spaces
            # the scientific names can be directly applied to the wikimedia links based on prior tests
            scientific_name = bird["ScientificName"]
            common_name = bird["EnglishName"]

            # ensure that dates are reset for each bird
            bird_dates = dates.copy()

            # enables easy check for missing data assignment instead of null assignment
            data_found = False

            for language in languages:
                items = self.retrieve_bird_data(
                    lang=language, 
                    name=scientific_name, 
                    start_date=start_date, 
                    end_date=end_date
                    )

                if items:
                    data_found = True
                    for item in items:
                        if bird_dates[item["timestamp"]] is None:
                            # ensure first language found is assigned to 
                            # prevent Nonetype + int addition
                            bird_dates[item["timestamp"]] = item["views"]
                        else:
                            bird_dates[item["timestamp"]] += item["views"]
               
            results[common_name] = bird_dates if data_found else None

        return results


    def save_to_json(self, data: dict, filepath: str):
        """"Saves the resultsto to a JSON file on the provided path"""
        with open(filepath, "w") as f:
            json.dump(data, f)


if __name__ == "__main__":
    # set default user agent per Wikipedia API guidelines
    # https://meta.wikimedia.org/wiki/User-Agent_policy
    USER_AGENT = "WingspanIncidentalLearning (13411438@uva.nl)"

    INPUT_PATH = "../data/raw/Wingspan Bird List ENG-NED-DEU.xlsx"
    OUTPUT_PATH = "../data/processed/bird_views_wikipedia.json"

    # retrieve dates until 30 days ago 
    # (aligning it with max retrieval date of 30 days of eBird)

    # eBird data was retrieved on 2026-03-23, end date set to match
    end_date = "20260323" # strftime no seperators per Wikipedia format %Y%m%d
    start_date = "20260222"

    df_birds = pd.read_excel(INPUT_PATH)
    retriever = WikipediaPageviewRetriever(USER_AGENT)
    
    bird_views = retriever.process_bird_list(df_birds, start_date, end_date, ["en", "fr", "es"])
    retriever.save_to_json(bird_views, OUTPUT_PATH)