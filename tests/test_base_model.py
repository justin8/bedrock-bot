import json
from io import BytesIO
from unittest.mock import patch, mock_open

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
    assert model.messages == [{"role": "user", "content": [{"text": "Hello"}]}]


@patch("bedrock_bot.models.base_model._BedrockModel._invoke")
def test_invoke(mock_internal_invoke, model):
    mock_internal_invoke.return_value = "Hello, world!"

    response = model.invoke("Hello")
    assert response == "Hello, world!"
    assert model.messages == [
        {"role": "user", "content": [{"text": "Hello"}]},
        {"role": "assistant", "content": [{"text": "Hello, world!"}]},
    ]


def test_handle_response(model):
    response_body = {"output": {"message": {"content": [{"text": "Hello, human!"}]}}}
    response = model._handle_response(response_body)
    assert response == "Hello, human!"


def test_handle_response_raises_error(model):
    response_body = {"output": {"message": {"content": [{"type": "image", "url": "example.com/image.jpg"}]}}}
    with pytest.raises(RuntimeError):
        model._handle_response(response_body)


@patch("bedrock_bot.models.base_model._BedrockModel._handle_response")
def test_internal_invoke(mock_handle_response, model):
    model._bedrock.converse.return_value = {"output": {"message": {"content": [{"text": "Hello, world!"}]}}}
    model._model_params = lambda: {"param1": "2"}
    model._model_id = "some-model"

    mock_handle_response.return_value = "handle response return value"

    response = model._invoke()
    assert response == "handle response return value"


@patch("pathlib.Path.open", new_callable=mock_open, read_data=b"test_data")
def test_handle_input_file(mock_open, model):
    # Test document file
    file_data = model._handle_input_file("test.pdf")
    assert file_data == {
        "document": {
            "name": "test",
            "format": "pdf",
            "source": {"bytes": b"test_data"},
        }
    }

    # Test image file
    file_data = model._handle_input_file("test.jpg")
    assert file_data == {
        "image": {
            "name": "test",
            "format": "jpeg",
            "source": {"bytes": b"test_data"},
        }
    }

    # Test video file
    file_data = model._handle_input_file("test.mp4")
    assert file_data == {
        "video": {
            "name": "test",
            "format": "mp4",
            "source": {"bytes": b"test_data"},
        }
    }

    # Test unsupported file type
    with pytest.raises(RuntimeError):
        model._handle_input_file("test.exe")
