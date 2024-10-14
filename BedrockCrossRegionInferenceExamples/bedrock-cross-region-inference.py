"""
Example of cross-region inference in Amazon Bedrock
https://aws.amazon.com/jp/blogs/machine-learning/getting-started-with-cross-region-inference-in-amazon-bedrock/

"""
import boto3
import json

primary_region ="us-east-1" #us-east-1, eu-central-1
bedrock_runtime = boto3.client("bedrock-runtime", region_name= primary_region)
inferenceProfileId = 'us.anthropic.claude-3-5-sonnet-20240620-v1:0' 

system_prompt = "You are an expert on AWS AI services."
input_message = "Tell me about AI service for Foundation Models"

##########################################################################
# Example with Converse API
print("----- Converse API -----")

response = bedrock_runtime.converse(
    modelId = inferenceProfileId,
    system = [{"text": system_prompt}],
    messages=[{
        "role": "user",
        "content": [{"text": input_message}]
    }],
    inferenceConfig={"maxTokens": 2048},
)

print(response['output']['message']['content'][0]['text'])

##########################################################################
# Example with invokeModel API
print("----- invokeModel API -----")

# Format the request payload using the model's native structure.
native_request = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 2048,
    "system": system_prompt,
    "messages": [
        {
            "role": "user",
            "content": [{"type": "text", "text": input_message}],
        }
    ],
}

# Convert the native request to JSON.
request = json.dumps(native_request)

response = bedrock_runtime.invoke_model(modelId=inferenceProfileId, body=request)

model_response = json.loads(response["body"].read())
response_text = model_response["content"][0]["text"]
print(response_text)
