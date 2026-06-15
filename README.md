# 🔀 Dataverse OpenAPI to OpenCollection

# 📖 Introduction
This repository automatically converts a Dataverse OpenAPI specification into an OpenCollection ([Bruno](https://www.usebruno.com/)) collection using GitHub Actions and the [vacuum CLI](https://quobix.com/vacuum/commands/). It also publishes a Swagger UI site for interactive API documentation and testing.

# ✨ Features

## 🇨 OpenCollection (Bruno)

This repository is designed for direct import into [Bruno](https://www.usebruno.com/) as an API collection.

**Environments**

Two pre-configured environments are included:

| Environment | Base URL |
|-------------|----------|
| `prod`      | `https://borealisdata.ca/api/` |
| `demo`      | `https://demo.borealisdata.ca/api/` |

You can switch between environments without changing your requests. To use a different Dataverse instance, update the `baseUrl` in `demo.yml` or `prod.yml` under `dataverse_endpoints/environments/`.

**Authentication**

Every request is pre-configured to include the `X-Dataverse-Key` header, sourced from the `X_Dataverse_Key` secret variable in each environment.

- Endpoints that **do not require authentication** will work with the header left empty.
- Endpoints that **require authentication** will need the variable populated with a valid API token.

---

## 🌐 Swagger UI

A live [Swagger UI](https://kenlhlui.github.io/dataverse_opencollection) is available for browsing and
testing all defined Dataverse API endpoints interactively — no local setup required.

# ✅ Prerequisites
Your Dataverse instance must have the OpenAPI specification enabled. You can check if it's enabled by navigating to `https://your-dataverse-instance/openapi`. You can also check the [OPENAPI_AVAILABILITY.md](OPENAPI_AVAILABILITY.md) for availability across different Dataverse instances.

To use this repository with [Bruno](https://www.usebruno.com/downloads), you will also need to install [Git](https://git-scm.com/install/).

# 🚀 Usage
1. Fork this repository.
2. Enable GitHub Actions in your forked repository.
3. Change the URL in the `dv.txt` file to point to your Dataverse instance. For example, if your Dataverse instance is hosted at `https://demo.dataverse.org` (without the trailing slash), you would change the line in `dv.txt` to: ```https://demo.dataverse.org```.
4. Update the `baseUrl` values in demo.yml/prod.yml under dataverse_endpoints/environments/ with your demo/prod Dataverse instances.
5. Change the values under `servers` in custom_config.yaml file to your dataverse instance as well.
6. Commit and push the changes to your forked repository.
7. The GitHub Action will automatically run and convert the Dataverse OpenAPI specification to an OpenCollection specification, and commit the changes to the main branch of your forked repository.
8. A [Swagger UI](https://swagger.io/) page will also be deployed with the URL https://{YOUR_GITHUB_USER_NAME}.github.io/dataverse_opencollection/

# 🐶 Bruno
See the video below for instructions on importing this repository into Bruno and using it to work with the API endpoints.

https://github.com/user-attachments/assets/60499d97-3021-4323-a4b1-294d253e9377

# 💬 Relevant discussion
Relevant discussion about OpenAPI specification in Harvard Dataverse Project:
 - [Use OpenAPI standard for Dataverse API's (Swagger) #5794](https://github.com/IQSS/dataverse/issues/5794)
 - [Add Swagger like UI to view and call APIs #11994](https://github.com/IQSS/dataverse/issues/11994)
 - [Improve OpenAPI with detailed descriptions and auth requirements #12437](https://github.com/IQSS/dataverse/issues/12437)

# ⚖️ License
[MIT](LICENSE)
