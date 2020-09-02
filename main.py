"""Package class to store data about one PyPI package

"""
import requests

from helpers import sort_semantic_version

class Package:
    """PyPI package class"""

    def __init__(self, pkg_name):
        self.pkg_name = pkg_name
        self.pypi_data = self.get_pypi_data()
        self.first_release_date = self.get_first_release_date()
        #.last_release_date = self.get_last_release_date()
        self.get_author_email = self.get_author_email()
    
    def get_pypi_data(self):
        """Retrieve metadata from PyPI json endpoint"""
        pkg_url = "https://pypi.org/pypi/" + self.pkg_name + "/json"
        response = requests.get(pkg_url)
        metadata_dict = response.json()
        return metadata_dict

    def get_first_release_date(self):
        """Retrieve date of first release"""
        # Get the version number associated with the first non-empty release
        version_list = list(self.pypi_data['releases'])
        sorted_version_list = sort_semantic_version(version_list)
        # Because some versions lack any info, i.e. are empty, skip those
        # and save the version number of the first non-empty version
        for version in sorted_version_list:
            if self.pypi_data['releases'][version] != []:
                first_release_version = version
                break
        # Extract upload time
        upload_time = self.pypi_data['releases'][first_release_version][0]['upload_time']
        # Extract the date
        first_release_date = upload_time[:10]
        return first_release_date

    def get_last_release_date(self):
        """Retrieve date of last release"""
        # Get the version number associated with the last release
        version_list = list(self.pypi_data['releases'])
        sorted_version_list = sort_semantic_version(version_list)
        last_release_version = sorted_version_list[-1]
        # Extract upload time
        upload_time = self.pypi_data['releases'][last_release_version][0]['upload_time']
        last_release_date = upload_time[:10]
        return last_release_date

    def get_author_email(self):
        """Retrieve author email"""
        author_email = self.pypi_data['info']['author_email']
        return author_email

    # get metadata from github

    # Get metadata about maintainers

    # Compare to other package names

    # Print info - least info (-v)
    def print(self):
        """Print package information"""
        print("Last release date: " + self.last_release_date)
        print("First release date: " + self.first_release_date)
        print("Author email: " + self.get_author_email)

    # Print info - more info (-vv)

    # Print info - most info (-vvv)


if __name__ == "__main__":
    package = Package("requests")
    package.print()
