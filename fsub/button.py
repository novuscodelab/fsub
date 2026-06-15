from fsub.config import BUTTON_ROW
from fsub.force import get_all_fsubs, get_join_button_title

from hydrogram.types import InlineKeyboardButton


async def start_button(client):
    all_fsubs = get_all_fsubs()
    if not all_fsubs:
        buttons = [
            [
                InlineKeyboardButton(text="Bantuan", callback_data="help"),
                InlineKeyboardButton(text="Tutup", callback_data="close"),
            ],
        ]
        return buttons

    dynamic_button = []
    current_row = []
    for key in all_fsubs.keys():
        current_row.append(InlineKeyboardButton(text=f"{get_join_button_title()} {key}", url=getattr(client, f'invitelink{key}')))
        if len(current_row) == BUTTON_ROW:
            dynamic_button.append(current_row)
            current_row = []

    if current_row:
        dynamic_button.append(current_row)

    buttons = [
        [
            InlineKeyboardButton(text="Bantuan", callback_data="help"),
        ],
    ] + dynamic_button + [
        [InlineKeyboardButton(text="Tutup", callback_data="close")],
    ]
    return buttons


async def fsub_button(client, message):
    all_fsubs = get_all_fsubs()
    if all_fsubs:
        dynamic_button = []
        current_row = []
        for key in all_fsubs.keys():
            current_row.append(InlineKeyboardButton(text=f"{get_join_button_title()} {key}", url=getattr(client, f'invitelink{key}')))
            if len(current_row) == BUTTON_ROW:
                dynamic_button.append(current_row)
                current_row = []

        if current_row:
            dynamic_button.append(current_row)
            
        try:
            dynamic_button.append([
                InlineKeyboardButton(
                    text="ᴄᴏʙᴀ ʟᴀɢɪ",
                    url=f"https://t.me/{client.username}?start={message.command[1]}",
                )
            ])
        except IndexError:
            pass

        return dynamic_button
