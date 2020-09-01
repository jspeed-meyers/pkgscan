"""Package class to store data about one PyPI package

"""
import requests

# class for a package
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
        """Retrieve data of first release"""
        # Get the version number associated with the first release
        # TODO: Double check this, especially the hard coding at the end
        # TODO: Probably unpack this line too
        # TODO: This is broken. I need to get all the semantic version and then
        # sort them.
        version_list = list(self.pypi_data['releases'])
        sorted_version_list = sorted(version_list)
        print(sorted_version_list)
        first_release_version = str(list(self.pypi_data['releases'].items())[1][0])
        print(first_release_version)
        # Extract upload time
        upload_time = self.pypi_data['releases'][first_release_version][0]['upload_time']
        first_release_date = upload_time[:10]
        return first_release_date

    def get_last_release_date(self):
        """Retrieve data of last release"""
        # Get the version number associated with the first release
        # TODO: Double check this, especially the hard coding at the end
        last_release_version = str(list(self.pypi_data['releases'].items())[-1])
        print(last_release_version)
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
