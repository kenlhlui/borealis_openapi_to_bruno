# /// script
# dependencies = [
#   "httpx2",
# ]
# ///

"""Checks the OpenAPI specification availability across Dataverse installations and export a Markdown file with the results.""" 
import httpx2
import asyncio
from pathlib import Path

from dataclasses import dataclass
from datetime import datetime, UTC
from urllib.parse import urljoin
from html import escape

SEM = asyncio.Semaphore(20)
HEADERS={
        "User-Agent": "Dataverse-OpenAPI-Checker/1.0"
    }


@dataclass
class DataverseInstallation:
    name: str
    hostname: str
    url: str | None = None
    openapi_available: bool = False


def get_dv_installations(source_url: str) -> dict:
    """Fetches the list of Dataverse installations from the specified source.
    
    Args:
        source_url: URL to fetch the Dataverse installations JSON data.

    Returns:
        A dictionary containing the list of Dataverse installations.
    """


    response = httpx2.get(source_url, timeout=None)

    if response.is_success:
        return response.json()
    else:
        raise ValueError("Failed to fetch Dataverse installations")


def read_records_from_json(json_data: dict) -> list:
    """Reads the records from the provided JSON data.

    Args:
        json_data: A dictionary containing the JSON data with Dataverse installations.
    
    Returns:
        A list of records extracted from the JSON data.
    """
    dv_installations = []

    for record in json_data.get('installations', []):
        name = record.get('name')
        hostname = record.get('hostname')
        dv_installations.append(DataverseInstallation(name=name, hostname=hostname,))
    
    return dv_installations


SEM = asyncio.Semaphore(20)


async def check_openapi(
    client: httpx2.AsyncClient,
    hostname: str,
) -> str | None:
    """
    Check whether a Dataverse installation exposes an OpenAPI endpoint.

    Args:
        client: Shared async HTTP client.
        hostname: Dataverse hostname.

    Returns:
        The OpenAPI URL if found, otherwise None.
    """

    endpoints = (
        "openapi",
        "api/openapi",
        "openapi.json",
    )

    async with SEM:
        for endpoint in endpoints:
            url = urljoin(f"https://{hostname}", endpoint)

            try:

                response = await client.get(
                    url,
                    timeout=30,
                    follow_redirects=True,
                )

                if response.is_success:
                    return url

            except Exception:
                pass

    return None


async def test_openapi_availability(
    dv_installations: list[DataverseInstallation],
) -> list[DataverseInstallation]:
    """
    Test OpenAPI availability for all Dataverse installations concurrently.

    Args:
        dv_installations: List of Dataverse installations.

    Returns:
        Updated list with openapi_available and url populated.
    """

    async with httpx2.AsyncClient(headers=HEADERS, verify=False) as client:

        tasks = [
            check_openapi(client, dv.hostname)
            for dv in dv_installations
        ]

        results = await asyncio.gather(*tasks)

        for dv, openapi_url in zip(dv_installations, results):
            if openapi_url:
                dv.openapi_available = True
                dv.url = openapi_url

    return dv_installations


def generate_report(dv_installations: list) -> str:
    """Generate a GitHub-compatible HTML status report."""

    rows = []

    overall_availability = sum(dv.openapi_available for dv in dv_installations)
    total_installations = len(dv_installations)
    availability_percentage = (overall_availability / total_installations * 100) if total_installations > 0 else 0

    for dv in dv_installations:
        status = "✅" if dv.openapi_available else "❌"

        hostname = escape(dv.hostname)
        name = escape(dv.name)

        hostname_link = (
            f'<a href="https://{hostname}">{hostname}</a>'
            if hostname
            else "-"
        )

        openapi_link = (
            f'<a href="{dv.url}">OpenAPI</a>'
            if dv.url
            else "-"
        )

        rows.append(
            f"""
<tr>
  <td>{status}</td>
  <td>{name}</td>
  <td>{hostname_link}</td>
  <td>{openapi_link}</td>
</tr>"""
        )

    return f"""# Dataverse OpenAPI Availability

_Last updated: {datetime.now(tz=UTC).strftime("%Y-%m-%d %H:%M:%S %Z")}_

_Overall availability: {overall_availability}/{total_installations} ({availability_percentage:.2f}%)_

> [!WARNING]
> Availability results are based on automated checks performed from GitHub Actions. Some installations may block automated traffic or be temporarily unavailable due to maintenance, resulting in false negatives. If you believe an availability result is incorrect, please verify it with the installation administrators.

<table>
  <thead>
    <tr>
      <th>Status</th>
      <th>Installation</th>
      <th>Hostname</th>
      <th>OpenAPI Endpoint</th>
    </tr>
  </thead>
  <tbody>
{''.join(rows)}
  </tbody>
</table>
"""


if __name__ == "__main__":
    dv_installations = get_dv_installations('https://raw.githubusercontent.com/IQSS/dataverse-installations/refs/heads/main/data/data.json')
    if not dv_installations:
        print("No Dataverse installations found.")
        exit(1)
    dv_installations = read_records_from_json(dv_installations)
    dv_installations_updated = asyncio.run(
    test_openapi_availability(dv_installations))
    md_content = generate_report(dv_installations_updated)
    Path("OPENAPI_AVAILABILITY.md").write_text(md_content, encoding="utf-8")