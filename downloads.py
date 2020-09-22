"""Functions to fetch and manipulate package download data"""

import requests


def get_download_info(pkg_name):
    """Retrieve package download data from pypistats"""
    url = "https://pypistats.org/api/packages/" + pkg_name + "/recent"
    response = requests.get(url)
    metadata_dict = response.json()
    return metadata_dict
