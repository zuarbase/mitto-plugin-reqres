# Mitto Plugin ReqRes

## Introduction

This file is `mitto-plugin-reqres/docs/src/index.md`. Click the `Show Source`
link on any page to see what the source code for the current page looks like.

These contents are the default placed here when the project was created with
cookiecutter.  It is the top-level public page for the project.  If a project is to have
documentation, this file is mandatory.  This file, and the others contained in `src`,
should contain *public* documentation suitable for consumption by anyone.

When published, the HTML content created by the `src` directory will be available in
`https://www.zuar.com/api/mitto/plugin/mitto-plugin-reqres`.

The [Amazon Advertising API](
https://www.zuar.com/api/mitto/plugin/amazon_advertising/
) documentation is a canonical example of what completed documentation should look like
for a plugin.

## Job Configuration Documentation

If mitto-plugin-reqres provides one or more Mitto jobs, the root of the configuration
documentation should be contained in `job.md`.  The `job.md` file should probably be
referenced from `index.md`, though this is not mandatory.

* [Job Configuration](job.md)

## API Documentation

If mitto-plugin-reqres provides an API, the root of the API documentation should be
contained in `api.md`.  The `api.md` file should probably be referenced from `index.md`,
though this is not mandatory.

* [API](api.md)

## Managing Public Documentation

```sh
$ cd mitto-plugin-reqres/docs
$ make clean
$ make schemas    # build Pydantic JSON-Schema documentation, if any
$ make html       # build the HTML
$ make server     # documentation viewable at localhost:8000
$ make publish    # push to https://www.zuar.com/api/mitto/plugin/mitto-plugin-reqres
```

Note: `make publish` overwrites any previously published public documentation for
mitto-plugin-reqres. 

## Managing Private Documentation

```sh
$ cd mitto-plugin-reqres/docs
$ make PVT=Y clean
$ make PVT=Y schemas    # build Pydantic JSON-Schema documentation, if any
$ make PVT=Y html       # build the HTML
$ make PVT=Y server     # documentation viewable at localhost:8000
$ make PVT=Y publish    # push to s3://zuar.com/docsp/mitto-plugin-reqres
```

Note: `make PVT=Y publish` overwrites any previously published private documentation for
mitto-plugin-reqres. 

