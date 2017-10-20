# Contributing Guidelines

### General
### Issues

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

Once new API endpoints/paths are introduced, there is a need to update `data.world-py/datadotworld/client/swagger-dwapi-def.json` file with [data.world APIs swagger.json](https://api.data.world/v0/swagger.json).

So, navigate to [data.world APIs swagger.json](https://api.data.world/v0/swagger.json), copy the and paste the json into the `data.world-py/datadotworld/client/swagger-dwapi-def.json` file in your project folder.

You will also need to re-generate `_swagger` package. This can be done be installing [swagger-codegen](https://swagger.io/swagger-codegen/).

#### Installing swagger-codegen with Homebrew

```sh
$ brew install swagger-codegen
```

`swagger-codegen` should now be a recognisable command.

Alternatively, there's a Makefile in the project folder root that allows us do the updates and regenerating with one command.

Once you have installed [swagger-codegen](https://swagger.io/swagger-codegen/), run;

```sh
$ make update_swagger_codegen
```

This will update `data.world-py/datadotworld/client/swagger-dwapi-def.json` and also regenerate `_swagger` package.

You can also run tests by:

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

### Write Tests

### Write Code

### Write Documentation

### Commit Changes

### Push

### Make a Pull Request

### Conventions

### Thank you!