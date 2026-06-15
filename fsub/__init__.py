import sys
import uvloop
import asyncio
from hydrogram import Client
from fsub.config import (
    CHANNEL_DB,
    LOGGER,
    BOT_TOKEN,
)
from fsub.force import get_all_fsubs
from fsub.credit import ensure_credit_integrity

uvloop.install()


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_id=2040,
            api_hash="b18441a1ff607e10a989891a5462e627",
            plugins={"root": "plugins"},
            bot_token=BOT_TOKEN,
            in_memory=True,
        )
        self.LOGGER = LOGGER


    async def refresh_fsub_invite_links(self, exit_on_error: bool = False):
        for key, channel_id in get_all_fsubs().items():
            try:
                info = await self.get_chat(channel_id)
                link = info.invite_link
                if not link:
                    link = await self.export_chat_invite_link(channel_id)
                setattr(self, f"invitelink{key}", link)
                self.LOGGER(__name__).info(
                    f"FORCE_SUB_{key} Detected!\n"
                    f"  Title: {info.title}\n"
                    f"  Chat ID: {info.id}\n\n"
                )
            except Exception as e:
                self.LOGGER(__name__).error(e)
                self.LOGGER(__name__).error(
                    f"Pastikan @{self.username} menjadi Admin di FORCE_SUB_{key} ({channel_id})\n\n"
                )
                if exit_on_error:
                    sys.exit()
                raise

    async def start(self):
        ensure_credit_integrity()
        try:
            await super().start()
            is_bot = await self.get_me()
            self.username = is_bot.username
            self.namebot = is_bot.first_name
            self.LOGGER(__name__).info(
                f"BOT_TOKEN detected!\n"
                f"  Username: @{self.username}\n\n"
            )
        except Exception as e:
            self.LOGGER(__name__).error(e)
            sys.exit()

        await self.refresh_fsub_invite_links(exit_on_error=True)

        try:
            db_channel = await self.get_chat(CHANNEL_DB)
            self.db_channel = db_channel
            await self.send_message(chat_id=db_channel.id, text="Bot Aktif!\n\n")
            self.LOGGER(__name__).info(
                "CHANNEL_DB Detected!\n"
                f"  Title: {db_channel.title}\n"
                f"  Chat ID: {db_channel.id}\n\n"
            )
        except Exception as e:
            self.LOGGER(__name__).error(e)
            self.LOGGER(__name__).error(
                f"Pastikan @{self.username} menjadi Admin di CHANNEL_DB\n\n"
            )
            sys.exit()

        self.LOGGER(__name__).info("Bot Aktif!\n\n")

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot Berhenti!\n\n")


if __name__ == "__main__":
    try:
        asyncio.set_event_loop(asyncio.new_event_loop())
    except Exception:
        pass
    Bot().run()
