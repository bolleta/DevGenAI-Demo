import boto3

# Bedrock Agent Client
kb_agent = boto3.client(service_name='bedrock-agent-runtime')

# 
model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
model_arn = f'arn:aws:bedrock:us-east-1::foundation-model/{model_id}'
kb_id = "XXXXXXXXXX" # Knowkedge BaseのID
prompt = "AnyCompany社では、社員が結婚するときの休暇は何日ですか？"
#prompt = "AnyCompany社では、6か月以上勤務した場合に与えられる有給休暇は何日ですか？"

# retrieve_and_generate
response = kb_agent.retrieve_and_generate(
    input={
        'text': prompt
    },
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': kb_id,
            'modelArn': model_arn
        }
    },
)

# result

generated_text = response['output']['text']
print(generated_text)