import re
from abc import (
    ABC, 
    abstractmethod
)
from typing import List

from pyrogram import (
    Client, 
    filters
)
from pyrogram.types import (
    InlineQueryResultArticle, 
    InputTextMessageContent, 
    InlineQuery
)

import bot
import database
import rules


class InlineQueryHandler(ABC):
    def __init__(self, inline_query: InlineQuery):
        self.inline_query = inline_query
    
    @abstractmethod
    async def handle(self, attribute: str = None) -> None:
        pass
    
    def create_article(
            self, 
            title: str, 
            message_text: str
    ) -> InlineQueryResultArticle:
        return InlineQueryResultArticle(
            title=title,
            input_message_content=InputTextMessageContent(
                message_text=message_text
            )
        )
    
    async def answer(self, articles: List[InlineQueryResultArticle]) -> None:
        await self.inline_query.answer(results=articles, cache_time=1)


class ViewGroupsHandler(InlineQueryHandler):
    async def handle(self, attribute: str = None) -> None:
        condition = {}
        if attribute and isinstance(attribute, str):
            attribute = re.escape(attribute)
            condition = {"group_name": {"$regex": attribute, "$options": "i"}}
        groups = database.db_interface.users_groups.find_many(
            condition=condition
        )
        
        if not groups:
            articles = [
                self.create_article("Группы отсутствуют", "Группы отсутствуют.")
            ]
        else:
            articles = [
                self.create_article(
                    f"Открыть группу: {group.group_name}",
                    f"/open_group {group.group_name}"
                )
                for group in groups
            ]
        
        await self.answer(articles)


class CreateGroupHandler(InlineQueryHandler):
    async def handle(self, attribute: str = None) -> None:
        if not attribute:
            article = self.create_article(
                "Введите имя новой группы",
                "Введите имя новой группы."
            )
        else:
            article = self.create_article(
                f"Создать группу: {attribute}",
                f"/create_group {attribute}"
            )
        
        await self.answer([article])


HANDLERS = {
    "View": ViewGroupsHandler,
    "Create": CreateGroupHandler
}


@bot.bot.on_inline_query(
    filters.regex(r"Groups:\s(?P<command_type>.+):(\s(?P<attribute>.+))?") & 
    rules.is_user_admin
)
async def handle_groups_inline_query(client: Client, inline_query: InlineQuery):
    match = inline_query.matches[0]
    command_type = match.group("command_type")
    attribute = (
        match.group("attribute").strip() 
        if match.group("attribute") 
        else None
    )
    
    handler_class = HANDLERS.get(command_type)
    if handler_class:
        handler = handler_class(inline_query)
        await handler.handle(attribute)