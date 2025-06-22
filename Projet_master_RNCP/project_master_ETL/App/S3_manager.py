from dotenv import load_dotenv
import os
import boto3

# Load environment variables from the .env file
load_dotenv('env/.env')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
BUCKET_NAME = os.getenv('BUCKET_NAME')

# Initialise S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def list_S3_contents(bucket_name=BUCKET_NAME):
    response = s3.list_objects_v2(Bucket=bucket_name)
    contents = response.get("Contents", [])
    simplified_contents = [
        {
            "Key": obj["Key"],
            "Size": obj["Size"]
        }
        for obj in contents
    ]
    print("Contents in S3 bucket:")
    for item in simplified_contents:
        print(f"{item['Key']} | {item['Size']} bytes")
    return simplified_contents



def upload_file_to_s3(file_path, bucket=BUCKET_NAME, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_path)
    s3.upload_file(file_path, bucket, object_name)
    print(f"[INFO] File {object_name} upload inside {bucket} S3 bucket")


def download_file_from_s3_to_path(object_name, out_path, bucket=BUCKET_NAME):
    complete_dump_path = os.path.join(out_path, object_name)
    s3.download_file(bucket, object_name, complete_dump_path)
    print(f"[INFO] Download S3 {object_name} File and stock here: {out_path}")