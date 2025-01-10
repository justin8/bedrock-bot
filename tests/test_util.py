from bedrock_bot.util import sanitize_filename


def test_sanitize_filename():
    assert sanitize_filename("test.pdf") == "test"
    assert sanitize_filename("test file.pdf") == "test file"
    assert sanitize_filename("test_file.pdf") == "test_file"
    assert sanitize_filename("test-file.pdf") == "test-file"
    assert sanitize_filename("test(file).pdf") == "test(file)"
    assert sanitize_filename("test[file].pdf") == "test[file]"
    assert sanitize_filename("test   filename.pdf") == "test filename"
    assert sanitize_filename("test.file.name.md") == "test file name"
