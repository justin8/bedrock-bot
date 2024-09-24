import logging
from io import StringIO
from unittest.mock import MagicMock, patch

import click
import pytest
from click.testing import CliRunner

from bedrock_bot.cli import (
    available_models,
    configure_logger,
    get_user_input,
    handle_input_files,
    main,
    model_class_from_input,
)
from bedrock_bot.models.claude import Claude3Haiku


class ModelStub:
    def __init__(self, name):
        self.name = name
        self.messages = []

    def reset(self):
        self.messages = []

    def invoke(self, user_input):
        return f"Response for: {user_input}"


@patch("bedrock_bot.cli.model_list", [ModelStub("foo")])
def test_available_models():
    assert available_models() == ["foo"]


def test_configure_logger():
    with patch("bedrock_bot.cli.logging.basicConfig") as mock_basic_config:
        configure_logger(verbose=False)
        mock_basic_config.assert_called_once_with(level=logging.ERROR)

        configure_logger(verbose=True)
        mock_basic_config.assert_called_with(level=logging.INFO)


def test_get_user_input():
    with patch("sys.stdin", StringIO("Input from stdin")), patch(
        "builtins.input", return_value="Input from prompt"
    ), patch("sys.exit") as mock_exit, patch("sys.stdin.isatty", return_value=True):
        assert get_user_input() == "Input from prompt"


def test_handle_input_files():
    file1 = StringIO("File 1 content")
    file2 = StringIO("File 2 content")

    file1.name = "file1"
    file2.name = "file2"

    assert handle_input_files([file1, file2]) == [
        "File 'file1':\nFile 1 content",
        "File 'file2':\nFile 2 content",
    ]
    assert handle_input_files([]) == []


def test_model_class_from_input():
    assert model_class_from_input("claude-3-haiku") == Claude3Haiku
    with pytest.raises(click.BadParameter):
        model_class_from_input("invalid-model")


@pytest.fixture
def runner():
    return CliRunner()


@patch("bedrock_bot.cli.sys.stdin", new_callable=StringIO)
@patch("bedrock_bot.cli.model_class_from_input")
def test_main_stdin(mock_model_class_from_input, mock_stdin, runner, monkeypatch):
    mock_stdin.write("Hello\n")
    mock_stdin.seek(0)
    monkeypatch.setattr("sys.stdin", mock_stdin)
    result = runner.invoke(main, input="Hello\n")
    assert "Note that stdin is not supported for input" in result.output


@patch("bedrock_bot.cli.sys.stdin.isatty", return_value=False)
@patch("bedrock_bot.cli.model_class_from_input")
def test_main_non_tty_input(mock_model_class_from_input, mock_isatty, runner):
    mock_model_class_from_input()().name = "model-name"
    result = runner.invoke(main, input="Hello\n")
    print(result.output)
    assert "Note that stdin is not supported for input" in result.output


@patch("bedrock_bot.cli.sys.stdin.isatty", return_value=True)
@patch("builtins.input", return_value="Hello")
@patch("bedrock_bot.cli.model_class_from_input")
def test_main_tty_input(mock_model_class_from_input, mock_input, mock_isatty, runner):
    result = runner.invoke(main)
    assert "Note that stdin is not supported for input" in result.output


@patch("bedrock_bot.cli.model_class_from_input")
@patch("bedrock_bot.cli.get_user_input", side_effect=["exit"])
def test_main_exit(mock_get_user_input, mock_model_class_from_input, runner):
    result = runner.invoke(main)
    print(result.output)
    assert "Goodbye!" in result.output


@patch("bedrock_bot.cli.model_class_from_input")
@patch("bedrock_bot.cli.get_user_input", side_effect=["reset>", "exit"])
def test_main_reset(mock_get_user_input, mock_model_class_from_input, runner):
    result = runner.invoke(main)
    assert "Resetting conversation..." in result.output
