"""Tests for pkgscan"""

from bs4 import BeautifulSoup

from main import Package
from pypi_pkg import sort_semantic_version

# Instantiate all packages once and only once
awscli = Package("awscli", False)
botocore = Package("botocore", False)
django = Package("django", False)
faucet = Package("faucet", False)
good = Package("good", False)
matplotlib = Package("matplotlib", False)
networkml = Package("networkml", False)
numpy = Package("numpy", False)
pandas = Package("pandas", False)
pcap2map = Package("pcap2map", True)
portunus = Package("portunus", False)
pytest = Package("pytest", False)
requests = Package("requests", False)
ryu = package = Package("ryu", False)
scapy = Package("scapy", False)
six = Package("six", True)
urllib3 = Package("urllib3", False)


def test_sort_semantic_version():
    """Test sort_semantic_version function"""
    unsorted_list = ["0.3.2", "0.1.1", "5.5.5"]
    sorted_list = sort_semantic_version(unsorted_list)
    assert sorted_list == ["0.1.1", "0.3.2", "5.5.5"]


def test_package_class():
    """Test instantiation of package class"""
    Package("requests", False)  # pylint: disable=unused-variable


def test_get_first_release_date():
    """Test get_first_release_date function"""
    assert requests.pypi_pkg["first_release_date"] == "2011-02-14"
    assert numpy.pypi_pkg["first_release_date"] == "2006-12-02"


def test_get_last_release_date():
    """Test get_last_release_date function

    To avoid breaking this test when there is a change to an often
    updated package, this test uses pcap2map, a personal project of
    John Speed Meyers on PyPI that is not maintained.
    """
    assert pcap2map.pypi_pkg["last_release_date"] == "2020-04-10"


def test_get_number_versions():
    """Test get_number_versions function"""
    assert pandas.pypi_pkg["number_versions"] >= 81
    assert six.pypi_pkg["number_versions"] >= 27
    assert pcap2map.pypi_pkg["number_versions"] == 1


def test_get_author_email():
    """Test get_author_email function"""
    assert portunus.pypi_pkg["author_email"] == "clewis@iqt.org"


def test_get_author_name():
    """Test get_author_name function"""
    assert networkml.pypi_pkg["author_name"] == "cglewis"
    assert botocore.pypi_pkg["author_name"] == "Amazon Web Services"
    assert matplotlib.pypi_pkg["author_name"] == "John D. Hunter, Michael Droettboom"


def test_get_home_page():
    """Test get_home_page function"""
    assert urllib3.pypi_pkg["home_page"] == "https://urllib3.readthedocs.io/"
    assert awscli.pypi_pkg["home_page"] == "http://aws.amazon.com/cli/"
    assert pcap2map.pypi_pkg["home_page"] == "https://github.com/jspeed-meyers/pcap2map"


def test_is_pypi_package_signed():
    """Test is_pypi_package_signed functionality"""
    assert not pcap2map.pypi_pkg["pypi_pkg_signed"]
    assert django.pypi_pkg["pypi_pkg_signed"]


def test_get_pypi_maintainers_list():
    """Test get_pypi_maintainers_list function"""
    assert pcap2map.pypi_pkg["maintainers_list"] == ["jspeed-meyers"]
    assert networkml.pypi_pkg["maintainers_list"] == [
        "cglewis",
        "iqtlabsbot",
        "jspeed-meyers",
    ]
    assert pytest.pypi_pkg["maintainers_list"] == [
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
    assert len(portunus.pypi_profiles["maintainers_data"]) == 2
    assert isinstance(portunus.pypi_profiles["maintainers_data"][0], BeautifulSoup)
    assert isinstance(portunus.pypi_profiles["maintainers_data"][1], BeautifulSoup)
    assert len(faucet.pypi_profiles["maintainers_data"]) == 1
    assert isinstance(faucet.pypi_profiles["maintainers_data"][0], BeautifulSoup)
    assert len(ryu.pypi_profiles["maintainers_data"]) == 2
    assert isinstance(ryu.pypi_profiles["maintainers_data"][0], BeautifulSoup)
    assert isinstance(ryu.pypi_profiles["maintainers_data"][1], BeautifulSoup)


def test_get_maintainers_account_creation_date():
    """Test get_maintainers_account_creation_date function"""
    assert pcap2map.pypi_profiles["maintainers_account_creation_date"] == [
        "Nov 7, 2019"
    ]
    assert six.pypi_profiles["maintainers_account_creation_date"] == []
    assert good.pypi_profiles["maintainers_account_creation_date"] == ["Jan 3, 2014"]
    assert ryu.pypi_profiles["maintainers_account_creation_date"] == ["May 31, 2017"]
    assert networkml.pypi_profiles["maintainers_account_creation_date"] == [
        "Jul 24, 2020",
        "Nov 7, 2019",
    ]


def test_get_number_of_packages_maintained_by_maintainers():
    """Test get_number_of_packages_maintained_by_maintainers"""
    assert pcap2map.pypi_profiles["number_of_packages_maintained_by_maintainers"] == [
        "2"
    ]
    assert networkml.pypi_profiles["number_of_packages_maintained_by_maintainers"] == [
        "9",
        "3",
        "2",
    ]
    assert matplotlib.pypi_profiles["number_of_packages_maintained_by_maintainers"] == [
        "3",
        "38",
        "17",
        "35",
        "10",
    ]


def test_get_github_page():
    """Test get_github_page function"""
    assert (
        pcap2map.github_page_data["github_page"]
        == "https://github.com/jspeed-meyers/pcap2map"
    )
    assert (
        networkml.github_page_data["github_page"]
        == "https://github.com/IQTLabs/NetworkML"
    )
    assert requests.github_page_data["github_page"] == "https://github.com/psf/requests"


def test_get_github_data():
    """Test get_github_data function"""
    if pcap2map.github_page_data["github_data_source"] == "API":
        assert pcap2map.github_page_data["github_data"]["id"] == 254624727
    else:
        assert isinstance(pcap2map.github_page_data["github_data"], BeautifulSoup)
    if scapy.github_page_data["github_data_source"] == "API":
        assert scapy.github_page_data["github_data"]["id"] == 254624727


def test_get_github_stars():
    """Test get_github_stars function"""
    assert pcap2map.github_page_data["github_stars"] in [0, "0"]
    if requests.github_page_data["github_data_source"] == "API":
        assert requests.github_page_data["github_stars"] > 43000
    else:
        # Check only first couple of numbers since github stars is constantly
        # increasing for requests. This tests will eventually break, probably
        # around thanksgiving 2020.
        assert requests.github_page_data["github_stars"][0:2] == "43"


def test_count_number_downloads():
    """Test count_number_downloads function"""
    assert requests.downloads["data"]["last_month"] > 50000000
    assert pcap2map.downloads["data"]["last_month"] < 1000


def test_number_releases_past_year():
    """Test number_releases_past_year function"""
    # These tests could break.
    assert networkml.pypi_pkg["number_releases_past_year"] >= 4
    assert requests.pypi_pkg["number_releases_past_year"] >= 2
    assert pcap2map.pypi_pkg["number_releases_past_year"] >= 1


def test_bandit_static_analysis():
    """Test bandit static analysis results"""
    assert pcap2map.static_analysis["bandit"]["count_all"] == 0
    assert six.static_analysis["bandit"]["count_all"] == 1
    assert six.static_analysis["bandit"]["count_medium"] == 1


def test_pylint_static_analysis():
    """Test pylint static analysis results"""
    assert six.static_analysis["pylint"]["average_lint_score"] in [4.73, "No files found"]
    assert pcap2map.static_analysis["pylint"]["average_lint_score"] in [6.84, "No files found"]