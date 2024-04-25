from unittest.mock import patch

import pytest

from bedrock_bot.models.base_model import ConversationRole
from bedrock_bot.models.claude import Claude3Haiku, Claude3Sonnet, _Claude3


@patch("boto3.client")
def test_create_invoke_body(mock_boto_client):
    model = _Claude3("mock_model_id")
    model.append_message(ConversationRole.USER, "Hello, Claude!")
    body = model._create_invoke_body()
    assert body == {"messages": [{"content": "Hello, Claude!", "role": "user"}]}


@patch("boto3.client")
def test_handle_response(mock_boto_client):
    model = _Claude3("mock_model_id")
    response_body = {"content": [{"type": "text", "text": "Hello, human!"}]}
    response = model._handle_response(response_body)
    assert response == "Hello, human!"


@patch("boto3.client")
def test_handle_response_raises_error(mock_boto_client):
    model = _Claude3("mock_model_id")
    response_body = {"content": [{"type": "image", "url": "example.com/image.jpg"}]}
    with pytest.raises(RuntimeError):
        model._handle_response(response_body)


@patch("boto3.client")
def test_claude3_sonnet_init(mock_boto_client):
    model = Claude3Sonnet()
    assert model._model_id == "anthropic.claude-3-sonnet-20240229-v1:0"


@patch("boto3.client")
def test_claude3_haiku_init(mock_boto_client):
    model = Claude3Haiku()
    assert model._model_id == "anthropic.claude-3-haiku-20240307-v1:0"
