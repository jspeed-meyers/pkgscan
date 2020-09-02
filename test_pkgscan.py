"""Tests for pkgscan"""

from main import Package
from helpers import sort_semantic_version

def test_sort_semantic_version():
    """Test sort_semantic_version function"""
    unsorted_list = ["0.3.2", "0.1.1", "5.5.5"]
    sorted_list = sort_semantic_version(unsorted_list)
    assert sorted_list == ["0.1.1", "0.3.2", "5.5.5"]

def test_PackageClass():
    """Test instantiation of package class"""
    package = Package("requests")

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

def test_get_author_email():
    """Test get_author_email function"""
    package = Package("portunus")
    assert package.author_email == "clewis@iqt.org"


