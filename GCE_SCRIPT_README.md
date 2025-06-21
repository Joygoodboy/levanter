# Google Cloud VM Creation Script (`create_gce_instance.py`)

This document provides instructions on how to set up and run the `create_gce_instance.py` script, which uses the Google Cloud Python client library to create a Compute Engine Virtual Machine (VM) instance.

## Prerequisites

1.  **Google Cloud Project:** You need an active Google Cloud Project.
2.  **Billing Enabled:** Ensure billing is enabled for your project.
3.  **Compute Engine API Enabled:** The Compute Engine API must be enabled for your project. You can enable it from the Google Cloud Console by navigating to "APIs & Services" > "Enabled APIs & services" and clicking "+ ENABLE APIS AND SERVICES", then searching for "Compute Engine API" and enabling it.
4.  **Python:** Python 3.7+ installed on your system.
5.  **pip:** Python package installer.

## Setup Instructions

1.  **Ensure you have the script:**
    The `create_gce_instance.py` script should be in the root directory of this project.

2.  **Install Required Python Libraries:**
    Open your terminal or command prompt and navigate to the project's root directory. Then run:
    ```bash
    pip install google-cloud-compute google-auth
    ```
    If you use a virtual environment for Python (recommended), activate it before running pip install.

3.  **Authenticate with Google Cloud:**
    You need to authenticate your environment so the script can make API calls on your behalf. The recommended way for local development is to use the Google Cloud CLI to set up Application Default Credentials (ADC):

    *   **Install Google Cloud CLI:** If you haven't already, [install the Google Cloud CLI](https://cloud.google.com/sdk/docs/install).
    *   **Login and Set Up ADC:** Run the following command and follow the prompts to log in with your Google account that has permissions for the target project:
        ```bash
        gcloud auth application-default login
        ```
        This command will open a web browser for you to log in and authorize access.

4.  **Configure the Script:**
    Open the `create_gce_instance.py` script in a text editor and update the following placeholder variables:

    *   `PROJECT_ID`: Replace `"your-gcp-project-id"` with your actual Google Cloud Project ID.
    *   `ZONE`: Optionally, change `"us-central1-a"` to your preferred GCP zone (e.g., `"europe-west1-b"`). You can find a list of available zones [here](https://cloud.google.com/compute/docs/regions-zones).

    Example snippet from `create_gce_instance.py`:
    ```python
    if __name__ == "__main__":
        # Replace with your project ID and desired zone
        PROJECT_ID = "your-gcp-project-id"  # <--- UPDATE THIS
        ZONE = "us-central1-a"              # <--- UPDATE THIS (OPTIONAL)
        INSTANCE_NAME = f"realtime-vps-{uuid.uuid4().hex[:6]}"
    ```

## Running the Script

Once you have completed the setup steps:

1.  Navigate to the root directory of the project in your terminal (the directory containing `create_gce_instance.py`).
2.  Run the script using Python:
    ```bash
    python create_gce_instance.py
    ```

The script will then attempt to create a new VM instance with the following specifications:
*   **Name:** `realtime-vps-<random_string>` (a unique name is generated each time)
*   **Machine Type:** `e2-custom-8-8192` (8 vCPUs, 8 GB RAM)
*   **Image:** Latest Debian 11
*   **Boot Disk Size:** 10 GB
*   **Network:** Default network with an external IP address automatically assigned.

You will see log messages indicating the progress. Upon successful creation, the script will print the instance name and its external IP address. If there are issues (e.g., project ID not updated, authentication problems), error messages will be displayed.

## Troubleshooting

*   **`DefaultCredentialsError`:** If you see an error like `google.auth.exceptions.DefaultCredentialsError: Could not automatically determine credentials...`, ensure your authentication is correctly set up by running `gcloud auth application-default login`.
*   **API Not Enabled:** If you get an error like `google.api_core.exceptions.Forbidden: 403 Compute Engine API has not been used in project ... before or it is disabled.`, go to the Google Cloud Console, navigate to "APIs & Services" > "Library", search for "Compute Engine API", and enable it for your project.
*   **Quota Exceeded:** You might encounter errors (e.g., `ZONE_RESOURCE_POOL_EXHAUSTED` or `QUOTA_EXCEEDED`) if your project has insufficient quota for resources like CPUs or IP addresses in the selected region/zone. You may need to request a quota increase from the Google Cloud Console under "IAM & Admin" > "Quotas".
*   **Invalid Zone/Region:** Ensure the `ZONE` you specified is valid and that the `e2-custom-8-8192` machine type (or E2 custom machines in general) are available in that zone.

This script provides a basic framework. You can extend it to customize disk types, sizes, network configurations, add startup scripts, and more by modifying the `compute_v1.types.Instance` object properties within the script. Refer to the [Google Cloud Compute Engine Client Library documentation](https://cloud.google.com/python/docs/reference/compute/latest) for more details.
