from dataclasses import dataclass
from typing import Optional

from kink import di
from vertexai import init
from vertexai.generative_models import GenerativeModel, Part


@dataclass
class GoogleVertexService:
    def __post_init__(self):
        init(project=di["GOOGLE_GCP_PROJECT_ID"], location=di["GOOGLE_GCP_REGION"])

    def chat(
        self,
        model_name: str,
        content: str,
        system_instructions: Optional[list[str]] = None,
    ) -> str:
        model = GenerativeModel(
            model_name=model_name,
            system_instruction=[
                Part.from_text(instruction) for instruction in system_instructions
            ]
            if system_instructions
            else None,
        )
        history = []
        chat_instance = model.start_chat(history=history)

        # start_datetime = datetime.now(tz=timezone.utc)
        response = chat_instance.send_message(content=Part.from_text(text=content))
        candidates = response.candidates
        # usage_metadata = response.usage_metadata
        # end_datetime = datetime.now(tz=timezone.utc)
        output = candidates.pop().content.parts.pop().text
        return output
