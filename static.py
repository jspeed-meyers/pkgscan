"""Functions to download package from pip and perform static analysis"""

import glob
import os
import shutil
import subprocess
import sys
import zipfile

import pandas as pd


def download_and_unzip_package(package):
    """Download via pip the desired package and then unzip"""

    # TODO: Will this work for all downloads? Are they all tar files?
    # TODO: In the future, analyze dependencies too.

    if os.path.exists("pkg-source"):
        shutil.rmtree("pkg-source")
    os.mkdir("pkg-source")

    # Download from pip and place in pkg-source directory
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "-q",
            "download",
            "--no-dependencies",
            "--destination-directory",
            "pkg-source/.",
            package,
        ]
    )

    # Identify and unzip any .tar or .gz files
    file_list = glob.glob("pkg-source/*.whl")
    for file in file_list:
        with zipfile.ZipFile(file, "r") as zip_ref:
            zip_ref.extractall("pkg-source")


def generate_bandit_csv():
    """Run bandit and generate csv of results"""
    try:
        subprocess.check_call(
            [
                "bandit",
                "--quiet",  # Suppress output
                "--recursive",
                "--format",
                "csv",
                "-o",
                "pkg-source/bandit.csv",  # output file path
                "--ignore-nosec",  # ignore the nosec designation
                "pkg-source",
            ]
        )
    except:
        pass


def generate_bandit_dict():
    """Parse bandit csv and return count of issues"""
    generate_bandit_csv()
    bandit = {}
    if os.path.exists("pkg-source/bandit.csv"):
        try:
            df = pd.read_csv("pkg-source/bandit.csv")
            # TODO: Add additional analyses
            bandit["count"] = len(df)
        except:
            bandit["count"] = "Error"
    return bandit


def remove_package_and_static_analysis_artifacts():
    """Remove directory that stored static analysis objects"""
    shutil.rmtree("pkg-source")
