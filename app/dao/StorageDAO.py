import logging
import boto3
import uuid
from botocore.exceptions import ClientError
from app.exceptions.exceptions import ImageUploadFailed

import mimetypes


def upload_image(image, image_name, bucket):
    s3_client = boto3.client('s3')
    content_type = mimetypes.guess_type(image.filename)[0]
    try:
        s3_client.upload_fileobj(
            image, bucket, f"image_uploads/{image_name}",
            ExtraArgs={'ACL': 'public-read', 'ContentType': content_type})
    except ClientError as e:
        logging.error(e)
        return False
    return True


def format_image_name(image):
    """Format an image name.
    UUID4's are appended to an image's name before being uploaded to S3. This ensures that they are unique
    but still retain some identifiable information when inspecting the S3 files manually.
    """
    name = image.filename.split('.')
    uuid_suffix = str(uuid.uuid4())
    return name[0] + "_" + uuid_suffix + "." + name[1]


def upload_exercise_image(image, bucket):
    filename_with_uuid = format_image_name(image)  # add uuid to end of filename to ensure uniqueness
    if not upload_image(image, filename_with_uuid, bucket):
        return ImageUploadFailed

    return filename_with_uuid


def get_url_for(bucket, region, folder, image_name):
    return f"https://{bucket}.s3-{region}.amazonaws.com/{folder}{image_name}"
