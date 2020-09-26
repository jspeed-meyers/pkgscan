"""Functions to download package from pip and perform static analysis"""

import glob
import os
import re
import shutil
import subprocess
import sys
import zipfile

import pandas as pd


def download_and_unzip_package(package):
    """Download via pip the desired package and then unzip"""

    # TODO: Will this work for all downloads? Are they all .whl files?
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

    # Identify and unzip any .whl files
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
            # Count number of vulnerabilities by severity
            bandit["count_all"] = len(df)
            bandit["count_low"] = len(df[df.issue_severity == "LOW"])
            bandit["count_medium"] = len(df[df.issue_severity == "MEDIUM"])
            bandit["count_high"] = len(df[df.issue_severity == "HIGH"])
        except:
            bandit["count_all"] = "Error"
    return bandit


def generate_pylint_files():
    """Run pylint against each .py file and create folder of output files"""

    # Identify all .py files recursively
    # TODO: Why do I need both globs? Investigate glob more
    file_list = glob.glob("pkg-source/**/*.py")
    file_list.extend(glob.glob("pkg-source/*.py"))

    # Create directory to store pylint output files
    os.mkdir("pkg-source/pylint")

    # Run pylint againt each file and store output as text files
    for file in file_list:
        # Extract name for storing a text file of pylint output per file
        file_name_with_extension = os.path.basename(file)
        file_name_no_extension = os.path.splitext(file_name_with_extension)[0]
        results_file_path = os.path.join(
            "pkg-source", "pylint", file_name_no_extension + ".txt"
        )
        try:
            # Run pylint and pipe output to a text file for later analysis
            output_file = open(results_file_path, "w")
            subprocess.check_call(["pylint", file], stdout=output_file)
        except subprocess.CalledProcessError:
            pass


def generate_pylint_dict():
    """Create dict storing pylint-related data"""

    # Create pylint output for all .py files
    generate_pylint_files()

    # Dict for returning pylint data
    pylint = {}

    # List to store pylint code scores for each .py file
    lint_scores = []

    # Find all text files storing pylint output
    file_list = glob.glob("pkg-source/pylint/*.txt")
    for file in file_list:
        # Read in file contents
        with open(file, "r") as f:
            try:
                # Extract line that contains score (quirk of pylint)
                score_line = f.readlines()[-4]
                # Check that score line exists at all
                if score_line:
                    # Find first occurrence of score
                    score_match = re.search(r"[\d]+.\d\d?", score_line)
                    # Check that score number exists
                    if score_match:
                        score = score_match.group(0)
                        lint_scores.append(float(score))
            # TODO: Make more robust. Why do index errors occur?
            except IndexError:
                continue

    # Take average of lint scores
    # TODO: Why is no files found sometimes?
    if len(lint_scores) == 0:
        pylint["average_lint_score"] = "No files found"
    else:
        average_lint_score = sum(lint_scores) / len(lint_scores)
        pylint["average_lint_score"] = round(average_lint_score, 2)

    return pylint


def remove_package_and_static_analysis_artifacts():
    """Remove directory that stored static analysis objects"""
    shutil.rmtree("pkg-source")
