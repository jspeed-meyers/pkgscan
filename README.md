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

Feature | Utility | Difficulty
--------------- | --------------- | --------------- 
maintainer's pypi account creation date | High | Low
number of other projects maintained by maintainers | High | Low
Check for any github link | High | Low
Count number downloads | High | Low
Github and pypy actually linked | High | High
Recent change in package maintainers | High | High
Measure package committer turnover | High | High
Correspondence between github and PyPI code | High | High
Similar name to often downloaded package? | High | High
Run bandit and report | High | High
Create aggregate risk score | High | High
Make pkgscan work with requirements.txt | High | High
'# github stars' | Low | Low

## Potential Mini-Research Project
Use libraries.io to do analysis of metadata present for packages previously
yanked from PyPI to determine completeness and utility of features above. This
analysis would help create additional useful software features and help prioritize
the development of these features.