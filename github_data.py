"""Functions related to retrieving data from github repo"""

import requests


def get_github_page(pypi_pkg):
    """Retrieve github page URL if available"""

    github_page = ""
    # Check potential fields for a github link
    potential_github_fields = [pypi_pkg["pypi_data"]["info"]["home_page"]]
    # Add project url fields
    for _, url in pypi_pkg["pypi_data"]["info"]["project_urls"].items():
        potential_github_fields.append(url)
    for field in potential_github_fields:
        # Any field with github in it must be github link
        if "github" in field:
            github_page = field
            break

    return github_page


def get_github_data(github_page_data):
    """Retrieve github data, if link exists, from API or website"""

    metadata_dict = {}

    if github_page_data["github_page"]:

        # TODO: Create try-except that catches rate limiting
        # and then uses web scraping instead of API in that case
        repo_info = github_page_data["github_page"].split("/")[-2:]
        url_end = "/".join(repo_info)
        github_url = "https://api.github.com/repos/" + url_end
        response = requests.get(github_url)
        metadata_dict = response.json()

    return metadata_dict


def get_github_stars(github_page_data):
    """Retrieve number of github stars from github data"""

    num_stars = "No github found"

    if github_page_data["github_page"]:
        try:
            num_stars = github_page_data["github_data"]["stargazers_count"]
        except KeyError:
            num_stars = "Rate limiting"

    return num_stars
