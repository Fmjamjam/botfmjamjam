import sqlite3
import random
import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Fungsi untuk mendapatkan koneksi database
def get_db_connection():
    return sqlite3.connect("chatbot.db", check_same_thread=False)

# Buat tabel jika belum ada
db = get_db_connection()
cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE,
    message TEXT,
    group_id TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS ksbcabang (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    group_id TEXT
)
""")
db.commit()

# Periksa dan tambahkan kolom 'date' jika belum ada
cursor.execute("PRAGMA table_info(ksbcabang)")
columns = [col[1] for col in cursor.fetchall()]
if "date" not in columns:
    cursor.execute("ALTER TABLE ksbcabang ADD COLUMN date TEXT")
    db.commit()

db.close()

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Halo! Saya jamBOT , Kirimi saya uang.')

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Berikut perintah yang tersedia:\n/start - Mulai bot\n/help - Bantuan\nGunakan:\n#req <pesan> - Menyimpan permintaan\n#sudah <kode> - Menandai permintaan sudah diproses\n#cekreq - Mengecek permintaan yang belum diproses\n#ksbcabang - Mencatat laporan KSB\n#cekksb - Mengecek laporan KSB harian.\n/siapa yang cakep?')

async def siapa(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('mamang ini nih @jamjamfirman cakep')

async def handle_message(update: Update, context: CallbackContext) -> None:
    message = update.message
    text = message.text.strip()
    chat_id = message.chat_id  # Dapatkan ID chat
    today = datetime.date.today().strftime("%Y-%m-%d")  # Format tanggal harian
    
    db = get_db_connection()
    cursor = db.cursor()
    
    # Hapus data #ksbcabang dari hari sebelumnya
    cursor.execute("DELETE FROM ksbcabang WHERE date < ?", (today,))
    db.commit()
    
    if text.startswith("#req"):
        request_text = text[5:].strip()
        code = str(random.randint(10000, 99999))  # Kode unik 5 digit
        cursor.execute("INSERT INTO requests (code, message, group_id) VALUES (?, ?, ?)", (code, request_text, str(chat_id)))
        db.commit()
        await message.reply_text(f"Pesan disimpan dengan kode: {code}")
        
    elif text.startswith("#sudah"):
        parts = text.split()
        if len(parts) > 1:
            code = parts[1]
            cursor.execute("SELECT group_id FROM requests WHERE code = ?", (code,))
            result = cursor.fetchone()
            if result:
                group_id = result[0]
                cursor.execute("DELETE FROM requests WHERE code = ?", (code,))
                db.commit()
                await message.reply_text("Oke sudah diproses ya.")
            else:
                await message.reply_text("Kode tidak ditemukan.")
        else:
            await message.reply_text("Format salah. Gunakan #sudah <kode>.")
    
    elif text.startswith("#cekreq"):
        cursor.execute("SELECT code FROM requests")
        requests = cursor.fetchall()
        if requests:
            response = "Berikut permintaan yang belum diproses:\n"
            for code in requests:
                response += f"Bro @jamjamfirman ini belum diroses ({code[0]})\n"
            await message.reply_text(response)
        else:
            await message.reply_text("Semua permintaan sudah diproses.")
    
    elif text.startswith("#ksbcabang"):
        lines = text.split("\n")
        if len(lines) >= 4:
            ksb_text = f"{lines[2].strip()}\n{lines[3].strip()}"  # Ambil baris ke-3 dan ke-4
            cursor.execute("INSERT INTO ksbcabang (message, group_id, date) VALUES (?, ?, ?)", (ksb_text, str(chat_id), today))
            db.commit()
            await message.reply_text("KSB sudah dicatat, terima kasih.")
        else:
            await message.reply_text("Format pesan tidak valid. Pastikan ada minimal 4 baris.")
    
    elif text.startswith("#cekksb"):
        cursor.execute("SELECT DISTINCT message FROM ksbcabang WHERE date = ?", (today,))
        reported_branches = [row[0] for row in cursor.fetchall()]
        
        all_branches = ["ini masih percobaan", "Cabang B", "Cabang C", "Cabang D"]  # Daftar semua cabang (bisa diganti sesuai kebutuhan)
        unreported_branches = [branch for branch in all_branches if branch not in reported_branches]
        
        if reported_branches:
            response = "Yang sudah laporan KSB:\n" + "\n".join(f"- {branch}" for branch in reported_branches)
            response += "\n__________________________\nYang belum KSB melakukan #ksbcabang:\n"
            response += "\n".join(f"@{branch.lower().replace(' ', '_')}" for branch in unreported_branches)  # Mention anggota
        else:
            response = "Belum ada cabang yang melaporkan KSB hari ini."
        
        await message.reply_text(response)
    
    db.close()

def main():
    TOKEN = "7750914821:AAGMZAffji-fEadwzZwHP-ldAEGVUXZP53E"  # Ganti dengan token dari BotFather
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("siapa", siapa))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()