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

@Bot.on_message(filters.command("listadmin") & filters.private & owner_filter)
async def list_admin_command(client: Bot, message: Message):
    from fsub.func import get_all_admin_ids

    admin_ids = get_all_admin_ids()
    if not admin_ids:
        return await message.reply("Belum ada Owner/Admin yang terdaftar.")

    lines = ["**Daftar Owner/Admin:**"]
    for index, user_id in enumerate(admin_ids, start=1):
        role = "Owner" if is_owner_id(user_id) else "Admin"
        lines.append(f"{index}. `{user_id}` - {role}")
    await message.reply("\n".join(lines))


@Bot.on_message(filters.command("addsub") & filters.private & owner_filter)
async def add_sub_command(client: Bot, message: Message):
    from fsub.config import FORCE_SUB_
    from fsub.database import add_dynamic_fsub, check_dynamic_fsub

    if len(message.command) < 2:
        return await message.reply("Gunakan format: /addsub -100xxxxxxxxxx")

    try:
        chat_id = int(message.command[1])
    except ValueError:
        return await message.reply("ID channel tidak valid. Harap masukkan angka, contoh: /addsub -1001234567890")

    if chat_id in FORCE_SUB_.values() or check_dynamic_fsub(chat_id):
        return await message.reply("Channel tersebut sudah ada di daftar force subscribe.")

    try:
        await client.get_chat(chat_id)
        add_dynamic_fsub(chat_id)
        await client.refresh_fsub_invite_links()
    except Exception as e:
        from fsub.database import del_dynamic_fsub

        del_dynamic_fsub(chat_id)
        return await message.reply(
            f"Gagal menambahkan channel `{chat_id}`. Pastikan bot sudah menjadi admin dan bisa membuat invite link.\n\nError: {e}"
        )

    await message.reply(f"✅ Channel `{chat_id}` berhasil ditambahkan ke force subscribe tambahan.")


@Bot.on_message(filters.command("delsub") & filters.private & owner_filter)
async def del_sub_command(client: Bot, message: Message):
    from fsub.config import FORCE_SUB_
    from fsub.database import del_dynamic_fsub

    if len(message.command) < 2:
        return await message.reply("Gunakan format: /delsub -100xxxxxxxxxx")

    try:
        chat_id = int(message.command[1])
    except ValueError:
        return await message.reply("ID channel tidak valid. Harap masukkan angka, contoh: /delsub -1001234567890")

    if chat_id in FORCE_SUB_.values():
        return await message.reply("Force subscribe wajib dari config.env tidak bisa dihapus lewat perintah. Hapus dari config.env jika ingin mengubahnya.")

    if del_dynamic_fsub(chat_id):
        await client.refresh_fsub_invite_links()
        return await message.reply(f"✅ Channel `{chat_id}` berhasil dihapus dari force subscribe tambahan.")

    await message.reply("Channel tersebut tidak ada di daftar force subscribe tambahan.")


@Bot.on_message(filters.command("listsub") & filters.private & owner_filter)
async def list_sub_command(client: Bot, message: Message):
    from fsub.config import FORCE_SUB_
    from fsub.database import full_dynamic_fsub
    from fsub.force import get_all_fsubs

    all_fsubs = get_all_fsubs()
    if not all_fsubs:
        return await message.reply("Belum ada force subscribe yang terdaftar.")

    static_values = set(FORCE_SUB_.values())
    dynamic_values = set(full_dynamic_fsub())
    lines = ["**Daftar Force Subscribe:**"]
    for index, chat_id in all_fsubs.items():
        source = "Wajib config.env" if chat_id in static_values else "Tambahan database"
        lines.append(f"{index}. `{chat_id}` - {source}")

    if len(message.command) > 1:
        try:
            requested_id = int(message.command[1])
        except ValueError:
            return await message.reply("ID channel tidak valid. Harap masukkan angka.")
        status = "terdaftar" if requested_id in static_values or requested_id in dynamic_values else "tidak terdaftar"
        lines.append(f"\nChannel `{requested_id}`: **{status}**")

    await message.reply("\n".join(lines))


@Bot.on_message(filters.command("setforce") & filters.private & owner_filter)
async def set_force_message_command(client: Bot, message: Message):
    from fsub.database import set_setting
    from fsub.force import SETTING_FORCE_MESSAGE

    text = message.text.split(None, 1)[1] if len(message.command) > 1 else None
    if not text and message.reply_to_message and message.reply_to_message.text:
        text = message.reply_to_message.text
    if not text:
        return await message.reply(
            "Gunakan format: /setforce pesan force subscribe\n"
            "Placeholder yang didukung: {first}, {last}, {username}, {mention}, {id}"
        )
    set_setting(SETTING_FORCE_MESSAGE, text)
    await message.reply("✅ FORCE_MESSAGE berhasil diperbarui. Watermark credit tetap otomatis ditambahkan.")


@Bot.on_message(filters.command("setjoin") & filters.private & owner_filter)
async def set_join_button_command(client: Bot, message: Message):
    from fsub.database import set_setting
    from fsub.force import SETTING_JOIN_BUTTON

    text = message.text.split(None, 1)[1] if len(message.command) > 1 else None
    if not text:
        return await message.reply("Gunakan format: /setjoin teks tombol join")
    set_setting(SETTING_JOIN_BUTTON, text)
    await message.reply(f"✅ Teks tombol join berhasil diperbarui menjadi: {text}")
