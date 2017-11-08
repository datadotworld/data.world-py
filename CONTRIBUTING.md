# Contributing Guidelines

### Issues
Our issue tracker can be used to report issues and propose changes to the current or next version of the data.world API specification.

Please follow these guidelines before opening an issue:

- Make sure your issue is not a duplicate.
- Make sure your issue is relevant to the specification.
# Contribute Code

### Fork the Project

Fork the project [on Github](https://github.com/datadotworld/data.world-py) and check out your copy.

```sh
$ git clone https://github.com/[YOUR_GITHUB_NAME]/data.world-py.git
$ cd data.world-py
$ git remote add upstream https://github.com/datadotworld/data.world-py.git
```

### Install and Test

Run the command below to install packages required:

```sh
$ python setup.py install
```

Run tests:

```sh
$ python setup.py test
```

### Updating Swagger Definition

Once new API endpoints/paths are introduced, there is a need to update `data.world-py/datadotworld/client/swagger-dwapi-def.json` file with [data.world APIs swagger.json](https://api.data.world/v0/swagger.json) and also need to re-generate `_swagger` package. Running the Makefile in the project folder root allows us do the updates and regenerating with one command.

First, install [swagger-codegen](https://swagger.io/swagger-codegen/).

#### Installing swagger-codegen with Homebrew

```sh
$ brew install swagger-codegen
```

`swagger-codegen` should now be a recognisable command.

Run;

```sh
$ make update_swagger_codegen
```

This will update `data.world-py/datadotworld/client/swagger-dwapi-def.json` and also regenerate `_swagger` package.

You can also run tests:

```sh
$ make test
```

### Checking the API endpoints

There are various ways you can access the list of endpoints;

* Using the [Swagger Editor](https://editor.swagger.io/)

> Copy the content of `swagger-dwapi-def.json` file and paste it in the swagger editor console. You can get the swagger editor either by navigating to the swagger editor on web https://editor.swagger.io/ or installing locally.

#### Installing swagger editor

Clone swagger editor
```sh
$ git clone https://github.com/swagger-api/swagger-editor.git
```
Navigate to swagger-editor folder
```sh
cd swagger-editor
```

Run:
```sh
$ npm install
$ npm run build
$ npm start
```

it should now be running on you local machine at http://127.0.0.1:3001 if the port is available.

* You can also import the `swagger-dwapi-def.json` file into Postman.

### Create a Feature Branch
```sh
$ git checkout master
$ git pull upstream master
$ git checkout -b my-feature-branch
```

### Write Tests
Try to write a test that reproduces the problem you're trying to fix or describes a feature that you want to build. Add tests to spec.

We definitely appreciate pull requests that highlight or reproduce a problem, even without a fix.

Once tests are written, we always make sure that the test coverage is up to 90%, otherwise builds will fail.

To check test coverage, run the fellowing command;
```sh
$ coverage run setup.py test && coverage report
```

NB: Coverage reports below 90% will fail on build.

### Write Code

Implement your feature or bug fix. Make sure that all tests pass without errors.

Also, to make sure that your code follows our coding style guide and best practises, run the command;
```sh
$ flake8
```
Make sure to fix any errors that appear if any.

NB: Builds will fail if warnings flagged by flake8 are not addressed

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

### Thank you!
Thank you in advance, for contributing to this project!
