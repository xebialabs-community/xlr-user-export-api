# XL Release User Export API

[![Build Status][xlr-user-export-api-travis-image]][xlr-user-export-api-travis-url]
[![Codacy Badge][xlr-user-export-api-codacy-image] ][xlr-user-export-api-codacy-url]
[![Code Climate][xlr-user-export-api-code-climate-image] ][xlr-user-export-api-code-climate-url]
[![License: MIT][xlr-user-export-api-license-image]][xlr-user-export-api-license-url]
[![Github All Releases][xlr-user-export-api-downloads-image]]()

## Preface

This document describes the functionality provided by the XL Release xlr-user-export-api.

See the [XL Release reference manual](https://docs.xebialabs.com/xl-release) for background information on XL Release and release automation concepts.  

## Overview

This plugin implements a custom REST API that returns users along with their roles, folders, and permissions.

## Requirements
*  **XL Release**   9.0.0+

## Installation

*   Copy the latest JAR file from the [releases page](https://github.com/xebialabs-community/xlr-user-export-api/releases) into the `XL_RELEASE_SERVER/plugins/__local__` directory.
*   Restart the XL Release server.

## Usage

Make an HTTP GET request to https://\<your xl release\>/api/extension/user-export/users.

The response object is similar to the following:

```json
{
  "entity": {
    "users": {
      "tjf": {
        "email": "tfleming@xebialabs.com",
        "lastActive": null,
        "fullName": "Tim Fleming",
        "loginAllowed": true,
        "roles": {
          "dev": {
            "permissions": [
              "global_variables#edit",
              "release#create",
              "template#create",
              "reports#view"
            ]
          }
        },
        "folders": {
          "CustomerService": {
            "permissions": [
              "release#reassign_task"
            ]
          }
        }
      },
      "admin": {
        "email": "",
        "lastActive": 1570754902193,
        "fullName": "XL Release Administrator",
        "loginAllowed": true,
        "roles": {},
        "folders": {
          "CustomerService": {
            "permissions": [
              "folder#edit_variables",
              "group#edit",
              "folder#edit_configuration",
              "folder#view",
              "dashboard#edit",
              "folder#edit_security",
              "folder#edit",
              "dashboard#view",
              "group#view"
            ]
          },
          "Samples & Tutorials": {
            "permissions": [
              "folder#edit_variables",
              "group_definition#edit",
              "group#edit",
              "folder#edit_configuration",
              "folder#view",
              "group_definition#view",
              "dashboard#edit",
              "folder#edit_security",
              "folder#edit",
              "dashboard#view",
              "group#view"
            ]
          }
        }
      }
    }
  },
  "stdout": "",
  "stderr": "",
  "exception": null
}
```

## Developers

### Prerequisites

1. You will need to have Docker and Docker Compose installed.
2. The XL-Release docker container expects to find a valid XL-Release license on your machine, at this location: ~/xl-licenses/xl-release-license.lic.

### Build and package the plugin

Execute the following from the project root directory:

```bash
./gradlew clean assemble
```

Output will be placed in ./build/libs folder.

### To run integration tests

Execute the following from the project root directory:

```bash
./gradlew clean itest
```

The itest will set up a containerized xlr/\<???\> testbed using Docker Compose.

### To run demo or dev version

```bash
cd ./src/test/resources
docker-compose -f docker/docker-compose.yml up
```

NOTE:

1. XL Release will run on the [localhost port 15516](http://localhost:15516/).
2. The XL Release username / password is admin / admin.

[xlr-user-export-api-travis-image]: https://travis-ci.org/xebialabs-community/xlr-user-export-api.svg?branch=master
[xlr-user-export-api-travis-url]: https://travis-ci.org/xebialabs-community/xlr-user-export-api

[xlr-user-export-api-codacy-image]: https://api.codacy.com/project/badge/Grade/88dec34743b84dac8f9aaaa665a99207
[xlr-user-export-api-codacy-url]: https://www.codacy.com/app/ladamato/xlr-user-export-api

[xlr-user-export-api-code-climate-image]: https://codeclimate.com/github/xebialabs-community/xlr-user-export-api/badges/gpa.svg
[xlr-user-export-api-code-climate-url]: https://codeclimate.com/github/xebialabs-community/xlr-user-export-api

[xlr-user-export-api-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-user-export-api-license-url]: https://opensource.org/licenses/MIT
[xlr-user-export-api-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-user-export-api/total.svg
