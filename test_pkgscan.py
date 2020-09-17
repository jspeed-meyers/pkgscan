"""Tests for pkgscan"""

from bs4 import BeautifulSoup

from main import Package
from helpers import sort_semantic_version


def test_sort_semantic_version():
    """Test sort_semantic_version function"""
    unsorted_list = ["0.3.2", "0.1.1", "5.5.5"]
    sorted_list = sort_semantic_version(unsorted_list)
    assert sorted_list == ["0.1.1", "0.3.2", "5.5.5"]


def test_package_class():
    """Test instantiation of package class"""
    package = Package("requests")  # pylint: disable=unused-variable


def test_get_first_release_date():
    """Test get_first_release_date function"""
    package = Package("requests")
    assert package.first_release_date == "2011-02-14"
    package = Package("numpy")
    assert package.first_release_date == "2006-12-02"


def test_get_last_release_date():
    """Test get_last_release_date function

    To avoid breaking this test when there is a change to an often
    updated package, this test uses pcap2map, a personal project of
    John Speed Meyers on PyPI that is not maintained.
    """
    package = Package("pcap2map")
    assert package.last_release_date == "2020-04-10"


def test_get_number_versions():
    """Test get_number_versions function"""
    package = Package("pandas")
    assert package.number_versions >= 81
    package = Package("six")
    assert package.number_versions >= 27
    package = Package("pcap2map")
    assert package.number_versions == 1


def test_get_author_email():
    """Test get_author_email function"""
    package = Package("portunus")
    assert package.author_email == "clewis@iqt.org"


def test_get_author_name():
    """Test get_author_name function"""
    package = Package("networkml")
    assert package.author_name == "cglewis"
    package = Package("botocore")
    assert package.author_name == "Amazon Web Services"
    package = Package("matplotlib")
    assert package.author_name == "John D. Hunter, Michael Droettboom"


def test_get_home_page():
    """Test get_home_page function"""
    package = Package("urllib3")
    assert package.home_page == "https://urllib3.readthedocs.io/"
    package = Package("awscli")
    assert package.home_page == "http://aws.amazon.com/cli/"
    package = Package("pcap2map")
    assert package.home_page == "https://github.com/jspeed-meyers/pcap2map"


def test_get_pypi_maintainers_list():
    """Test get_pypi_maintainers_list function"""
    package = Package("pcap2map")
    assert package.maintainers_list == ["jspeed-meyers"]
    package = Package("networkml")
    assert package.maintainers_list == ["cglewis", "iqtlabsbot", "jspeed-meyers"]
    package = Package("pytest")
    assert package.maintainers_list == [
        "The_Compiler",
        "anatoly",
        "flub",
        "hpk",
        "nicoddemus",
        "pfctdayelise",
        "ronny",
    ]


def test_get_pypi_maintainers_data():
    """Test get_pypi_maintainers_data function"""
    package = Package("portunus")
    assert len(package.maintainers_data) == 2
    assert isinstance(package.maintainers_data[0], BeautifulSoup)
    assert isinstance(package.maintainers_data[1], BeautifulSoup)
    package = Package("faucet")
    assert len(package.maintainers_data) == 1
    assert isinstance(package.maintainers_data[0], BeautifulSoup)
    package = Package("ryu")
    assert len(package.maintainers_data) == 2
    assert isinstance(package.maintainers_data[0], BeautifulSoup)
    assert isinstance(package.maintainers_data[1], BeautifulSoup)


def test_get_maintainers_account_creation_date():
    """Test get_maintainers_account_creation_date function"""
    package = Package("pcap2map")
    assert package.maintainers_account_creation_date == ["Nov 7, 2019"]
    package = Package("six")
    assert package.maintainers_account_creation_date == []
    package = Package("good")
    assert package.maintainers_account_creation_date == ['Jan 3, 2014']
    package = Package("ryu")
    assert package.maintainers_account_creation_date == ['May 31, 2017']
    package = Package("networkml")
    assert package.maintainers_account_creation_date == ['Jul 24, 2020', 'Nov 7, 2019']

def test_get_number_of_packages_maintained_by_maintainers():
    """Test get_number_of_packages_maintained_by_maintainers"""
    package = Package("pcap2map")
    assert package.number_of_packages_maintained_by_maintainers == ['2']
    package = Package("networkml")
    assert package.number_of_packages_maintained_by_maintainers == ['9', '3', '2']
    package = Package("matplotlib")
    assert package.number_of_packages_maintained_by_maintainers == ['3', '38', '17', '35', '10']
