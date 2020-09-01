from main import Package

def test_PackageClass():
    package = Package("requests")

def test_get_first_release_date():
    package = Package("requests")
    assert package.get_first_release_date() == "2012-01-22"
    package = Package("numpy")
    assert package.get_first_release_date() == "2012-01-22"


