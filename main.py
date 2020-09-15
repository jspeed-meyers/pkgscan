"""Package class to store data about one PyPI package"""
import json
import sys

import requests

from helpers import sort_semantic_version


class Package:
    """PyPI package class"""

    def __init__(self, pkg_name):
        self.pkg_name = pkg_name
        self.pypi_data = self.get_pypi_data()
        self.first_release_date = self.get_first_release_date()
        self.last_release_date = self.get_last_release_date()
        self.number_versions = self.get_number_versions()
        self.author_email = self.get_author_email()
        self.author_name = self.get_author_name()
        self.home_page = self.get_home_page()
        self.maintainers_account_creation_date = self.get_maintainers_account_creation_date()

    def get_pypi_data(self):
        """Retrieve metadata from PyPI json endpoint"""
        try:
            pkg_url = "https://pypi.org/pypi/" + self.pkg_name + "/json"
            response = requests.get(pkg_url)
            metadata_dict = response.json()
        except json.decoder.JSONDecodeError:
            print("ERROR: No such package on PyPI")
            sys.exit(1)

        return metadata_dict

    def get_first_release_date(self):
        """Retrieve date of first release"""
        # Get the version number associated with the first non-empty release
        version_list = list(self.pypi_data["releases"])
        sorted_version_list = sort_semantic_version(version_list)
        # Because some versions lack any info, i.e. are empty, skip those
        # and save the version number of the first non-empty version
        for version in sorted_version_list:
            if self.pypi_data["releases"][version] != []:
                first_release_version = version
                break
        # Extract upload time
        upload_time = self.pypi_data["releases"][first_release_version][0][
            "upload_time"
        ]
        # Extract the date
        first_release_date = upload_time[:10]
        return first_release_date

    def get_last_release_date(self):
        """Retrieve date of last release"""
        # Get the version number associated with the last release
        version_list = list(self.pypi_data["releases"])
        sorted_version_list = sort_semantic_version(version_list)
        last_release_version = sorted_version_list[-1]
        # Extract upload time
        upload_time = self.pypi_data["releases"][last_release_version][0]["upload_time"]
        last_release_date = upload_time[:10]
        return last_release_date

    def get_author_email(self):
        """Retrieve author email"""
        author_email = self.pypi_data["info"]["author_email"]
        return author_email

    def get_number_versions(self):
        """Count number of versions released"""
        version_list = list(self.pypi_data["releases"])
        num_versions = len(version_list)
        return num_versions

    def get_author_name(self):
        """Get author's name"""
        author_name = self.pypi_data["info"]["author"]
        return author_name

    def get_home_page(self):
        """Retrieve home page link"""
        home_page = self.pypi_data["info"]["home_page"]
        return home_page

    def get_maintainers_account_creation_date(self):
        """Retrieve dates that maintainers PyPI accounts were created"""
        pass

    # get metadata from github

    # Get metadata about maintainers

    # Compare to other package names

    # Get number of downloads

    # Create supsicious score

    # Print info - least info (-v)
    def print(self):
        """Print package information"""
        print("Last release date: " + self.last_release_date)
        print("First release date: " + self.first_release_date)
        print("Number of versions: " + str(self.number_versions))
        print("Home page: " + self.home_page)
        print("Author email: " + self.author_email)
        print("Author name: " + self.author_name)

    # Print info - more info (-vv)

    # Print info - most info (-vvv)


if __name__ == "__main__":

    # Collect package name from command line
    # TODO: Use argparse instead
    package = Package(sys.argv[1])
    package.print()
