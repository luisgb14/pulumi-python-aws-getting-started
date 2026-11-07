"""A private S3 bucket for build artifacts, configured per stack."""

import pulumi
import pulumi_aws as aws

config = pulumi.Config()
versioning = config.get_bool("versioning") or False

tags = {
    "project": pulumi.get_project(),
    "stack": pulumi.get_stack(),
    "managed-by": "pulumi",
}

bucket = aws.s3.Bucket("artifacts", tags=tags)

aws.s3.BucketPublicAccessBlock(
    "artifacts",
    bucket=bucket.id,
    block_public_acls=True,
    block_public_policy=True,
    ignore_public_acls=True,
    restrict_public_buckets=True,
)

if versioning:
    aws.s3.BucketVersioning(
        "artifacts",
        bucket=bucket.id,
        versioning_configuration={"status": "Enabled"},
    )

pulumi.export("bucket_name", bucket.id)
pulumi.export("bucket_uri", pulumi.Output.concat("s3://", bucket.id))
pulumi.export("versioning", versioning)
