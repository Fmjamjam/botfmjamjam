import pandas as pd
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import asyncio

# Konfigurasi logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Fungsi untuk memulai bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Received /start command")
    await update.message.reply_text('Halo! Kirim file Excel Anda dan saya akan membandingkan datanya.')

# Fungsi untuk menangani file Excel yang dikirim
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Received file")
    document = update.message.document
    if document:
        file = await document.get_file()
        if file:
            logging.info("File downloaded")
            await file.download_to_drive('data.xlsx')

            # Baca file Excel
            df = pd.read_excel('data.xlsx')

            # Buat kolom Keterangan
            df['Keterangan'] = ''

            # Logika perbandingan data
            df['Keterangan'] = df.apply(lambda row: keterangan(row), axis=1)

            # Simpan hasil ke file baru
            df.to_excel('hasil.xlsx', index=False)

            # Kirim kembali file hasil
            await context.bot.send_document(chat_id=update.message.chat_id, document=open('hasil.xlsx', 'rb'))
        else:
            logging.warning("Failed to download file")
            await update.message.reply_text('Terjadi kesalahan dalam mengunduh file. Silakan coba lagi.')
    else:
        logging.warning("No document received")
        await update.message.reply_text('Tidak ada file yang terdeteksi. Silakan kirim file Excel Anda.')

def keterangan(row):
    # Implementasikan logika penambahan/kenaikan/penurunan anggota/outstanding di sini
    if row['Total Balance'] > 0:
        return 'Outstanding naik'
    elif row['Total Balance'] < 0:
        return 'Outstanding turun'
    else:
        return ''

async def main():
    # Token bot Telegram Anda
    token = '8134228080:AAFlVhjfNFvurDGtig_5qFoxj_O6KCBnzZA'

    # Buat aplikasi
    application = Application.builder().token(token).build()

    # Daftarkan handler
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.Document.MimeType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"), handle_file))

    # Inisialisasi dan jalankan bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
