from unittest.mock import patch

import pytest

from bedrock_bot.models.base_model import ConversationRole
from bedrock_bot.models.nova import NovaLite, NovaMicro, NovaPro, _Nova


@patch("boto3.client")
def test_create_invoke_body(mock_boto_client):
    model = _Nova("mock_model_id")
    model.append_message(ConversationRole.USER, "Hello, Nova!")
    body = model._create_invoke_body()
    assert body == {"messages": [{"role": "user", "content": [{"text": "Hello, Nova!"}]}]}


@patch("boto3.client")
def test_handle_response(mock_boto_client):
    model = _Nova("mock_model_id")
    response_body = {"output": {"message": {"content": [{"text": "Hello, human!"}]}}}
    response = model._handle_response(response_body)
    assert response == "Hello, human!"


@patch("boto3.client")
def test_handle_response_raises_error(mock_boto_client):
    model = _Nova("mock_model_id")
    response_body = {"output": {"message": {"content": [{"type": "image", "url": "example.com/image.jpg"}]}}}
    with pytest.raises(RuntimeError):
        model._handle_response(response_body)


@patch("boto3.client")
def test_nova_lite_init(mock_boto_client):
    model = NovaLite()
    assert model._model_id == "us.amazon.nova-lite-v1:0"


@patch("boto3.client")
def test_nova_micro_init(mock_boto_client):
    model = NovaMicro()
    assert model._model_id == "us.amazon.nova-micro-v1:0"


@patch("boto3.client")
def test_nova_pro_init(mock_boto_client):
    model = NovaPro()
    assert model._model_id == "us.amazon.nova-pro-v1:0"
