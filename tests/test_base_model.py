import json
from io import BytesIO
from unittest.mock import patch

import pytest

from bedrock_bot.models.base_model import ConversationRole, _BedrockModel


@pytest.fixture
@patch("boto3.client")
def model(mock_boto_client):
    model = _BedrockModel()
    return model


def test_reset(model):
    model.append_message(ConversationRole.USER, "Hello")
    model.reset()
    assert model.messages == []


def test_append_message(model):
    model.append_message(ConversationRole.USER, "Hello")
    assert model.messages == [{"role": "user", "content": "Hello"}]


@patch("bedrock_bot.models.base_model._BedrockModel._invoke")
def test_invoke(mock_internal_invoke, model):
    mock_internal_invoke.return_value = "Hello, world!"

    response = model.invoke("Hello")
    assert response == "Hello, world!"
    assert model.messages == [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hello, world!"},
    ]


def test_create_invoke_body(model):
    with pytest.raises(NotImplementedError):
        model._create_invoke_body()


def test_handle_response(model):
    with pytest.raises(NotImplementedError):
        model._handle_response({})


@patch("bedrock_bot.models.base_model._BedrockModel._create_invoke_body")
@patch("bedrock_bot.models.base_model._BedrockModel._handle_response")
def test_internal_invoke(mock_handle_response, mock_create_invoke_body, model):
    model._bedrock.invoke_model.return_value = {"body": BytesIO(json.dumps({"text": "Hello, world!"}).encode())}
    model.model_params = {"param1": "2"}
    model._model_id = "some-model"

    mock_create_invoke_body.return_value = {"foo": "bar"}
    mock_handle_response.return_value = "handle response return value"

    print(f"foooo: {model._handle_response()}")

    response = model._invoke()
    assert response == "handle response return value"
    model._bedrock.invoke_model.assert_called_once_with(modelId=model._model_id, body='{"foo": "bar", "param1": "2"}')
