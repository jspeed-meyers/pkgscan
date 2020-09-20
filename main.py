"""Package class to store data about one PyPI package"""

import sys

from github_data import get_github_data, get_github_page, get_github_stars
from pypi_pkg import (
    get_author_email,
    get_author_name,
    get_first_release_date,
    get_home_page,
    get_last_release_date,
    get_number_versions,
    get_pypi_data,
    get_pypi_maintainers_list,
    is_pypi_pkg_signed,
)
from pypi_profiles import (
    get_maintainers_account_creation_date,
    get_number_of_packages_maintained_by_maintainers,
    get_pypi_maintainers_data,
)


class Package:
    """PyPI package class"""

    def __init__(self, pkg_name):
        self.pkg_name = pkg_name
        # PyPI package data
        self.pypi_pkg = {}
        self.generate_pypi_pkg_dict_data()
        # PyPI maintainers data
        self.pypi_profiles = {}
        self.generate_pypi_profiles_data()
        # Github page data
        self.github_page_data = {}
        self.generate_github_data()

    def generate_pypi_pkg_dict_data(self):
        """Create a dict of all pypi package-related data"""
        self.pypi_pkg["pypi_data"] = get_pypi_data(self.pkg_name)
        self.pypi_pkg["first_release_date"] = get_first_release_date(self.pypi_pkg)
        self.pypi_pkg["last_release_date"] = get_last_release_date(self.pypi_pkg)
        self.pypi_pkg["number_versions"] = get_number_versions(self.pypi_pkg)
        self.pypi_pkg["author_email"] = get_author_email(self.pypi_pkg)
        self.pypi_pkg["author_name"] = get_author_name(self.pypi_pkg)
        self.pypi_pkg["home_page"] = get_home_page(self.pypi_pkg)
        self.pypi_pkg["pypi_pkg_signed"] = is_pypi_pkg_signed(self.pypi_pkg)
        self.pypi_pkg["maintainers_list"] = get_pypi_maintainers_list(self.pkg_name)

    def generate_pypi_profiles_data(self):
        """Create a dict of all pypi profile-related data"""
        self.pypi_profiles["maintainers_data"] = get_pypi_maintainers_data(
            self.pypi_pkg
        )
        self.pypi_profiles[
            "maintainers_account_creation_date"
        ] = get_maintainers_account_creation_date(self.pypi_profiles)
        self.pypi_profiles[
            "number_of_packages_maintained_by_maintainers"
        ] = get_number_of_packages_maintained_by_maintainers(self.pypi_profiles)

    def generate_github_data(self):
        """Create a dict of all github-related data"""
        self.github_page_data["github_page"] = get_github_page(self.pypi_pkg)
        self.github_page_data["github_data"] = get_github_data(self.github_page_data)
        self.github_page_data["github_stars"] = get_github_stars(self.github_page_data)

    def print(self):
        """Print package information"""
        print("First release date: " + self.pypi_pkg["first_release_date"])
        print("Number of versions: " + str(self.pypi_pkg["number_versions"]))
        print("Home page: " + self.pypi_pkg["home_page"])
        print("Github link: " + self.github_page_data["github_page"])
        print("Author email: " + self.pypi_pkg["author_email"])
        print("Author name: " + self.pypi_pkg["author_name"])
        print("Maintainer usernames: ", end="")
        for maintainer in self.pypi_pkg["maintainers_list"]:
            print(maintainer, end=" ")
        print()
        print("Maintainer accounts creation dates: ", end="")
        for date in self.pypi_profiles["maintainers_account_creation_date"]:
            print(date, end=" ")
        print()
        print("Number of packagages maintained by maintainers: ", end=" ")
        for num in self.pypi_profiles["number_of_packages_maintained_by_maintainers"]:
            print(num, end=" ")
        print()
        print("Github stars: " + str(self.github_page_data["github_stars"]))


if __name__ == "__main__":

    # Collect package name from command line
    # TODO: Use argparse instead
    package = Package(sys.argv[1])
    package.print()
