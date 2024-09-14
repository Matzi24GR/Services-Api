# CPSV-API

A REST API designed to convert Linked Open Data (LOD) from public services, formatted in RDF (Resource Description Framework) using the Core Public Service Vocabulary Application Profile (CPSV-AP), into JSON format. This API simplifies the integration of LOD into modern applications, making public service data more accessible for developers.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation) 
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Docker Setup](#docker-setup)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Extending the API](#extending-the-api)
- [License](#license)

## Overview

Linked Open Data (LOD) has become crucial for promoting transparency and interoperability in public services. However, RDF-based LOD adoption faces challenges due to its complexity. The **CPSV-API** resolves this by providing a user-friendly API to transform RDF into JSON, making it easier to integrate public service data into modern software applications.

## Features

- **SPARQL Querying**: Retrieve public service data using SPARQL.
- **JSON Output**: Converts RDF data to JSON, making it easy to work with in most modern applications.
- **RESTful Endpoints**: Access public service data, organizations, legal resources, and more through REST API endpoints.
- **Docker Integration**: Deploy the API quickly and reliably using Docker.
- **Extensible Architecture**: Easily add support for new data sources by extending the provider interface.

## Tech Stack

- **Python**: Core language of the project.
- **FastAPI**: High-performance web framework for the API.
- **RDFLib**: Library for working with RDF data.
- **SPARQLWrapper**: Interface for querying SPARQL endpoints.
- **YAML**: Configuration files for flexibility.
- **Docker**: For containerized deployment and consistent environment setup.

## Setup and Installation

### Requirements

- Python 3.8+
- Docker (optional but recommended)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Matzi24GR/Services-Api
    cd Services-Api
    ```
   
2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```
   
3. Edit ```config.yaml``` to specify your data sources and SPARQL endpoints.

4. Run the API:

    ```bash
    uvicorn app.main:app --reload
    ```
### Docker Setup

1. Build the Docker image:

    ```bash
    docker build -t cpsv-api .
    ```
   
2. Start the API using Docker Compose:

    ```bash
    docker-compose up
    ```
   
## API Endpoints

The following RESTful endpoints are available:

- GET /providers: Lists all active data providers.
- GET /services: Returns a merged list of public services from all data providers.
- GET /services/{id}: Fetches details of a specific public service by id.
- GET /organizations: Returns all public organizations related to the services.
- GET /evidences: Lists all evidences/documents required for the services.
- GET /requirements: Lists all service requirements.
- GET /rules: Returns all rules governing the services.
- GET /legalResources: Lists legal resources linked to public services.
- GET /outputs: Lists the outputs or results of services.

Configuration

The API can be configured using two YAML files:

1. ```config.yaml```: This file defines the data sources and their SPARQL endpoints. Example configuration:

    ```yaml
    providers:
        - tag: "bdti-mitos"
          name: "BDTI Virtuoso With Mitos Data"
          cpsv_version: "3.1.1"
          type: sparql
          url: "https://virtuoso-1706142355.p1.bdti.dataplatform.tech.ec.europa.eu/sparql/"
          graph_uri: "https://mitos.gov.gr:8890/"
    ```
2. ```provider/sparql/data/{version}-config.yaml```: These files, located in the provider/sparql/data folder, provide version-specific configuration for each CPSV-AP version. The {version}-config.yaml file maps the CPSV-AP JSON-LD vocabulary to the endpoints for data retrieval. This allows dynamic construction of SPARQL queries based on the configuration.

    Example of a ```3.1.1-config.yaml``` file:
    
    ```yaml
    queries:
      getRequirements:
        target: Requirement
        elements:
          - Requirement.fulfils
          - Requirement.hasSupportingEvidence
          - Requirement.identifier
          - Requirement.name
          - Requirement.type
    ```
    Each version of CPSV-AP is mapped using a corresponding JSON-LD file, allowing seamless integration of various vocabulary versions. You can configure and modify how each data element is retrieved through these files.

# Extending the API

To add a new data source class:

1. Implement a new provider class by extending the ```Provider``` interface.
2. Define SPARQL queries in the corresponding YAML configuration file located in ```provider/sparql/data```.
3. Register the new provider in ```config.yaml``` and implement the corresponding endpoints in the API.

The current design is flexible and allows for future extension without altering the core logic of the API.
# License

This project is licensed under the [European Union Public License (EUPL)](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12).
