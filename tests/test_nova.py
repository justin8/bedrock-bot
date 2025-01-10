from unittest.mock import patch

import pytest

from bedrock_bot.models.base_model import ConversationRole
from bedrock_bot.models.nova import NovaLite, NovaMicro, NovaPro, _Nova


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
