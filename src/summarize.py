from discord import Message


def casual_summarize(messages: list[Message]) -> tuple[list[str], str]:
    system_instructions = [
        "You are a helpful assistant that summarizes messages.",
        "You are given a list of messages wrap in <messages> tags.",
        "You need to summarize the messages into a short summary with same language as the messages.",
    ]
    user_instructions = ["<messages>"]
    for message in messages:
        user_instructions.append(f"{message.author.name}: {message.content}")
    user_instructions.append("</messages>")
    return (system_instructions, "\n".join(user_instructions))


def serious_summarize(messages: list[Message]) -> tuple[list[str], str]:
    raw_messages = ""
    for message in messages:
        raw_messages += f"[{message.created_at}] {message.author}: {message.content}\n"

    system_instructions = [
        "You are an expert summarizer of casual Discord chat logs from a software side project community."
        "Your goal is to provide concise summaries that capture the key learnings, shared resources, quick help instances, and any projects or progress mentioned in the chat.",
        "The chat log will be provided in the <chat_log> tags.",
        "",
        "**Context:** This is a coding-lab channel of a side project community, people shares things more than coding and with their casual live",
        "",
        "**Summary Instructions:**",
        "Based on the chat log above, please create a summary that adheres to the following guidelines:",
        "* **Output have to be in the same language as the chat log(like Traditional Chinese).**",
        "* **Identify any key learnings or insights shared.**",
        "* **Note any resources, tools, or links that were shared.**",
        "* **Capture instances where someone asked for and received quick help or advice.**",
        "* **Summarize any progress updates or discussions around specific side projects.**",
        "* **Keep the summary concise and easy to understand (aim for [desired length, e.g., 3-5 bullet points or a short paragraph]).**",
        "* **Focus on the valuable information exchanged and any ongoing projects.**",
        "* **Maintain a neutral and informative tone, acknowledging the casual nature of the conversation.**",
        "* **Links have to wrap in correct markdown format.**"
        "",
        "**Example Summary Output Format (Optional but helpful):**",
        "",
        "**Key Learnings/Insights:**",
        "* [Learning point 1]",
        "* [Learning point 2]",
        "* ...",
        "",
        "**Shared Resources:**",
        "* [Link to resource 1] - Briefly described",
        "* [Tool/Library mentioned] - Context of its use",
        "* ...",
        "",
        "**Quick Help/Advice:**",
        "* [User A] got help with [problem] from [User B] - [Brief solution]",
        "* [Question asked] and [Answer given]",
        "* ...",
        "",
        "**Project Updates/Discussions:**",
        "* [User C] shared progress on their [project name] - [Brief update]",
        "* Discussion around [project idea]",
        "* ...",
        "",
    ]
    user_prompt = f"<chat_log>\n{raw_messages}\n</chat_log>"
    return (system_instructions, user_prompt)
