import os, boto3, botocore

print("keys set:", bool(os.getenv("AWS_ACCESS_KEY_ID")), bool(os.getenv("AWS_SECRET_ACCESS_KEY")))

try:
    ident = boto3.client("sts").get_caller_identity()
    print("account:", ident["Account"])
    print("arn    :", ident["Arn"])
except Exception as e:
    print("STS failed:", e)

BUCKET = "my-model-mlopsproj"
s3 = boto3.client("s3", region_name="us-east-1")

try:
    loc = s3.get_bucket_location(Bucket=BUCKET)["LocationConstraint"]
    print("bucket region:", loc or "us-east-1")
except botocore.exceptions.ClientError as e:
    print("get_bucket_location ->", e.response["Error"]["Code"])

try:
    s3.list_objects_v2(Bucket=BUCKET, MaxKeys=1)
    print("list  : OK")
except botocore.exceptions.ClientError as e:
    print("list  ->", e.response["Error"]["Code"])

try:
    s3.put_object(Bucket=BUCKET, Key="_perm_test.txt", Body=b"x")
    print("write : OK")
    s3.delete_object(Bucket=BUCKET, Key="_perm_test.txt")
except botocore.exceptions.ClientError as e:
    print("write ->", e.response["Error"]["Code"])

try:
    print("buckets visible:", [b["Name"] for b in s3.list_buckets()["Buckets"]])
except botocore.exceptions.ClientError as e:
    print("list_buckets ->", e.response["Error"]["Code"])
