from unittest.mock import patch

import pytest

from bedrock_bot.models.base_model import ConversationRole
from bedrock_bot.models.claude import Claude3Haiku, Claude3Sonnet, _Claude3


@patch("boto3.client")
def test_claude3_sonnet_init(mock_boto_client):
    model = Claude3Sonnet()
    assert model._model_id == "anthropic.claude-3-sonnet-20240229-v1:0"


@patch("boto3.client")
def test_claude3_haiku_init(mock_boto_client):
    model = Claude3Haiku()
    assert model._model_id == "anthropic.claude-3-haiku-20240307-v1:0"
