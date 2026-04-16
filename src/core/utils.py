"""
Lab 11 - Helper Utilities
"""
from __future__ import annotations

from google.genai import types

from core.config import is_gemini_quota_error, rotate_gemini_key


async def chat_with_agent(agent, runner, user_message: str, session_id=None):
    """Send a message to the agent and get the response.

    Args:
        agent: The LlmAgent instance
        runner: The InMemoryRunner instance
        user_message: Plain text message to send
        session_id: Optional session ID to continue a conversation

    Returns:
        Tuple of (response_text, session)
    """
    user_id = "student"
    app_name = runner.app_name

    session = None
    if session_id is not None:
        try:
            session = await runner.session_service.get_session(
                app_name=app_name, user_id=user_id, session_id=session_id
            )
        except (ValueError, KeyError):
            pass

    if session is None:
        try:
            session = await runner.session_service.create_session(
                app_name=app_name, user_id=user_id
            )
        except Exception:
            session = await runner.session_service.create_session(
                app_name=app_name, user_id=user_id
            )

    content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_message)],
    )

    attempts = max(1, len(getattr(runner, "_codex_api_key_pool", [1])))
    last_error = None

    for attempt in range(attempts):
        try:
            final_response = ""
            async for event in runner.run_async(
                user_id=user_id, session_id=session.id, new_message=content
            ):
                if hasattr(event, "content") and event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            final_response += part.text
            return final_response, session
        except Exception as exc:
            last_error = exc
            if attempt == attempts - 1 or not is_gemini_quota_error(exc):
                raise

            next_key = rotate_gemini_key()
            if not next_key:
                raise

            rebuild = getattr(runner, "_codex_rebuild", None) or getattr(agent, "_codex_rebuild", None)
            if rebuild is not None:
                new_agent, new_runner = rebuild()
                if hasattr(agent, "__dict__") and hasattr(new_agent, "__dict__"):
                    agent.__dict__.clear()
                    agent.__dict__.update(new_agent.__dict__)
                if hasattr(runner, "__dict__") and hasattr(new_runner, "__dict__"):
                    runner.__dict__.clear()
                    runner.__dict__.update(new_runner.__dict__)

            session = await runner.session_service.create_session(
                app_name=runner.app_name, user_id=user_id
            )

    raise last_error
