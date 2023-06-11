# s3-image-migrator
# S3 Image Migration

This Python script allows you to migrate images from one S3-compatible storage endpoint to another. It supports moving images from a specific bucket in the source endpoint to a bucket in the destination endpoint. Additionally, it checks if the image is in PNG format and converts it to JPEG before moving it to the destination.

## Prerequisites

- Python 3.x
- `boto3` library: You can install it using `pip install boto3`
- `Pillow` library: You can install it using `pip install Pillow`

## Getting Started

1. Clone the repository or download the source code.
2. Install the required dependencies mentioned in the Prerequisites section.
3. Create a YAML file named `endpoints.yaml` in the same directory as the script. The file should contain the endpoint details for the source and destination storage. Refer to the example YAML file provided in the repository.
4. Modify the endpoint URLs and bucket names in the script to match your private cloud storage configuration.
5. Run the script using `python image_migration.py`.

## Configuration

The `endpoints.yaml` file is used to store the endpoint details. It should have the following structure:

```yaml
source:
  endpoint: 'source-endpoint'
  access_key: 'source-access-key'
  private_access_key: 'source-private-access-key'

destination:
  endpoint: 'destination-endpoint'
  access_key: 'destination-access-key'
  private_access_key: 'destination-private-access-key'
```
Make sure to replace the placeholder values with the actual endpoint URLs and access keys for your private cloud storage.

## Usage

Once you have set up the configuration, run the script by executing the image_migration.py file. The script will connect to the source and destination endpoints, list the images in the source bucket, and perform the following actions:

If the image is in PNG format, it will convert it to JPEG format before moving it to the destination bucket.
If the image is already in JPEG format or any other format, it will directly move it to the destination bucket.
The script will print messages indicating the status of each image migration operation.

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

