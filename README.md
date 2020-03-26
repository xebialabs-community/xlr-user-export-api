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

* Copy the latest JAR file from the [releases page](https://github.com/xebialabs-community/xlr-user-export-api/releases) into the `XL_RELEASE_SERVER/plugins/__local__` directory.
* Restart the XL Release server.

## Usage

To retrieve all users, make an HTTP GET request to...

```bash
http://<your xl release>/api/extension/user-export/users.
```

The response object is similar to the following:

```json
{
	"entity": {
		"roles": [{
			"name": "devops",
			"principals": ["tim"]
		}],
		"users": {
			"admin": {
				"email": "",
				"lastActive": 1585193051078,
				"fullName": "XL Release Administrator",
				"loginAllowed": true,
				"roles": {},
				"folders": {
					"DevOps": {
						"permissions": ["template#edit", "template#lock_task", "template#view", "folder#view", "template#edit_triggers", "template#edit_precondition", "template#create_release", "template#edit_failure_handler"],
						"type": "PRINCIPAL"
					},
					"Samples & Tutorials": {
						"permissions": [],
						"type": "PRINCIPAL"
					}
				}
			},
			"tim": {
				"email": "tim@xebialabs.com",
				"lastActive": null,
				"fullName": "Tim",
				"loginAllowed": true,
				"roles": {
					"devops": {
						"permissions": ["reports#view"]
					}
				},
				"folders": {
					"DevOps": {
						"permissions": ["template#view", "folder#view"],
						"type": "ROLE"
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

Regarding folders, a user may have access to a folder either because they are assigned to the folder as a 'principal', or because
they belong to a 'role' that is assigned to the folder.  As shown in the example above, the folder 'type' property is used to 
distinguish between these cases.

### Pagination

If you have many users, you may want to paginate results.  Use the 'page' and 'resultsPerPage' query parameters to paginate through the results:

```bash
http://<your xl release>/api/extension/user-export/users?page=0&resultsPerPage=10
```

The first page is '0'.

### Find A Specific User

You may limit the search to a single user with the 'userid' query parameter.  For example:

```bash
http://<your xl release>/api/extension/user-export/users?userid=admin
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
