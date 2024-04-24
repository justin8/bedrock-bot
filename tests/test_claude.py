from unittest.mock import patch

import pytest

from bedrock_bot.models.base_model import ConversationRole
from bedrock_bot.models.claude import Claude3Haiku, Claude3Sonnet, _Claude3


def test_create_invoke_body():
    model = _Claude3("mock_model_id")
    model.append_message(ConversationRole.USER, "Hello, Claude!")
    body = model._create_invoke_body()
    assert body == {"messages": [{"content": "Hello, Claude!", "role": "user"}]}


def test_handle_response():
    model = _Claude3("mock_model_id")
    response_body = {"content": [{"type": "text", "text": "Hello, human!"}]}
    response = model._handle_response(response_body)
    assert response == "Hello, human!"


def test_handle_response_raises_error():
    model = _Claude3("mock_model_id")
    response_body = {"content": [{"type": "image", "url": "example.com/image.jpg"}]}
    with pytest.raises(RuntimeError):
        model._handle_response(response_body)


def test_claude3_sonnet_init():
    model = Claude3Sonnet()
    assert model._model_id == "anthropic.claude-3-sonnet-20240229-v1:0"


def test_claude3_haiku_init():
    model = Claude3Haiku()
    assert model._model_id == "anthropic.claude-3-haiku-20240307-v1:0"
