from fsub.config import BUTTON_ROW
from fsub.force import get_all_fsubs, get_join_button_title

from hydrogram.types import InlineKeyboardButton


def get_invite_link(client, key):
    return getattr(client, f"invitelink{key}", None)


def build_join_buttons(client):
    dynamic_button = []
    current_row = []
    for key in get_all_fsubs().keys():
        link = get_invite_link(client, key)
        if not link:
            continue
        current_row.append(
            InlineKeyboardButton(text=f"{get_join_button_title()} {key}", url=link)
        )
        if len(current_row) == BUTTON_ROW:
            dynamic_button.append(current_row)
            current_row = []

    if current_row:
        dynamic_button.append(current_row)
    return dynamic_button


async def start_button(client):
    dynamic_button = build_join_buttons(client)
    buttons = [[InlineKeyboardButton(text="Bantuan", callback_data="help")]]
    buttons.extend(dynamic_button)
    buttons.append([InlineKeyboardButton(text="Tutup", callback_data="close")])
    return buttons


async def fsub_button(client, message):
    dynamic_button = build_join_buttons(client)
    try:
        start_arg = message.command[1]
    except (AttributeError, IndexError):
        start_arg = None

    if start_arg:
        dynamic_button.append(
            [
                InlineKeyboardButton(
                    text="ᴄᴏʙᴀ ʟᴀɢɪ",
                    url=f"https://t.me/{client.username}?start={start_arg}",
                )
            ]
        )

    return dynamic_button
