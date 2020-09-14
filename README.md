# pkgscan
Scan PyPI package metadata to assess security risks

## Usage
`python main.py [package_name]`

## Motivation
Make it easier to assess the provenance of the package and associated maintainers
on PyPI to enable an informed assessment of the package. Moreover, make this
process quicker than clicking through PyPI and related links.

UNDER DEVELOPMENT!

## Roadmap

Feature | Utility | Difficulty | Category
--------------- | --------------- | --------------- | ---------------- 
maintainer's pypi account creation date | High | Low | Identity
number of other projects maintained by maintainers | High | Low | Identity
Check for any github link | High | Low | Metadata
Count number downloads | High | Low | Metadata
Check if package is signed | High | Low | Metadata
Github and PyPI actually linked | High | High | Metadata
Recent change in package maintainers | High | High | Metadata
Measure package committer turnover | High | High | Metadata
Correspondence between github and PyPI code | High | High | Source Code
Similar name to often downloaded package? | High | High | Metadata
Run bandit and report | High | High | Source Code
Run pylint and report | High | High | Source Code
Create aggregate risk score | High | High | Functionality
Make pkgscan work with requirements.txt | High | Low | Functionality 
'# github stars' | Low | Low | Metadata
Mean time between releases | Low | Low | Metadata
Means of tying back to known entity | High | High | Identity 
Check for tying back to signed commit | High | Low | Metadata

## Potential Mini-Research Project
Use libraries.io to do analysis of metadata present for packages previously
yanked from PyPI to determine completeness and utility of features above. This
analysis would help create additional useful software features and help prioritize
the development of these features.
