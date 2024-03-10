"""
alias
"""

import aiohttp


async def get_alias_by_id(song_id: int) -> str:
    """
    get_alias_by_id

    Args:
        song_id (int): song_id

    Returns:
        str: alias
    """
    url = "https://maimai.lxns.net/api/v0/maimai/alias/list"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:

            if resp.status != 200:
                return
            data = await resp.json()

            aliases = data.get("aliases")
            for i in aliases:
                if i.get("song_id") == song_id:
                    return "\n".join(i.get("aliases"))
