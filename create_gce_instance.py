import google.auth
from google.cloud import compute_v1
import uuid

def create_instance(
    project_id: str,
    zone: str,
    instance_name: str,
    machine_type: str = "e2-standard-8",  # 8 vCPUs, 32 GB RAM by default with E2.
                                         # e2-custom-8-8192 would be 8 vCPU 8GB RAM
    source_image_family: str = "debian-11",
    source_image_project: str = "debian-cloud",
    network_name: str = "global/networks/default",
) -> compute_v1.types.Instance:
    """
    Creates a Compute Engine VM instance.

    Args:
        project_id: Project ID for this request.
        zone: The zone to create the instance in.
        instance_name: Name of the new instance.
        machine_type: Machine type of the VM. (e.g., "e2-standard-8")
                      For 8vCPU and 8GB RAM, a custom machine type like "e2-custom-8-8192"
                      or "n1-custom-8-8192" would be more precise.
                      The "e2-standard-8" provides 32GB RAM.
                      Let's adjust to use a custom type for 8GB RAM.
        source_image_family: Source image family for the boot disk.
        source_image_project: Project containing the source image.
        network_name: The name of the network to attach the instance to.
                      Defaults to "global/networks/default".

    Returns:
        The created Instance object.
    """
    instance_client = compute_v1.InstancesClient()

    # Get the latest Debian 11 image.
    image_client = compute_v1.ImagesClient()
    latest_image = image_client.get_from_family(
        project=source_image_project, family=source_image_family
    )

    # Configure the machine type.
    # For 8 vCPUs and 8 GB RAM, we use a custom machine type.
    # Format: zones/{zone}/machineTypes/{type_name}
    # For custom types: zones/{zone}/machineTypes/custom-{CPUS}-{MEMORY_MB}
    # or e.g. zones/{zone}/machineTypes/e2-custom-8-8192
    machine_type_uri = f"zones/{zone}/machineTypes/e2-custom-8-8192"


    # Configure the boot disk
    disk = compute_v1.types.AttachedDisk()
    disk.boot = True
    disk.auto_delete = True
    disk.initialize_params = compute_v1.types.AttachedDiskInitializeParams()
    disk.initialize_params.source_image = latest_image.self_link
    disk.initialize_params.disk_size_gb = 10  # Standard 10GB boot disk

    # Define the instance
    instance = compute_v1.types.Instance()
    instance.name = instance_name
    instance.machine_type = machine_type_uri
    instance.disks = [disk]

    # Configure the network interface
    network_interface = compute_v1.types.NetworkInterface()
    network_interface.name = network_name
    # Add an access config to assign an external IP address (optional)
    access_config = compute_v1.types.AccessConfig()
    access_config.name = "External NAT"
    access_config.type_ = "ONE_TO_ONE_NAT"
    network_interface.access_configs = [access_config]
    instance.network_interfaces = [network_interface]

    print(f"Creating instance {instance_name} in project {project_id} zone {zone}...")

    try:
        operation = instance_client.insert(
            project=project_id, zone=zone, instance_resource=instance
        )

        # Wait for the operation to complete
        print(f"Waiting for operation {operation.name} to complete...")
        operation_client = compute_v1.ZoneOperationsClient()
        while True:
            result = operation_client.get(project=project_id, zone=zone, operation=operation.name)
            if result.status == compute_v1.types.Operation.Status.DONE:
                print("Operation finished.")
                if result.error:
                    print(f"Error during creation: {result.error}")
                    raise Exception(result.error)
                break
            # time.sleep(10) # Consider adding a small delay if running for long operations

        created_instance = instance_client.get(project=project_id, zone=zone, instance=instance_name)
        print(f"Instance {instance_name} created successfully with IP: {created_instance.network_interfaces[0].access_configs[0].nat_ip}")
        return created_instance

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Replace with your project ID and desired zone
    PROJECT_ID = "your-gcp-project-id"
    ZONE = "us-central1-a" # Example zone, choose one appropriate for you
    INSTANCE_NAME = f"realtime-vps-{uuid.uuid4().hex[:6]}" # Unique instance name

    if PROJECT_ID == "your-gcp-project-id":
        print("Please update the PROJECT_ID variable in the script with your GCP project ID.")
    else:
        # Check for Application Default Credentials
        try:
            credentials, project = google.auth.default()
            print("Using Application Default Credentials.")
        except google.auth.exceptions.DefaultCredentialsError:
            print("Could not find Application Default Credentials.")
            print("Please run 'gcloud auth application-default login' or set up credentials manually.")
            print("See https://cloud.google.com/docs/authentication/provide-credentials-adc for more information.")
            exit(1)

        create_instance(
            project_id=PROJECT_ID,
            zone=ZONE,
            instance_name=INSTANCE_NAME,
            # The machine type is now set inside the function to e2-custom-8-8192
        )
