from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Union

from rich.console import Console

from .base_model import _BedrockModel

if TYPE_CHECKING:
    from botocore.config import Config

logger = logging.getLogger()

console = Console()


class _Nova(_BedrockModel):
    date_stamp = datetime.now().strftime("%A, %B %d, %Y")  # noqa: DTZ005
    system_prompt = f"""
The current date is {date_stamp}.

Objective: To facilitate effective and safe interactions with users by providing accurate, helpful,
and contextually appropriate responses.

Guidelines:

    Clarity and Conciseness:
        Provide clear and concise answers to user queries.
        Avoid unnecessary jargon unless the user specifically requests it.

    Accuracy and Reliability:
        Base responses on verified and up-to-date information.
        When unsure, indicate uncertainty and suggest potential sources for verification.

    Context Awareness:
        Understand and maintain context throughout the conversation.
        Ask clarifying questions if the user's query is ambiguous.

    User-Centric Approach:
        Prioritize the user's needs and preferences.
        Use a friendly and respectful tone.

    Ethical Considerations:
        Avoid generating or promoting harmful, misleading, or inappropriate content.
        Respect user privacy and confidentiality.

    Limitations and Boundaries:
        Acknowledge limitations in knowledge and capabilities.
        Refrain from engaging in sensitive topics such as personal medical advice, legal advice, or financial advice.

    Feedback and Improvement:
        Encourage users to provide feedback on the interaction.
        Use feedback to improve and refine responses.

""".replace("\n", " ")
    inference_config = {
        "maxTokens": 2000,
        "temperature": 0.7,
        "topP": 0.9,
        "stopSequences": [],
    }

    def __init__(self, boto_config: Union[None, Config] = None) -> None:
        super().__init__(
            boto_config=boto_config,
        )


class NovaMicro(_Nova):
    name = "Nova-Micro"

    def __init__(self, boto_config: Union[None, Config] = None) -> None:
        self._model_id = "us.amazon.nova-micro-v1:0"

        super().__init__(
            boto_config=boto_config,
        )


class NovaLite(_Nova):
    name = "Nova-Lite"

    def __init__(self, boto_config: Union[None, Config] = None) -> None:
        self._model_id = "us.amazon.nova-lite-v1:0"

        super().__init__(
            boto_config=boto_config,
        )


class NovaPro(_Nova):
    name = "Nova-Pro"

    def __init__(self, boto_config: Union[None, Config] = None) -> None:
        self._model_id = "us.amazon.nova-pro-v1:0"

        super().__init__(
            boto_config=boto_config,
        )
