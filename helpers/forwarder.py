# (c) @AbirHasan2005

import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from helpers.filters import FilterMessage
from helpers.block_exts_handler import CheckBlockedExt


async def ForwardMessage(client: Client, msg: Message):
    try:
        ## --- Check 1 --- ##
        can_forward = await FilterMessage(message=msg)
        if can_forward == 400:
            return 400
        ## --- Check 2 --- ##
        has_blocked_ext = await CheckBlockedExt(event=msg)
        if has_blocked_ext is True:
            return 400
        ## --- Check 3 --- ##
        if Config.FORWARD_AS_COPY is True:
            await msg.copy(int(Config.FORWARD_TO_CHAT_ID))
        else:
            await msg.forward(int(Config.FORWARD_TO_CHAT_ID))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await client.send_message(chat_id="me", text=f"#FloodWait: Stopped Forwarder for `{e.x}s`!")
        await asyncio.sleep(Config.SLEEP_TIME)
        await ForwardMessage(client, msg)
    except Exception as err:
        await client.send_message(chat_id="me", text=f"#ERROR: `{err}`")
