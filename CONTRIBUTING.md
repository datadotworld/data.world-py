# Contributing Guidelines

### Issues

Issue reports are a great way to contribute to this project.
To the extent possible, make sure that your issue is detailed and not a duplicate.

# Contribute Code

### Fork the Project

Fork the project [on Github](https://github.com/datadotworld/data.world-py) and check out your copy.

```sh
$ git clone https://github.com/[YOUR_GITHUB_NAME]/data.world-py.git
$ cd data.world-py
$ git remote add upstream https://github.com/datadotworld/data.world-py.git
```
### Install and Test
#### Python Version Support
The following list of python versions have been tested and have been found to work with the SDK.
This is not a conclusive list and should be amended to include other versions that have worked for others:
 -  3.5.9


Run the command below to install packages required:

```sh
$ pip install -e .
```

Run tests:

```sh
$ python setup.py test
```

### Create a Feature Branch

```sh
$ git checkout master
$ git pull upstream master
$ git checkout -b my-feature-branch
```
### Running Swagger-codegen
Should you find the need to run swagger-codegen, you will need to make changes to some generated code in order to address an issue with OAuth.
You can refer to the issue for more details: https://github.com/swagger-api/swagger-codegen/issues/10968
After running swagger-codegen, you will need to update the `configurations.py` file by adding this [function](https://github.com/datadotworld/data.world-py/pull/120/files#diff-097089a848b0e5d38d7a980e2d1ffea3e687f544e286573cf79ef0297ba1e118R197-R202), and using it in the `auth_settings` function over [here](https://github.com/datadotworld/data.world-py/pull/120/files#diff-097089a848b0e5d38d7a980e2d1ffea3e687f544e286573cf79ef0297ba1e118R225).
### Write Tests

Try to write a test that reproduces the problem you're trying to fix or describes a feature that you want to build. Add tests to spec.

We definitely appreciate pull requests that highlight or reproduce a problem, even without a fix.

### Write Code

Implement your feature or bug fix. Make sure that all tests pass without errors.

Also, to make sure that your code follows our coding style guide and best practises, run the command;

```sh
$ flake8
```

Make sure to fix any errors that appear if any.

### Write Documentation

Document any external behavior in the [README](https://github.com/datadotworld/data.world-py/blob/master/README.rst).

### Commit Changes

Make sure git knows your name and email address:

```sh
git config --global user.name "Your Name"
git config --global user.email "contributor@example.com"
```

Writing good commit logs is important. A commit log should describe what changed and why.

```sh
git add ...
git commit
```

### Push

```sh
git push origin my-feature-branch
```

### Make a Pull Request

Go to https://github.com/[YOUR_GITHUB_NAME]/data.world-py.git and select your feature branch. Click the 'Pull Request' button and fill out the form. Pull requests are usually reviewed within a few days.

# Release (for maintainers)

Checklist:

- Build passes `tox` verification (all tests across versions, test coverage, and code style)
- Version number is correct in `datadotworld/__init__.py`
- All docs are updated, including `README.rst` and `/docs`

Release process:

1. Create a GitHub release (and respective tag)
2. Push respective tag to `release` branch (i.e. `git push origin [tag]^{}:release`)

# Thank you!

Thank you in advance, for contributing to this project!
