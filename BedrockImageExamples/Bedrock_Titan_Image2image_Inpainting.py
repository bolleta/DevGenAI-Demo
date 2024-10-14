"""
イメージの Inpainting (Titan)
https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-image.html
"""
import logging
import datetime
import json
import boto3
from botocore.exceptions import ClientError

### For Image
#from PIL import Image
import base64
import io

logger = logging.getLogger(__name__)


print("---" * 42)
print("Titan")
print("---" * 42)

prompt_data = "a car in the woods"
mask_data = "a car"

try:
    image_file = "car-woods.jpg"
    
    image_data = None
    
    with open(image_file,"rb") as f:
        image_data = f.read()
    
    base64_data = base64.b64encode(image_data).decode()
    
    
    bedrock_runtime = boto3.client('bedrock-runtime')
    
    body = json.dumps({
            "taskType": "INPAINTING",
            "inPaintingParams": {
                "image": base64_data,                         
                "text":  prompt_data,
                "negativeText": "bad quality, low res",        
                "maskPrompt": mask_data
            },                                                 
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "height": 1024,
                "width": 1024,
                "cfgScale": 7.0
            }
        }
            
    )

    modelId = 'amazon.titan-image-generator-v1'
    accept = "application/json"
    contentType = "application/json"

    response = bedrock_runtime.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )
    # body は StreamingBody オブジェクトで返されるので read() で取得する
    response_body = json.loads(response.get("body").read())
    
    # body の base64: に base64 でエンコードされたイメージがある
    base64_image = response_body.get("images")[0]
    
    # base64コードからファイルに保存するには、バイナリに戻す
    image_bytes = base64.b64decode(base64_image)
    dt_now = str(datetime.datetime.now())
    with open(f"{dt_now}.png", "wb") as f:
        f.write(image_bytes)
    print(f'save to "{dt_now}.png".')    
    
    
    # # Pillow を使ってファイルに書く方法
    # base64_bytes = base64_image.encode('ascii')
    # image_bytes = base64.b64decode(base64_bytes)
    # dt_now = datetime.datetime.now()
    # image = Image.open(io.BytesIO(image_bytes))
    # image.save(str(dt_now) + ".png")
    

except ClientError as error:
    if error.response['Error']['Code'] == 'AccessDeniedException':
           print(f"\x1b[41m{error.response['Error']['Message']}\
                \nTo troubeshoot this issue please refer to the following resources.\
                 \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
                 \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")

    else:
        raise error
