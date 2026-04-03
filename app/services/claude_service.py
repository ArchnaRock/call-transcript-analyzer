import asyncio
from anthropic import AsyncAnthropic
import json
import logging

logger = logging.getLogger(__name__)


class ClaudeService:
    def __init__(self, api_key: str):
        self.client = AsyncAnthropic(api_key=api_key)

    async def analyze(self, transcript: str) -> dict:
        prompt = f"""
Analyze the following call transcript and return STRICT JSON:

{{
  "qa_score": number (1-10),
  "justification": "one sentence",
  "summary": "2-3 sentences",
  "sentiment": "positive | neutral | negative"
}}

Transcript:
{transcript}
"""

        # retry mechanism (bonus)
        for attempt in range(2):
            try:
                response = await self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=300,
                    temperature=0,
                    messages=[{"role": "user", "content": prompt}],
                )

                content = response.content[0].text

                # Try parsing JSON safely
                data = json.loads(content)

                # Basic validation fallback
                return {
                    "qa_score": int(data.get("qa_score", 5)),
                    "justification": data.get("justification", "No justification provided"),
                    "summary": data.get("summary", "No summary provided"),
                    "sentiment": data.get("sentiment", "neutral"),
                }

            except Exception as e:
                logger.warning(f"Claude attempt {attempt+1} failed: {e}")
                await asyncio.sleep(1)

        # fallback response
        return {
            "qa_score": 5,
            "justification": "Fallback due to processing error",
            "summary": "Could not generate summary",
            "sentiment": "neutral",
        }