from main import Package
from helpers import sort_semantic_version

def test_sort_semantic_version():
    """Test sort_semantic_version function"""
    unsorted_list = ["0.3.2", "0.1.1", "5.5.5"]
    sorted_list = sort_semantic_version(unsorted_list)
    assert sorted_list == ["0.1.1", "0.3.2", "5.5.5"]

def test_PackageClass():
    package = Package("requests")

def test_get_first_release_date():
    package = Package("requests")
    assert package.get_first_release_date() == "2011-02-14"
    package = Package("numpy")
    assert package.get_first_release_date() == "2006-12-02"


