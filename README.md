# pkgscan
Scan PyPI package metadata to assess security risks

## Motivation
Make it easier to assess the provenance of the package and associated maintainers
on PyPI to enable an informed assessment of the package. Moreover, make this
process quicker than clicking through PyPI and related links.

## Usage
`$ git clone https://github.com/jspeed-meyers/pkgscan.git`

`$ cd pkgscan`

`pip install -r requirements.txt`

`$ python main.py [package_name]`

For instance:

```
$ python main.py requests
First release date: 2011-02-14
Number of versions: 140
Home page: https://requests.readthedocs.io
Github link: https://github.com/psf/requests
Author email: me@kennethreitz.org
Author name: Kenneth Reitz
Maintainer usernames: Lukasa graffatcolmingov nateprewitt
Maintainer accounts creation dates: Feb 12, 2017
Number of packagages maintained by maintainers:  23 66 4
Github stars: 43533
Number of PyPI downloads in past month: 63819668
```


## Unit Tests
`pytest`

## Roadmap

Feature | Utility | Difficulty | Category | Completed
--------------- | --------------- | --------------- | --------------- | ---------------
maintainer's pypi account creation date | High | Low | Identity | X
number of projects maintained by maintainers | High | Low | Identity | X
Means of tying back to known entity | High | High | Identity |
Check for any github link | High | Low | Metadata | X
Count number downloads | High | Low | Metadata | X
Check if package is signed | High | Low | Metadata | X
'# github stars' | Low | Low | Metadata | X
Number of releases past year | Low | Low | Metadata | X
Github and PyPI actually linked | High | High | Metadata |
Recent change in package maintainers | High | High | Metadata |
Measure package committer turnover | High | High | Metadata |
Similar name to often downloaded package? | High | High | Metadata |
Check for tying back to signed commit | High | Low | Metadata |
Correspondence between github and PyPI code | High | High | Source Code |
Run bandit and report | High | Low | Source Code |
Run pylint and report | High | Low | Source Code |
Run mccabe and report | High | Low | Source Code |
Create aggregate risk score | High | High | Functionality |
Make pkgscan work with requirements.txt | High | Low | Functionality |
Visualize results with HTML | High | Low | Functionality |

## Potential Mini-Research Project
Use libraries.io to do analysis of metadata present for packages previously
yanked from PyPI to determine completeness and utility of features above. This
analysis would help create additional useful software features and help prioritize
the development of these features.
