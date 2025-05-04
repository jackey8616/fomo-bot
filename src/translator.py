from discord import Locale, app_commands


class Translator(app_commands.Translator):
    async def translate(
        self,
        string: app_commands.locale_str,
        locale: Locale,
        context: app_commands.TranslationContext,
    ):
        translations = {
            "casual_summarize_description": {
                "en-US": "Summarizes the messages from whitelisted users in a casual format",
                "zh-TW": "總結白名單用戶的訊息",
            },
            "casual_summarize_describe_channel": {
                "en-US": "The channel to summarize messages from. If not provided, uses the current channel.",
                "zh-TW": "要總結訊息的頻道。如果未提供，則使用當前頻道。",
            },
            "serious_summarize_description": {
                "en-US": "Summarizes the messages from whitelisted users in a detailed format",
                "zh-TW": "總結白名單用戶的訊息",
            },
            "serious_summarize_describe_channel": {
                "en-US": "The channel to summarize messages from. If not provided, uses the current channel.",
                "zh-TW": "要總結訊息的頻道。如果未提供，則使用當前頻道。",
            },
        }
        return translations.get(string.message, {}).get(locale.value, string.message)
