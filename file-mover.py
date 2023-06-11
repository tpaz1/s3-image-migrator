import boto3
from PIL import Image
import io
import yaml

class Endpoint:
    def __init__(self, endpoint, access_key, private_access_key):
        self.endpoint = endpoint
        self.access_key = access_key
        self.private_access_key = private_access_key

def convert_image_to_jpg(image):
    if image.format != 'JPEG':
        buffered = io.BytesIO()
        image.save(buffered, format='JPEG')
        buffered.seek(0)
        return Image.open(buffered)
    return image

def move_images(source_bucket, source_endpoint, source_access_key, source_private_access_key,
                destination_bucket, destination_endpoint, destination_access_key, destination_private_access_key):
    # Connect to source and destination S3 endpoints
    source_session = boto3.session.Session(aws_access_key_id=source_access_key,
                                           aws_secret_access_key=source_private_access_key)
    source_s3 = source_session.resource('s3', endpoint_url=source_endpoint)
    
    destination_session = boto3.session.Session(aws_access_key_id=destination_access_key,
                                                aws_secret_access_key=destination_private_access_key)
    destination_s3 = destination_session.resource('s3', endpoint_url=destination_endpoint)

    # List all objects in the source bucket
    bucket = source_s3.Bucket(source_bucket)
    objects = bucket.objects.all()

    for obj in objects:
        # Check if the object is an image and its format is PNG
        if obj.key.lower().endswith('.png'):
            image_object = source_s3.Object(source_bucket, obj.key)
            image_data = io.BytesIO(image_object.get()['Body'].read())
            image = Image.open(image_data)
            
            # Convert the image to JPEG format
            image = convert_image_to_jpg(image)
            
            # Upload the converted image to the destination bucket
            destination_s3.Object(destination_bucket, obj.key).put(Body=image.tobytes(),
                                                                   ContentType='image/jpeg')
            print(f"Image '{obj.key}' converted and moved to the destination bucket.")
            
        else:
            # If the object is not a PNG image, simply copy it to the destination bucket
            source_s3.Object(source_bucket, obj.key).copy_from(
                CopySource={'Bucket': source_bucket, 'Key': obj.key},
                MetadataDirective='COPY',
                ContentType=source_s3.Object(source_bucket, obj.key).content_type
            )
            print(f"Image '{obj.key}' moved to the destination bucket.")

def read_endpoints_from_yaml(file_path):
    with open(file_path, 'r') as file:
        endpoints_data = yaml.safe_load(file)

    source_endpoint_data = endpoints_data.get('source')
    destination_endpoint_data = endpoints_data.get('destination')

    source_endpoint = Endpoint(source_endpoint_data['endpoint'], source_endpoint_data['access_key'], source_endpoint_data['private_access_key'])
    destination_endpoint = Endpoint(destination_endpoint_data['endpoint'], destination_endpoint_data['access_key'], destination_endpoint_data['private_access_key'])

    return source_endpoint, destination_endpoint

def main():
    # Read endpoint details from YAML file
    endpoints_file = 'endpoints.yaml'
    source_endpoint, destination_endpoint = read_endpoints_from_yaml(endpoints_file)

    # Call the move_images function with the endpoint details
    move_images('source-bucket', source_endpoint.endpoint, source_endpoint.access_key, source_endpoint.private_access_key,
                'destination-bucket', destination_endpoint.endpoint, destination_endpoint.access_key, destination_endpoint.private_access_key)

# Call the main function to start the execution
if __name__ == '__main__':
    main()
