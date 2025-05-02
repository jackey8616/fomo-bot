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
        "* **Links have to wrap in correct markdown format.**",
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


def serious_summarize_with_link(messages: list[Message]) -> tuple[list[str], str]:
    system_instructions = [
        "You are an expert summarizer of casual Discord chat logs from a software side project community."
        "Your goal is to provide concise summaries that capture the key learnings, shared resources, quick help instances, and any projects or progress mentioned in the chat, with each summary point linking back to the relevant message."
        "",
        "**Input Chat Log Format:**"
        "The chat log will be provided within the <chat_log> tags. Each message in the log will include the `time`, `author`, `content`, and a `jump_url` which links directly to that message on Discord."
        "",
        "**Context:** This is a coding-lab channel of a side project community. Conversations are often casual and may mix technical topics with daily life."
        "",
        "**Summary Instructions:**"
        "Based on the chat log provided above, please create a summary that adheres to the following guidelines:",
        "*   **Output Language:** The *entire* summary, including headings and bullet points, **must** be in the **same language** as the original chat log content (e.g., Traditional Chinese if the chat is in Traditional Chinese).",
        "*   **Identify Key Information:** Extract key learnings/insights, shared resources, instances of help/advice, and project updates/discussions.",
        "*   **Bullet Point Format with Navigation:**",
        "    *   Present the summary using bullet points under relevant categories (see example format below).",
        "    *   **Crucially, each bullet point *must* link back to the relevant message in the chat log.** Use the `jump_url` from the input data for this.",
        "    *   Format each bullet point as: `* [Concise summary of the point][Ref](relevant_jump_url)`.",
        "    *   Select the `jump_url` corresponding to the message that *best represents the start or the core* of the summarized topic (e.g., the message sharing the link, asking the question, or starting the project discussion).",
        "*   **Conciseness:** Keep the summary brief and easy to digest (aim for a few key bullet points per category as relevant).",
        "*   **Focus:** Prioritize valuable information exchange and project-related activity.",
        "*   **Tone:** Maintain a neutral, informative tone, reflecting the casual nature of the chat.",
        "*   **Link Handling:** Ensure all `jump_url` links used for navigation are correctly formatted in Markdown. Any *other* links shared in the content should also be formatted correctly.",
        "",
        "**Example Summary Output Format (Adapt headings to the chat log's language):**",
        "",
        "**重點學習/見解 (Key Learnings/Insights):**",
        "*   關於某個概念的學習點[Ref](URL_to_message1)",
        "*   分享的另一個見解[Ref](URL_to_message2)",
        "",
        "**分享的資源 (Shared Resources):**",
        "*   某個工具的連結[Ref](URL_to_message3) - 簡短描述",
        "*   提到的函式庫[Ref](URL_to_message4) - 使用情境",
        "",
        "**快速協助/建議 (Quick Help/Advice):**",
        "*   用戶A 在 問題 上獲得 用戶B 的幫助 - 簡要解決方案[Ref](URL_to_message5)",
        "*   提出的問題 得到 回答[Ref](URL_to_message6)",
        "",
        "**專案更新/討論 (Project Updates/Discussions):**",
        "*   用戶C 分享了 專案名稱 的進度 - 簡要更新[Ref](URL_to_message7)",
        "*   關於 專案想法 的討論 [Ref](URL_to_message8)",
        "",
        "**閒聊/八卦 (Casual Chat/Gossip):**",
        "*   用戶D 分享了週末計畫[Ref](URL_to_message9)",
        "*   關於 [某個非技術話題] 的輕鬆討論[Ref](URL_to_message10)",
        "*   社群成員互相問候或開玩笑[Ref](URL_to_message11)",
        "",
    ]
    raw_messages = ""
    for message in messages:
        raw_messages += f"[{message.created_at}] {message.author}: {message.content} (link_to:{message.id})\n"
    user_prompt = f"<chat_log>\n{raw_messages}\n</chat_log>"
    return (system_instructions, user_prompt)
