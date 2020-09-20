"""Functions related to gathering data about PyPI maintainer profiles"""

from bs4 import BeautifulSoup
import requests


def get_pypi_maintainers_data(pypi_pkg):
    """Retrieve metadata from PyPI on all maintainers via web scraping"""
    maintainers_data = []
    for username in pypi_pkg["maintainers_list"]:
        url = "https://pypi.org/user/" + username
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        maintainers_data.append(soup)

    return maintainers_data


def get_maintainers_account_creation_date(pypi_profiles):
    """Retrieve dates that maintainers' PyPI accounts were created"""

    dates = []
    # Loop through beautiful soup-ified maintainer data to extract dates
    for soup in pypi_profiles["maintainers_data"]:
        # Because 'time' elements will appear in multiple locations on
        # a PyPI maintainer profile page, filter in only those html
        # tags associated with author metadata
        author_metadata_elements = soup.findAll(
            "div", {"class": "author-profile__metadiv"}
        )
        for elem in author_metadata_elements:
            # Extract any time-related elements and add to dates list
            # if it exists
            date = elem.find("time")
            if date:
                # The [0] slice is because contents is a list and
                # strip() is not a valid method for lists
                dates.append(date.contents[0].strip())

    return dates


def get_number_of_packages_maintained_by_maintainers(pypi_profiles):
    """Retrieve number of PyPI packages maintained by each maintainer"""

    num_packages = []

    # Loop thru beautiful-souped maintainer list
    for soup in pypi_profiles["maintainers_data"]:
        package_count_elements = soup.findAll("div", {"class": "left-layout__main"})
        # Extract count of number of projects maintained for each profile
        for element in package_count_elements:
            num_package_element = element.find("h2")
            # Remove whitespace
            num_package_element_stripped = num_package_element.contents[0].strip()
            # Take only number from the number of packages, drop "packages" units
            num_package = num_package_element_stripped.split(" ")[0]
            num_packages.append(num_package)

    return num_packages
