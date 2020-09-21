"""Functions related to retrieving data from github repo"""

from bs4 import BeautifulSoup
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

    github_data = None
    github_data_source = "API"

    if github_page_data["github_page"]:

        # Try github API. There is rate limiting, including only six
        # hits without being signed in to github, so rate limiting
        # will likely apply.
        repo_info = github_page_data["github_page"].split("/")[-2:]
        url_end = "/".join(repo_info)
        github_url = "https://api.github.com/repos/" + url_end
        response = requests.get(github_url)
        metadata_dict = response.json()
        github_data = metadata_dict

        # If github API rate limit exceeded. Try scraping github page
        if not response.ok:
            github_data_source = "webscrape"
            html = requests.get(github_page_data["github_page"])
            soup = BeautifulSoup(html.content, "html.parser")
            github_data = soup

    return github_data, github_data_source


def get_github_stars(github_page_data):
    """Retrieve number of github stars from github data"""

    num_stars = "No github found"

    # print(github_page_data["github_data_source"])
    if github_page_data["github_page"]:
        # If data on github comes form github API, parse json
        if github_page_data["github_data_source"] == "API":
            num_stars = github_page_data["github_data"]["stargazers_count"]
        # If data on github comes from web scraping, parse beautiful soup object
        elif github_page_data["github_data_source"] == "webscrape":
            num_stars_element = github_page_data["github_data"].find(
                "a", {"class": "social-count js-social-count"}
            )
            try:
                num_stars = num_stars_element.contents[0].strip()
            except AttributeError:
                num_stars = "Error"

    return num_stars
