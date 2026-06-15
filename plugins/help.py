from fsub import Bot
# --- PERUBAHAN: Import tambahan ---
from fsub.config import ADMINS
from fsub.database import get_talent
from fsub.func import is_admin_id
from hydrogram import filters
# -----------------------------------
from hydrogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from hydrogram.types import InlineKeyboardButton


class Data:
    # --- PERUBAHAN: Membagi pesan Bantuan ---
    
    HELP_MEMBER = """
/start: Mulai bot
/help: Bantuan dan tentang bot
/idku: Lihat User ID Telegram Anda
/ping: Cek latensi bot
/uptime: Cek waktu aktif bot
/mycoins: Cek saldo koin Anda
/rate (id_talent): Beri 1 🍓 ke talent (Biaya: 10 🪙)
/talent: Lihat daftar talent
/toptalent: Lihat papan peringkat talent
"""

    HELP_TALENT_ONLY = """
**Perintah Talent:**
/setbio (bio): Atur bio profil Anda
/setvip (chat_id): Atur channel VIP Anda
/delvip: Hapus channel VIP Anda
"""

    HELP_ADMIN_ONLY = """
**Perintah Admin:**
/users: Statistik pengguna bot
/batch: Multi post dalam satu link
/broadcast: Pesan siaran ke pengguna bot
/addtalent (id): Tambah talent
/deltalent (id): Hapus talent
/tfcoin (id) (jml): Transfer koin ke user
/revokevip (id_talent) (id_user): Cabut akses VIP member
/addadmin (id): Owner menambahkan admin database
/unadmin (id): Owner menurunkan admin database
/listadmin: Lihat daftar admin database
/addsub (chat_id): Tambah channel/group force subscribe
/delsub (chat_id): Hapus channel/group force subscribe
/listsub: Lihat daftar force subscribe
/setforce (teks): Ubah pesan force subscribe
/setjoin (teks): Ubah teks tombol join
/gitpull: Owner menerapkan perubahan terbaru dari repo
"""
    # ----------------------------------------

    close = [
        [InlineKeyboardButton("Tutup", callback_data="close")]
    ]

    mbuttons = [
        [
            InlineKeyboardButton("Bantuan", callback_data="help"),
            InlineKeyboardButton("Tutup", callback_data="close")
        ],
    ]

    buttons = [
        [
            InlineKeyboardButton("Tentang", callback_data="about"),
            InlineKeyboardButton("Tutup", callback_data="close")
        ],
    ]

    admin_buttons = [
        [InlineKeyboardButton("Git Pull", callback_data="gitpull")],
        [
            InlineKeyboardButton("Tentang", callback_data="about"),
            InlineKeyboardButton("Tutup", callback_data="close")
        ],
    ]

    ABOUT = """
@{} adalah Bot untuk menyimpan postingan atau file yang dapat diakses melalui link khusus.

  Framework: <a href='https://docs.hydrogram.org'>hydrogram</a>
  Developer: <a href='https://t.me/MasterHereXD'>Master</a>
"""


def build_help_text(user_id: int) -> str:
    is_admin = is_admin_id(user_id)
    is_talent = get_talent(user_id)

    if is_admin:
        role_header = "🛠️ **Menu Bantuan Admin** 🛠️"
        help_text = Data.HELP_MEMBER + "\n" + Data.HELP_TALENT_ONLY + "\n" + Data.HELP_ADMIN_ONLY
    elif is_talent:
        role_header = "⭐️ **Menu Bantuan Talent** ⭐️"
        help_text = Data.HELP_MEMBER + "\n" + Data.HELP_TALENT_ONLY
    else:
        role_header = "👤 **Menu Bantuan Member** 👤"
        help_text = Data.HELP_MEMBER

    return f"{role_header}\n{help_text}"


@Bot.on_message(filters.private & filters.incoming & filters.command("help"))
async def help(client: Bot, message: Message):
    text = build_help_text(message.from_user.id)

    await client.send_message(
        message.chat.id, 
        text,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(Data.admin_buttons if is_admin_id(message.from_user.id) else Data.buttons),
    )


# --- PERUBAHAN: Logika dinamis untuk tombol callback "Bantuan" ---
@Bot.on_callback_query()
async def handler(client: Bot, query: CallbackQuery):
    data = query.data
    
    if data == "about":
        try:
            await query.message.edit_text(
                text=Data.ABOUT.format(client.username),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(Data.mbuttons),
            )
        except Exception:
            pass
            
    elif data == "help":
        text = build_help_text(query.from_user.id)

        try:
            await query.message.edit_text(
                text=text,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(Data.admin_buttons if is_admin_id(query.from_user.id) else Data.buttons),
            )
        except Exception:
            pass

    elif data == "gitpull":
        from fsub.func import is_owner_id
        from plugins.admin import format_git_pull_result, run_git_pull

        if not is_owner_id(query.from_user.id):
            return await query.answer("Hanya owner yang dapat menjalankan git pull.", show_alert=True)

        await query.answer("Menjalankan git pull...")
        status_message = await query.message.reply("Menjalankan `git pull --ff-only`...")
        returncode, output = await run_git_pull()
        await status_message.edit_text(format_git_pull_result(returncode, output))
            
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except Exception:
            pass
