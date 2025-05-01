from discord import User


def summarize(messages: list[tuple[User, str]]) -> tuple[list[str], str]:
    system_instructions = [
        "You are a helpful assistant that summarizes messages.",
        "You are given a list of messages wrap in <messages> tags.",
        "You need to summarize the messages into a short summary with same language as the messages.",
    ]
    user_instructions = ["<messages>"]
    for message in messages:
        user_instructions.append(f"{message}")
    user_instructions.append("</messages>")
    return (system_instructions, "\n".join(user_instructions))
