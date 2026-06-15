from fsub import Bot
from fsub.config import ADMINS
from fsub.database import add_admin, check_admin, del_admin
from fsub.func import is_owner_id, owner_filter

from hydrogram import filters
from hydrogram.errors import PeerIdInvalid
from hydrogram.types import Message


@Bot.on_message(filters.command("addadmin") & filters.private & owner_filter)
async def add_admin_command(client: Bot, message: Message):
    if len(message.command) < 2:
        return await message.reply("Gunakan format: /addadmin (user_id)")

    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply("User ID tidak valid. Harap masukkan angka.")

    if is_owner_id(user_id):
        return await message.reply("User tersebut sudah menjadi Owner.")

    if user_id in ADMINS or check_admin(user_id):
        return await message.reply("User tersebut sudah menjadi Admin.")

    try:
        user = await client.get_users(user_id)
        if user.is_bot:
            return await message.reply("Bot tidak bisa dijadikan Admin.")
    except (PeerIdInvalid, ValueError):
        return await message.reply(f"User ID {user_id} tidak ditemukan.")
    except Exception as e:
        return await message.reply(f"Terjadi error saat mengambil data user: {e}")

    add_admin(user_id)
    await message.reply(
        f"✅ Sukses! **{user.first_name}** (`{user_id}`) telah ditambahkan sebagai Admin."
    )


@Bot.on_message(filters.command("unadmin") & filters.private & owner_filter)
async def unadmin_command(client: Bot, message: Message):
    if len(message.command) < 2:
        return await message.reply("Gunakan format: /unadmin (user_id)")

    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply("User ID tidak valid. Harap masukkan angka.")

    if is_owner_id(user_id):
        return await message.reply("Owner tidak bisa diturunkan dengan /unadmin.")

    if user_id in ADMINS:
        return await message.reply("Admin dari config.env tidak bisa diturunkan melalui database. Hapus dari ADMINS di config.env.")

    if del_admin(user_id):
        return await message.reply(f"✅ Sukses! User `{user_id}` telah diturunkan dari Admin.")

    await message.reply("User tersebut bukan Admin database.")
