"""Package class to store data about one PyPI package"""
import json
import sys

from bs4 import BeautifulSoup
import requests

from helpers import sort_semantic_version


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
        self.pypi_pkg["pypi_data"] = self.get_pypi_data()
        self.pypi_pkg["first_release_date"] = self.get_first_release_date()
        self.pypi_pkg["last_release_date"] = self.get_last_release_date()
        self.pypi_pkg["number_versions"] = self.get_number_versions()
        self.pypi_pkg["author_email"] = self.get_author_email()
        self.pypi_pkg["author_name"] = self.get_author_name()
        self.pypi_pkg["home_page"] = self.get_home_page()
        self.pypi_pkg["pypi_pkg_signed"] = self.is_pypi_pkg_signed()
        self.pypi_pkg["maintainers_list"] = self.get_pypi_maintainers_list()

    def generate_pypi_profiles_data(self):
        """Create a dict of all pypi profile-related data"""
        self.pypi_profiles["maintainers_data"] = self.get_pypi_maintainers_data()
        self.pypi_profiles[
            "maintainers_account_creation_date"
        ] = self.get_maintainers_account_creation_date()
        self.pypi_profiles[
            "number_of_packages_maintained_by_maintainers"
        ] = self.get_number_of_packages_maintained_by_maintainers()

    def generate_github_data(self):
        """Create a dict of all github-related data"""
        self.github_page_data["github_page"] = self.get_github_page()
        self.github_page_data["github_data"] = self.get_github_data()
        self.github_page_data["github_stars"] = self.get_github_stars()

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
        # TODO: Create get releases functionality to simplify this and related functions
        # Get the version number associated with the first non-empty release
        version_list = list(self.pypi_pkg["pypi_data"]["releases"])
        sorted_version_list = sort_semantic_version(version_list)
        # Because some versions lack any info, i.e. are empty, skip those
        # and save the version number of the first non-empty version
        for version in sorted_version_list:
            if self.pypi_pkg["pypi_data"]["releases"][version] != []:
                first_release_version = version
                break
        # Extract upload time
        upload_time = self.pypi_pkg["pypi_data"]["releases"][first_release_version][0][
            "upload_time"
        ]
        # Extract the date
        first_release_date = upload_time[:10]
        return first_release_date

    def get_last_release_date(self):
        """Retrieve date of last release"""
        # Get the version number associated with the last release
        version_list = list(self.pypi_pkg["pypi_data"]["releases"])
        sorted_version_list = sort_semantic_version(version_list)
        last_release_version = sorted_version_list[-1]
        # Extract upload time
        upload_time = self.pypi_pkg["pypi_data"]["releases"][last_release_version][0][
            "upload_time"
        ]
        last_release_date = upload_time[:10]
        return last_release_date

    def get_author_email(self):
        """Retrieve author email"""
        author_email = self.pypi_pkg["pypi_data"]["info"]["author_email"]
        return author_email

    def get_number_versions(self):
        """Count number of versions released"""
        version_list = list(self.pypi_pkg["pypi_data"]["releases"])
        num_versions = len(version_list)
        return num_versions

    def get_author_name(self):
        """Get author's name"""
        author_name = self.pypi_pkg["pypi_data"]["info"]["author"]
        return author_name

    def get_home_page(self):
        """Retrieve home page link"""
        home_page = self.pypi_pkg["pypi_data"]["info"]["home_page"]
        return home_page

    def is_pypi_pkg_signed(self):
        """Check if latest version of package is signed"""
        # TODO: Package up this code block into fnto function since
        # it is duplicated from get_last_release date.
        version_list = list(self.pypi_pkg["pypi_data"]["releases"])
        sorted_version_list = sort_semantic_version(version_list)
        last_release_version = sorted_version_list[-1]
        # Extract whether there is a signature
        is_signed = self.pypi_pkg["pypi_data"]["releases"][last_release_version][0][
            "has_sig"
        ]
        return is_signed

    def get_pypi_maintainers_list(self):
        """Retrieve list of PyPI maintainers via web scraping"""
        # Scrape regular PyPI package site
        url = "https://pypi.org/project/" + self.pkg_name
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        elements = soup.findAll(
            "span", {"class": "sidebar-section__user-gravatar-text"}
        )
        # Strip white space from all elements
        maintainers_full_list = [elem.string.strip() for elem in elements]
        # Remove duplicates via set, then sort a list of maintainers
        maintainers_list = sorted(list(set(maintainers_full_list)))
        return maintainers_list

    def get_pypi_maintainers_data(self):
        """Retrieve metadata from PyPI on all maintainers via web scraping"""
        maintainers_data = []
        for username in self.pypi_pkg["maintainers_list"]:
            url = "https://pypi.org/user/" + username
            html = requests.get(url)
            soup = BeautifulSoup(html.content, "html.parser")
            maintainers_data.append(soup)

        return maintainers_data

    def get_maintainers_account_creation_date(self):
        """Retrieve dates that maintainers' PyPI accounts were created"""

        dates = []
        # Loop through beautiful soup-ified maintainer data to extract dates
        for soup in self.pypi_profiles["maintainers_data"]:
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

    def get_number_of_packages_maintained_by_maintainers(self):
        """Retrieve number of PyPI packages maintained by each maintainer"""

        num_packages = []

        # Loop thru beautiful-souped maintainer list
        for soup in self.pypi_profiles["maintainers_data"]:
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

    def get_github_page(self):
        """Retrieve github page URL if available"""

        github_page = ""
        # Check potential fields for a github link
        potential_github_fields = [self.pypi_pkg["pypi_data"]["info"]["home_page"]]
        # Add project url fields
        for _, url in self.pypi_pkg["pypi_data"]["info"]["project_urls"].items():
            potential_github_fields.append(url)
        for field in potential_github_fields:
            # Any field with github in it must be github link
            if "github" in field:
                github_page = field
                break

        return github_page

    def get_github_data(self):
        """Retrieve github data, if link exists, from API or website"""

        metadata_dict = {}

        if self.github_page_data["github_page"]:

            # TODO: Create try-except that catches rate limiting
            # and then uses web scraping instead of API in that case
            repo_info = self.github_page_data["github_page"].split("/")[-2:]
            url_end = "/".join(repo_info)
            github_url = "https://api.github.com/repos/" + url_end
            response = requests.get(github_url)
            metadata_dict = response.json()

        return metadata_dict

    def get_github_stars(self):
        """Retrieve number of github stars from github data"""

        num_stars = "No github found"

        if self.github_page_data["github_page"]:
            try:
                num_stars = self.github_page_data["github_data"]["stargazers_count"]
            except KeyError:
                num_stars = "Rate limiting"

        return num_stars

    # Print info - least info (-v)
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

    # Print info - more info (-vv)

    # Print info - most info (-vvv)


if __name__ == "__main__":

    # Collect package name from command line
    # TODO: Use argparse instead
    package = Package(sys.argv[1])
    package.print()
