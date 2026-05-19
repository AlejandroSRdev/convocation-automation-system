_SYSTEM_PROMPT = """You are a text refinement assistant for sports convocation messages.

Your task is to improve the readability, wording, or formatting of the provided convocation message.

You MUST:
- Preserve every player name and number exactly as written
- Preserve every URL exactly as written
- Preserve all schedule information (date, time, location) exactly as written
- Preserve WhatsApp formatting syntax (* for bold, _ for italic)
- Preserve all emojis
- Return ONLY the refined message text. No commentary, no explanations, no preamble.

You MUST NOT:
- Remove or alter any player name, number, or position
- Remove or modify any URL
- Remove or modify any date, time, or location
- Add information not present in the original
- Change the operational structure of the message"""


def build_initial_prompt(message: str, style: str | None) -> tuple[str, str]:
    user_prompt = (
        f"Refine the following convocation message.\n"
        f"Style instruction: {style if style else 'improve readability and clarity'}.\n\n"
        f"Message:\n{message}"
    )
    return _SYSTEM_PROMPT, user_prompt


def build_retry_prompt(
    message: str, style: str | None, missing_fragments: list[str]
) -> tuple[str, str]:
    fragments_block = "\n".join(f"- {f}" for f in missing_fragments)
    user_prompt = (
        f"Your previous refinement failed operational validation.\n\n"
        f"The following required fragments were missing or altered in your response:\n"
        f"{fragments_block}\n\n"
        f"You MUST preserve ALL the above fragments exactly as they appear in the original message.\n"
        f"Do not modify, rephrase, or remove them under any circumstances.\n\n"
        f"Refine the following convocation message again.\n"
        f"Style instruction: {style if style else 'improve readability and clarity'}.\n\n"
        f"Message:\n{message}"
    )
    return _SYSTEM_PROMPT, user_prompt
