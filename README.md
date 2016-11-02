# GH2S3

It downloads [GitHub Archive](https://www.githubarchive.org/) 2016 data and uploads it to an Amazon S3 bucket.

It's preferred to run it inside an Amazon EC2 instance, for better bandwidth and latency.

## Run locally

With Python 3 and pip:

```shell
pip install -r requirements.txt
```

You need to setup your AWS credentials, [the same way it's done with AWS CLI](https://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration).

Then run:

```shell
export S3_BUCKET=YOUR_BUCKET
./gh2s3.py
```

## With Docker

```shell
docker build -t gh2s3 .

docker run \
    --rm \
    -e "AWS_ACCESS_KEY_ID=YOUR_ID" \
    -e "AWS_SECRET_ACCESS_KEY=YOUR_KEY" \
    -e "S3_BUCKET=YOUR_BUCKET" \
    gh2s3
```
