# Analysis of urban growth using decadal remote sensing data

This project is designed to facilitate the big geodata solution developmen and deployment for urrban growth change mapping using GIS, Remote Sensing and Databricks ecosystem.This repository contains a comprehensive set of instruction and workflow to set up the big geodata solution on cloud or docker.

- Web app: [streamlit Dashboard](https://kaykaushal-big-geodata-urban-growth-streamlit-app-w3prjd.streamlit.app/)
- Source code: <https://github.com/kaykaushal/big_geodata_urban_growth>

## Project workflow and technology stack
### Web App Instruction:

1. Pull the [GitHub repository](https://github.com/kaykaushal/big_geodata_urban_growth)
2. Create new python env and insatll package from ```requirements.txt```
3. Run streamlit local or push it on streamlit [community cloud](https://streamlit.io/cloud)

## Project Structure

This project has the following structure to a depth of 2.

```

├── README.md
├── docker-compose.yml
├── env
│   └── docker
├── example
├── scripts
│   └── development.py
├── src
│   ├── config.py
│   ├── operations.py
│   └── utility.py
└── tests
    ├── data
    └── spark
```

- **`doc`** - contains documentation associated with this project
- **`docker-compose.yml`** - defines the local development docker services
- **`env/docker`** - contains the `Dockerfile` and `requirements.txt` used to define the Python environment for local development
- **`example`** - contains a built-out example for how to use this project structure
- **`scripts`** - contains python scripts used for exploration and development purposes (**TODO**) discuss how to use these with Databricks and with JupyterLab
- **`src`** - contains source code
- **`tests/data`** - contains fixture data used during testing
- **`tests/spark`** - contains unit and integration tests


## Development

![](https://github.com/kaykaushal/big_geodata_urban_growth/blob/439e59efd9e20028f4e731c347334d72b80ae7d9/Picture%201.png)

Databricks cluster creation and pipeline setup in aws.

### Running Tests Locally

Run tests against the local package using the `make` commands below.

Run a single test file:

```
make run-test testfile=<PATH_TO_TEST_FILE>
```

Run all tests:

```
make run-tests
```
