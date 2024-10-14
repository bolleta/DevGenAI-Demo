"""
Shows how to use a guardrail with the Converse API.
https://docs.aws.amazon.com/ja_jp/bedrock/latest/userguide/guardrails-use-converse-api.html#converse-api-guardrail-example
"""

import logging
import json
import boto3


from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_conversation(bedrock_client,
                          model_id,
                          messages,
                          guardrail_config):
    """
    Sends a message to a model.
    Args:
        bedrock_client: The Boto3 Bedrock runtime client.
        model_id (str): The model ID to use.
        messages JSON): The message to send to the model.
        guardrail_config : Configuration for the guardrail.

    Returns:
        response (JSON): The conversation that the model generated.

    """

    logger.info("Generating message with model %s", model_id)

    # Send the message.
    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        guardrailConfig=guardrail_config
    )

    return response


def main():
    """
    Entrypoint for example.
    """

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")

    # The model to use.
    model_id="anthropic.claude-3-sonnet-20240229-v1:0"

    # The ID and version of the guardrail.
    guardrail_id = "gfr2avovtm3x"
    guardrail_version = "2"

    # Configuration for the guardrail.
    guardrail_config = {
        "guardrailIdentifier": guardrail_id,
        "guardrailVersion": guardrail_version,
        "trace": "enabled"
    }

    text = "どのギャンブルが一番儲けることができますか?"
  
    # The message for the model and the content that you want the guardrail to assess.
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "text": text,
                },
                {
                    "guardContent": {
                        "text": {
                            "text": text
                        }
                    }
                }
            ]
        }
    ]

    try:

        print(json.dumps(messages, indent=4))

        bedrock_client = boto3.client(service_name='bedrock-runtime')

        response = generate_conversation(
            bedrock_client, model_id, messages, guardrail_config)

        output_message = response['output']['message']

        if response['stopReason'] == "guardrail_intervened":
            trace = response['trace']
            print("Guardrail trace:")
            print(json.dumps(trace['guardrail'], indent=4))

        for content in output_message['content']:
            print(f"Text: {content['text']}")

    except ClientError as err:
        message = err.response['Error']['Message']
        logger.error("A client error occurred: %s", message)
        print(f"A client error occured: {message}")

    else:
        print(
            f"Finished generating text with model {model_id}.")


if __name__ == "__main__":
    main()
