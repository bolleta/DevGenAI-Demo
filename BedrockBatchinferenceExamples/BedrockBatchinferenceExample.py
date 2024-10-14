"""
バッチ推論ジョブ
https://docs.aws.amazon.com/ja_jp/bedrock/latest/userguide/batch-inference.html

"""

import boto3
import time

bedrock = boto3.client(service_name="bedrock")

# 入力用のファイル
inputDataConfig=({
    "s3InputDataConfig": {
        's3InputFormat': 'JSONL',
        "s3Uri": "s3://tnobe-us-east-1-bedrock-batch/input/input.jsonl"
    }
})

# 出力用のフォルダは事前に作成しておく必要あり
outputDataConfig=({
    "s3OutputDataConfig": {
        "s3Uri": "s3://tnobe-us-east-1-bedrock-batch/output/"
    }
})

# モデル ID
modelId="anthropic.claude-3-haiku-20240307-v1:0"
#modelId="amazon.titan-text-express-v1"

# Batch JOB 名
jobName = "my-batch-job-" + time.strftime("%Y%m%d%H%M%S")

# Role ARN
roleArn = "arn:aws:iam::000000000000:role/my-bedrock-batch-role"

# Batch JOB 実行
response=bedrock.create_model_invocation_job(
    roleArn=roleArn,
    modelId=modelId,
    jobName=jobName,
    inputDataConfig=inputDataConfig,
    outputDataConfig=outputDataConfig
)

# Batch JOB ARN の表示
jobArn = response.get('jobArn')
print(f"Job ARN = {jobArn}")

# Batch JOB のステータスを表示
while True:
    time.sleep(30)
    status = bedrock.get_model_invocation_job(jobIdentifier=jobArn)['status']
    print(status)
    if status in ["Completed", "Failed"]:
        break

# Batch JOB の詳細を表示
jobDetail = bedrock.get_model_invocation_job(jobIdentifier=jobArn)
print(jobDetail)
