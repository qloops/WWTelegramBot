from pyrogram import filters


def create_forwarded_from_filter(user_id: int):
    async def func(_, __, query):
        return query.forward_from and query.forward_from.id == user_id
    return filters.create(func)