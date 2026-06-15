import os
import discord
from discord.ext import commands
from difflib import SequenceMatcher

# ============================================================
# FAQ DATA — เพิ่ม/แก้ไขคำถามตรงนี้ได้เลย
# ============================================================
FAQ = [
    {
        "keywords": ["เข้าไม่ได้", "timeout", "connect", "เชื่อมต่อ", "เข้าเซิร์ฟ"],
        "q": "เข้าเซิร์ฟไม่ได้ / timeout",
        "a": (
            "ลองทำตามนี้ครับ:\n"
            "1️⃣ ปิด VPN ถ้าเปิดอยู่\n"
            "2️⃣ กด F8 แล้วพิมพ์ `connect [IP เซิร์ฟ]` ใหม่\n"
            "3️⃣ ล้างแคช FiveM ที่ `%localappdata%/FiveM` → ลบโฟลเดอร์ cache\n"
            "ถ้ายังไม่ได้ เปิด ticket ที่ <#ticket-channel> ครับ 🌸"
        ),
    },
    {
        "keywords": ["เงินหาย", "เงิน", "ล่ม", "หาย", "หายหลัง"],
        "q": "เงินหายหลังเซิร์ฟล่ม",
        "a": (
            "เปิด ticket หมวด **ติดต่อ support** ครับ แจ้งข้อมูลนี้ด้วย:\n"
            "• จำนวนเงินที่หาย\n"
            "• เวลาโดยประมาณ\n"
            "• กิจกรรมที่ทำก่อนเงินหาย\n"
            "ทีมงานจะตรวจ log และคืนให้ถ้าเป็นความผิดพลาดของเซิร์ฟครับ 💰"
        ),
    },
    {
        "keywords": ["ไอเทมหาย", "ไอเทม", "ของหาย", "ตู้", "รถหาย"],
        "q": "ไอเทมหาย",
        "a": (
            "เปิด ticket หมวด **แจ้งบัค** ระบุมาด้วยครับ:\n"
            "• ชื่อไอเทมที่หาย\n"
            "• ตำแหน่งที่วางไว้\n"
            "• เวลาที่หาย\n"
            "ทีม DEV จะตรวจสอบ log ให้ครับ 🔍"
        ),
    },
    {
        "keywords": ["แบน", "ban", "โดนแบน", "unban", "ปลดแบน", "ขอ unban"],
        "q": "โดนแบน / ขอ unban",
        "a": (
            "เปิด ticket หมวด **ติดต่อแอดมิน** ครับ แนบมาด้วย:\n"
            "• Discord ID ของคุณ\n"
            "• Steam ID\n"
            "• อธิบายสถานการณ์ตามความจริง\n"
            "ทีมงานจะตรวจสอบและแจ้งผลใน 24-48 ชั่วโมง ⏳"
        ),
    },
    {
        "keywords": ["rdm", "vdm", "กฎ", "rule", "โทษ", "ผิดกฎ"],
        "q": "RDM / VDM คืออะไร?",
        "a": (
            "**RDM** (Random DeathMatch) = ฆ่าผู้เล่นอื่นโดยไม่มีเหตุใน RP\n"
            "**VDM** (Vehicle DeathMatch) = ใช้ยานพาหนะชนผู้เล่นโดยเจตนา\n"
            "โทษเริ่มจาก kick ไปจนถึง permanent ban ขึ้นกับความรุนแรง 🚫"
        ),
    },
    {
        "keywords": ["metagaming", "meta", "นอกเกม"],
        "q": "Metagaming คืออะไร?",
        "a": (
            "**Metagaming** คือการนำข้อมูลนอกเกม (Discord, LINE) มาใช้ใน RP\n"
            "เช่น รู้ตำแหน่งศัตรูจาก Discord แล้วไปดักใน RP ถือว่าผิดกฎครับ ❌"
        ),
    },
    {
        "keywords": ["สมัคร", "ลงทะเบียน", "เข้าเกมครั้งแรก", "สมัครสมาชิก"],
        "q": "วิธีสมัครสมาชิก",
        "a": (
            "เปิด ticket หมวด **ติดต่อ support** ใน Discord ครับ\n"
            "กรอกข้อมูลตามฟอร์มที่บอทส่งมา:\n"
            "• ชื่อในเกม\n"
            "• Discord ID\n"
            "• ยืนยันว่าอ่านกฎครบแล้ว ✅"
        ),
    },
    {
        "keywords": ["lag", "กระตุก", "fps", "แล็ค", "ช้า"],
        "q": "เกมกระตุก / lag",
        "a": (
            "ลองทำตามนี้ครับ:\n"
            "1️⃣ ลด Graphics Settings ใน GTA V\n"
            "2️⃣ ปิดโปรแกรมที่ใช้ RAM เยอะ\n"
            "3️⃣ ล้างแคช FiveM\n"
            "4️⃣ ตรวจ ping ใน F8 (ควรต่ำกว่า 150ms) 🎮"
        ),
    },
    {
        "keywords": ["ตัวละครหาย", "char หาย", "character หาย", "ตัวละคร"],
        "q": "ตัวละครหาย",
        "a": (
            "เปิด ticket หมวด **แจ้งบัค** ครับ แนบ:\n"
            "• Screenshot\n"
            "• เวลาที่เจอปัญหา\n"
            "ทีม DEV จะตรวจสอบ database ให้ครับ 🌸"
        ),
    },
    {
        "keywords": ["restart", "รีสตาร์ท", "เซิร์ฟปิด", "กี่โมง"],
        "q": "เซิร์ฟ restart กี่โมง?",
        "a": "ตรวจสอบได้ที่ช่อง **#ประกาศ** หรือ **#ข้อมูลเซิร์ฟ** ใน Discord ครับ เวลาอาจเปลี่ยนแปลงได้ 🕐",
    },
]

# ============================================================
# BOT SETUP
# ============================================================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

SUPPORT_CHANNELS = []  # ใส่ channel ID ที่ต้องการให้บอทตอบ เช่น [123456789, 987654321]
# ถ้าปล่อยว่าง บอทจะตอบทุก channel

FAQ_CHANNEL_ID = None  # ใส่ ID ของช่อง FAQ ถ้ามี

def find_faq(text: str):
    text_lower = text.lower()
    best_score = 0
    best_item = None

    for item in FAQ:
        # ตรวจ keyword ตรงๆ ก่อน
        for kw in item["keywords"]:
            if kw in text_lower:
                return item

        # fuzzy match backup
        for kw in item["keywords"]:
            score = SequenceMatcher(None, kw, text_lower).ratio()
            if score > best_score:
                best_score = score
                best_item = item

    # คืนผลถ้า score สูงพอ
    if best_score >= 0.65:
        return best_item
    return None


def build_embed(item):
    embed = discord.Embed(
        title=f"🌸 {item['q']}",
        description=item["a"],
        color=0xE8A0BF,
    )
    embed.set_footer(text="Sakura Town · หากยังไม่ได้รับการแก้ไข เปิด ticket ได้เลยครับ")
    return embed


@bot.event
async def on_ready():
    print(f"✅ {bot.user} พร้อมทำงานแล้วครับ")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="ช่วยตอบคำถาม Sakura Town 🌸"
    ))


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # จำกัดเฉพาะ channel ที่กำหนด (ถ้ามี)
    if SUPPORT_CHANNELS and message.channel.id not in SUPPORT_CHANNELS:
        await bot.process_commands(message)
        return

    # ค้นหา FAQ
    result = find_faq(message.content)
    if result:
        embed = build_embed(result)
        await message.reply(embed=embed, mention_author=False)

    await bot.process_commands(message)


# คำสั่ง !faq ค้นหาด้วยตัวเอง
@bot.command(name="faq")
async def faq_cmd(ctx, *, query: str = ""):
    if not query:
        # แสดงรายการทั้งหมด
        embed = discord.Embed(title="🌸 รายการคำถามทั้งหมด", color=0xE8A0BF)
        for item in FAQ:
            embed.add_field(name=f"• {item['q']}", value="\u200b", inline=False)
        embed.set_footer(text="ใช้ !faq [คำค้น] เพื่อค้นหา เช่น !faq เงินหาย")
        await ctx.reply(embed=embed, mention_author=False)
        return

    result = find_faq(query)
    if result:
        await ctx.reply(embed=build_embed(result), mention_author=False)
    else:
        embed = discord.Embed(
            description="❌ ไม่พบคำตอบที่ตรงกันครับ ลองเปิด ticket หรือถามแอดมินโดยตรงได้เลย 🌸",
            color=0x3D2232,
        )
        await ctx.reply(embed=embed, mention_author=False)


# คำสั่ง !ping ทดสอบ
@bot.command(name="ping")
async def ping(ctx):
    await ctx.reply(f"🌸 Pong! `{round(bot.latency * 1000)}ms`", mention_author=False)


# ============================================================
# RUN
# ============================================================
TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ ไม่พบ DISCORD_BOT_TOKEN ใน environment variables")

bot.run(TOKEN)
