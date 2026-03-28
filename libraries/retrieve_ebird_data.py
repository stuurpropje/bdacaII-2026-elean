import os

import pandas as pd
import requests

def retrieve_ebird_data(back: int, key: str, regions: str, timeout: int=30) -> list[dict]:
    """
    Retrieve data of observations from given regions
    
    args:
        back: days looking back from moment of query (max 30)
        key: API access key
        regions: region or region in str format, seperated by a comma if multiple
        timeout: prevent the script from becoming unresponsive if API doesn't respond

    returns:
        a list of dictionaries containing observations in a given region
    """
    response = requests.get(
        url=f"https://api.ebird.org/v2/data/obs/{regions}/recent",
        params={"back": back}, 
        headers={'X-eBirdApiToken': key},
        timeout=timeout,
        )

    print(response.status_code)
    response.raise_for_status()

    return response.json()

def filter_wingspan_birds(data: list[dict], wingspan_birds: set[str]) -> list[dict]:
    """Returns only birds in observation logs also in Wingspan"""
    return [obs for obs in data if obs.get("sciName") in wingspan_birds]

if __name__ == "__main__":
     # store API key locally, enables API access
    api_key = os.environ.get('EBIRD_API_KEY', "")

    # United states, Mexico, Canada
    regions = "US,MX,CA"

    # data source: https://github.com/coolbutuseless/wingspan
    # file contains all birds featured in the base game
    wingspan_bird_data = pd.read_excel("../data/raw/Wingspan Bird List ENG-NED-DEU.xlsx")
    wingspan_sci_names = set(wingspan_bird_data["ScientificName"])

    # set max numbers of days looking back to 30 (maximum allowed following eBird API documentation)
    data = retrieve_ebird_data(30, api_key, regions)    

    pd.DataFrame(data).to_csv(
        "../data/raw/ebird_observations_2026_03_27.csv", 
        index=False
        )

    final_dataset = filter_wingspan_birds(data, wingspan_sci_names)

    pd.DataFrame(final_dataset).to_csv(
        "../data/processed/wingspan_ebird_observations_2026_03_27.csv", 
        index=False
        )


