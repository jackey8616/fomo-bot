from discord import Locale, app_commands

translate_dictionary = {
    "casual_summarize_description": {
        Locale.american_english.value: "Casually summarizes the messages from tracking users in a casual format",
        Locale.taiwan_chinese.value: "粗略總結追蹤用戶的訊息",
    },
    "casual_summarize_describe_channel": {
        Locale.american_english.value: "The channel to summarize messages from. If not provided, uses the current channel.",
        Locale.taiwan_chinese.value: "要總結訊息的頻道。如果未提供，則使用當前頻道。",
    },
    "serious_summarize_description": {
        Locale.american_english.value: "Detailedly summarizes the messages from tracking users in a detailed format",
        Locale.taiwan_chinese.value: "詳細總結追蹤用戶的訊息",
    },
    "serious_summarize_describe_channel": {
        Locale.american_english.value: "The channel to summarize messages from. If not provided, uses the current channel.",
        Locale.taiwan_chinese.value: "要總結訊息的頻道。如果未提供，則使用當前頻道。",
    },
    "missing_channel": {
        Locale.american_english.value: "Could not determine the channel to summarize.",
        Locale.taiwan_chinese.value: "無法確定要總結訊息的頻道。",
    },
    "empty_messages": {
        Locale.american_english.value: "No tracking user messages found in channel {channel_url}!",
        Locale.taiwan_chinese.value: "在頻道 {channel_url} 中找不到任何追蹤用戶訊息！",
    },
}


class Translator(app_commands.Translator):
    async def translate(
        self,
        string: app_commands.locale_str,
        locale: Locale,
        context: app_commands.TranslationContext,
    ) -> str:
        return translate_dictionary.get(string.message, {}).get(
            locale.value, string.message
        )
