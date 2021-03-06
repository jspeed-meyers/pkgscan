"""Functions related to gathering data about a particular package on PyPI"""
from datetime import datetime, timedelta
import json
import sys

from bs4 import BeautifulSoup
from packaging import version
import requests


def get_author_email(pypi_pkg):
    """Retrieve author email"""
    author_email = pypi_pkg["pypi_data"]["info"]["author_email"]
    return author_email


def get_author_name(pypi_pkg):
    """Get author's name"""
    author_name = pypi_pkg["pypi_data"]["info"]["author"]
    return author_name


def get_first_release_date(pypi_pkg):
    """Retrieve date of first release"""
    sorted_version_list = get_sorted_version_list(pypi_pkg)
    # Because some versions lack any info, i.e. are empty, skip those
    # and save the version number of the first non-empty version
    for pkg_version in sorted_version_list:
        if pypi_pkg["pypi_data"]["releases"][pkg_version] != []:
            first_release_version = pkg_version
            break
    # Extract upload time
    upload_time = pypi_pkg["pypi_data"]["releases"][first_release_version][0][
        "upload_time"
    ]
    # Extract the date
    first_release_date = upload_time[:10]
    return first_release_date


def get_home_page(pypi_pkg):
    """Retrieve home page link"""
    home_page = pypi_pkg["pypi_data"]["info"]["home_page"]
    return home_page


def get_last_release_date(pypi_pkg):
    """Retrieve date of last release"""
    sorted_version_list = get_sorted_version_list(pypi_pkg)
    last_release_version = sorted_version_list[-1]
    # Extract upload time
    upload_time = pypi_pkg["pypi_data"]["releases"][last_release_version][0][
        "upload_time"
    ]
    last_release_date = upload_time[:10]
    return last_release_date


def get_number_releases_past_year(pypi_pkg):
    """Retrieve mean time between releases over past two years"""
    sorted_version_list = get_sorted_version_list(pypi_pkg)
    # Determine current and date one year ago
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)

    num_versions_within_last_year = 0
    # Loop thru versions in reverse order
    sorted_version_list.reverse()
    for pkg_version in sorted_version_list:
        # Retrieve version date
        try:
            upload_time = pypi_pkg["pypi_data"]["releases"][pkg_version][0][
                "upload_time"
            ]
        except IndexError:
            upload_time = "2010-11-04T00:05:23"
        # Convert version date to datetime object
        upload_datetime = datetime.fromisoformat(upload_time)
        # Check if version date is within past year
        if upload_datetime > one_year_ago:
            num_versions_within_last_year += 1
        else:
            break

    return num_versions_within_last_year


def get_number_versions(pypi_pkg):
    """Count number of versions released"""
    version_list = list(pypi_pkg["pypi_data"]["releases"])
    num_versions = len(version_list)
    return num_versions


def get_pypi_data(pkg_name):
    """Retrieve metadata from PyPI json endpoint"""
    try:
        pkg_url = "https://pypi.org/pypi/" + pkg_name + "/json"
        response = requests.get(pkg_url)
        metadata_dict = response.json()
    except json.decoder.JSONDecodeError:
        print("ERROR: No such package on PyPI")
        sys.exit(1)

    return metadata_dict


def get_pypi_maintainers_list(pkg_name):
    """Retrieve list of PyPI maintainers via web scraping"""
    # Scrape regular PyPI package site
    url = "https://pypi.org/project/" + pkg_name
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    elements = soup.findAll("span", {"class": "sidebar-section__user-gravatar-text"})
    # Strip white space from all elements
    maintainers_full_list = [elem.string.strip() for elem in elements]
    # Remove duplicates via set, then sort a list of maintainers
    maintainers_list = sorted(list(set(maintainers_full_list)))
    return maintainers_list


def is_pypi_pkg_signed(pypi_pkg):
    """Check if latest version of package is signed"""
    sorted_version_list = get_sorted_version_list(pypi_pkg)
    last_release_version = sorted_version_list[-1]
    # Extract whether there is a signature
    is_signed = pypi_pkg["pypi_data"]["releases"][last_release_version][0]["has_sig"]
    return is_signed


def sort_semantic_version(unsorted_list):
    """Sort a list of semantic version numbers"""
    sorted_list = sorted(unsorted_list, key=lambda x: version.Version(x))
    return sorted_list


def get_sorted_version_list(pypi_pkg):
    """Create list of package versions sorted"""
    version_list = list(pypi_pkg["pypi_data"]["releases"])
    sorted_version_list = sort_semantic_version(version_list)
    return sorted_version_list
