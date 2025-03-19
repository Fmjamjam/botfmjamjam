from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio

async def delete_message_later(context: CallbackContext, chat_id: int, message_id: int, delay: int = 600):
    await asyncio.sleep(delay)
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print(f"Gagal menghapus pesan: {e}")

async def handle_messages(update: Update, context: CallbackContext):
    user_text = update.message.text.lower()
    chat_id = update.message.chat_id

    responses = {
        "#req": "Oke permintaan dicatat, wait.",
        "minta tolong": "Oke permintaan dicatat, wait.",
        "#email": "REGIONAL : regional_s@komida.co.id\n Pak Frans : franskomida@gmail.com\n HRD Regional S : hrdregionals@gmail.com\n MIS REG : fmjamjam@gmail.com\n KORCAB 1 (pak Dicky) : dickykomida@gmail.com\n KORCAB 2 (pak Ivan) : komidaivantegar@gmail.com\n KORCAB 3 (pak Asep) : josepkomida@gmail.com\n\n KANTOR PUSAT\n SEKRETARIAT : sekretariat@mitradhuafa.com\n DIREKTUR KOMIDA : sugengpriyono@mitradhuafa.com\n MANAGER OPERASIONAL : iwan06mitradhuafa@gmail.com\n Accounting : accounting@mitradhuafa.com\n AUDIT : audit@mitradhuafa.com\n FINANCE : finance@mitradhuafa.com\n HRD : hrd@mitradhuafa.com\n MIS : mis@mitradhuafa.com\n OPERASIONAL : operasional@mitradhuafa.com\n SPM : spm.reporting@mitradhuafa.com\n DIV UMUM : umum@mitradhuafa.com\n KOPKADA : sekretariatkopkada@gmail.com\n LEGAL : legal@mitradhuafa.com\n YAMIDA : yamidapusat@gmail.com",
        "#regional": " KANTOR REGIONAL S\n\n Alamat email : regional_s@komida.co.id (utama)\n regional.s.ntt@gmail.com (cadangan / rekap cetakan)\n\n ALAMAT : jln. Merpati RT 9 RW 6 kel.Oebesa, kec. kota Soe , Kab.TIMOR TENGAH SELATAN\n\n MAPS :<a href='https://maps.app.goo.gl/qRj6vYo33oW2V8zh6'>Cek MAPS</a>",
        "izin off dulu": "Kang Jamjam Offline dulu, mohon ditunggu ya teman-teman, sampai BOT ini membalas kembali brarti Sudah Online, Silahkan Req saja di grup",
        "izin pm": "Lebih enak di grup aja agar permasalahan kamu jika yang lain juga mengalami hal yang sama, jadi temen-temen yg lain alurnya mengetahui harus seperti apa, tapi boleh silahkan",
        "ijin pm": "Lebih enak di grup aja agar permasalahan kamu jika yang lain juga mengalami hal yang sama, jadi temen-temen yg lain alurnya mengetahui harus seperti apa, tapi boleh silahkan",
        "izin PM": "Lebih enak di grup aja agar permasalahan kamu jika yang lain juga mengalami hal yang sama, jadi temen-temen yg lain alurnya mengetahui harus seperti apa, tapi boleh silahkan",
        "ksb cabang": "Sipp, ksbmu dicatat, terimakasih kerja keras hari ini, selamat istirahat ya.",
        "KSB cabang": "Sipp, ksbmu dicatat, terimakasih kerja keras hari ini, selamat istirahat ya.",
        "KSB Cabang": "Sipp, ksbmu dicatat, terimakasih kerja keras hari ini, selamat istirahat ya.",
        "#tutormdis" : "1. tutorial setting mdis sistem di EDGE : <a href='https://t.me/c/2270432603/6/825'>Cek Pesan</a>.\n2. tutorial setting mdis sistem di INTERNET EXPLORER : <a href='https://t.me/c/2270432603/6/835'>Cek Pesan</a>.",
        "#formatreq": "FORMAT REQUEST : <a href='https://t.me/c/2270432603/3/331'>Cek Pesan</a>",
        "#infotf": "Studi kasus : <a href='https://t.me/c/2270432603/6/297'>Cek Pesan</a> \n Persamaan persepsi TF : <a href='https://t.me/c/2270432603/6/625'> Cek Pesan</a> ",
        "#inputinfo": "input informasi Cabang : <a href='https://forms.gle/3zYQ7XM8SLokHzkz57'>Input disini</a> ",
        "#ende1": "Nama Cabang : ENDE 1 (Wolowaru)\n Kode Cab : 339\n Email : komidaende1@gmail.com\n Alamat : CQC OKAMAGE, RT/RW: 012/005 DESA NAKAMBARA KEC WOLOWARU KAB ENDE\n Opening : 17/06/2024\n Manager : MELKI FREDRIK LAU, S. PD\n DESRIANA NINO \n Titik Koordinat : yahh ga diinput",
        "#soe": "Nama Cabang : SOE\n Kode Cab : 067\n Email : komidasoe@gmail.com\n Alamat :  Desa Kesetnana, Rt.007 Rw.004, Kecamatan Mollo Selatan, Kab.Timor Tengah Selatan\n Opening : 17/09/2013\n Manager : I NYOMAN AGUS SUARDANA\n STAF MSA : PRISILA OKTOVIANA TABATI \n Titik Koordinat : <a href='https://maps.app.goo.gl/ERLMu92hbqR7kn6o7'>Cek MAPS</a>",
        "#insana": "Nama Cabang : INSANA\n Kode Cab : 293\n Email : komidainsana@gmail.com\n Alamat :  JL. TIMOR RAYA, NESAM RT/RW 01/01 DESA MANUAIN A KEC. INSANA KAB. TIMOR TENGAH UTARA\n Opening : 09/09/2019\n Manager :GUIDO ISADORUS KASE\n STAF MSA : NATALIA BATSEBA LETUNA \n Titik Koordinat : Insana",
        "#kangae": "Nama Cabang : KANGAE\n Kode Cab : 309\n Email : komidakangae@gmail.com\n Alamat :  Jl. Nairoa, RT. 018 / RW. 008, Desa Watumilok, Kec. Kangae, Kab. Sikka - NTT \n Opening : 31/01/2020\n Manager : YOHANES TAUS\n STAF MSA : HENDRIKUS BANU \n Titik Koordinat : <a href='https://maps.app.goo.gl/cuu1D43uP56cdvuz7'>Cek MAPS</a>",
        "#nikiniki": "Nama Cabang : NIKI-NIKI\n Kode Cab : 076\n Email : komidanikiniki@gmail.com\n Alamat : JL TIMOR RAYA, RT/RW 015/005. KELURAHA. NIkI-NIKI, KECAMATAN,AMANUBAN TENGAH, KABUPATEN. TTS - NTT\n Opening : yahh ga diinput\n Manager : FRANSISKUS KORE\n STAF MSA : ICHE FLORIDA TAUNU \n Titik Koordinat : <a href='https://maps.app.goo.gl/HNcFjMcaMRKat29TA'>Cek MAPS</a>",
        "#atambua": "Nama Cabang : ATAMBUA\n Kode Cab : 190\n Email : komidaatambua0190@gmail.com\n Alamat :  Jl. Putri Sion No. 009, Rt/RW 017/002 Tulamalae Kec. Atambua Barat, Kab. Belu\n Opening : yahh ga diinput\n Manager : FEBRIANUS NULE\n STAF MSA : DEVITA NATALIA TALAN\n Titik Koordinat : <a href='https://maps.app.goo.gl/oLqyrZJmT13VwSoa7'>Cek MAPS</a>",
        "#malaka": "Nama Cabang : MALAKA\n Kode Cab : 278\n Email : komidamalaka@gmail.com\n Alamat : Desa Kamanasa, Dusun Sukabiwedik RT 001 / RW 001, Kec. Malaka Tengah, Kab. Malaka\n Opening : 24/09/2019\n Manager : JUNALDI M.F.TUALAKA\n STAF MSA : NATALI BUKIFAN \n Titik Koordinat : https://www.google.com/maps/@-9.5435184,124.9213713,13.25z?entry=ttu&g_ep=EgoyMDI1MDEyMi4wIKXMDSoASAFQAw%3D%3D",
        "#kefa": "Nama Cabang : kefamenanu\n Kode Cab : 068\n Email : komidakefamenanu@gmail.com\n Alamat :  Kantor Komida Cabang Kefamenanu Jl. sonbay ,Kelurahan Kefa Tengah, Kecamatan Kota Kefamenanu, Kabupaten Timor Tengah Utara Provinsi Nusa Tengara Timur\n Opening : 01/10/2013\n Manager : NOVERNUS SEMUEL BORU\n STAF MSA : MIRA INDRAWATI SUAN\n Titik Koordinat : https://www.google.com/maps/uv?pb=!1s0x2c55815a9f3060b5%3A0x2cc058fcbfc91dcb!3m1!7e115!4s%2Fmaps%2Fplace%2Fkomida%2Bkefamenanu%2F%40-9.4549512%2C124.4820151%2C3a%2C75y%2C65.84h%2C90t%2Fdata%3D*213m4*211e1*213m2*211shN6sOTAZSxTsxc6t99xH0g*212e0*214m2*213m1*211s0x2c55815a9f3060b5%3A0x2cc058fcbfc91dcb%3Fsa%3DX%26ved%3D2ahUKEwijpoailZWLAxXo4zgGHQxsKU0Qpx96BAgkEAA!5skomida%20kefamenanu%20-%20Penelusuran%20Google!15sCgIgARICCAI&imagekey=!1e2!2shN6sOTAZSxTsxc6t99xH0g&cr=le_a7&hl=id&ved=1t%3A206134&ictx=111&cshid=1737955667671019",
        "#tarus": "Nama Cabang : TARUS\n Kode Cab : 165\n Email : komidataros@gmail.com\n Alamat : JLN BHAKTI WARGA RT 30 RW 10 KEC. FATULULI-OEBOBO KOTA KUPANG\n Opening : yahh ga diinput\n Manager : LEONARDO NOLDI HAUSUFA\n STAF MSA : GEORGE PRADANA SAEBESI\n Titik Koordinat : <a href='https://maps.app.goo.gl/8vaYgAs3hQ6q3Jms5'>Cek MAPS</a>",
       
        }

    for key, response in responses.items():
        if key in user_text:
            sent_message = await update.message.reply_text(response, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
            asyncio.create_task(delete_message_later(context, chat_id, sent_message.message_id))
            break

async def help_command(update: Update, context: CallbackContext):
    help_text = ( 
        "Pertolongan pertama pada orang pusing setengah mati :(\n\n"
        "#infoTF         :" " informasi terkait tf\n"
        "#tutormdis  :" " Tutorial Setting Mdis Sistem\n"
        "#formatreq :" " Format Request, Mari saling memudahkan\n"
        "#regional     :" " KANTOR REGIONAL S\n"
        "#email          :" " Email Regional dan KANTOR PUSAT\n"
        "#inputinfo   :" " Input Informasi Cabang\n\n"
        "INFORMASI CABANG : \n"
        "#ende1        :" " Informasi Cabang ENDE 1\n"
        "#soe             :" " Informasi Cabang di SOE\n"
        "#insana       :" " Informasi Cabang di INSANA\n"
        "#kangae      :" " Informasi Cabang di KANGAE\n"
        "#nikiniki       :" " Informasi Cabang di NIKI-NIKI\n"
        "#atambua   :" " Informasi Cabang di ATAMBUA\n"
        "#malaka      :" " Informasi Cabang di MALAKA\n"
        "#kefa           :" " Informasi Cabang di KEFAMENANU\n"
        "#tarus         :" " Informasi Cabang di TARUS\n\n"
        "BOT INI AKAN MEMBALAS JIKA KANG JAMJAM LAPTOPNYA ONLINE, KALAU GA MEMBALAS BERARTI SEDANG OFFLINE"
    )       
    await update.message.reply_text(help_text)

def main():
    TOKEN = "7750914821:AAGMZAffji-fEadwzZwHP-ldAEGVUXZP53E"
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    
    app.run_polling()

if __name__ == "__main__":
    main()