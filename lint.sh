#!/bin/bash
set -e
ruff="poetry run ruff"

echo "Running linter..."
$ruff check bedrock_bot tests

echo "Checking for formatting errors..."
$ruff format --check
