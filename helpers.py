"""Helper functions"""

from packaging import version

def sort_semantic_version(unsorted_list):
    """Sort a list of semantic version numbers"""
    sorted_list = sorted(unsorted_list, key=lambda x: version.Version(x))
    return sorted_list
