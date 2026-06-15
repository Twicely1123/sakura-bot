# Sakura Town — FAQ System

## ไฟล์ที่มี
- `index.html` — หน้าเว็บ FAQ (GitHub Pages)
- `bot.py` — Discord Bot ตอบอัตโนมัติ
- `requirements.txt` — library ที่ต้องการ

---

## 1. หน้าเว็บ FAQ (GitHub Pages — ฟรี)

1. สร้าง repo ใหม่บน GitHub ชื่อ `sakura-faq`
2. อัปโหลดไฟล์ `index.html`
3. ไปที่ Settings → Pages → Branch: main → Save
4. ได้ URL: `https://[username].github.io/sakura-faq`

---

## 2. Discord Bot (Railway.app — ฟรี tier)

### สร้าง Bot Token
1. ไปที่ https://discord.com/developers/applications
2. New Application → Bot → Reset Token → คัดลอก Token
3. เปิด: Message Content Intent, Server Members Intent

### Deploy บน Railway
1. สมัคร https://railway.app (ฟรี)
2. New Project → Deploy from GitHub Repo
3. อัปโหลด `bot.py` และ `requirements.txt`
4. ไปที่ Variables → เพิ่ม `DISCORD_BOT_TOKEN = [token ของคุณ]`
5. Deploy!

### เพิ่ม Bot เข้า Server
ใช้ URL นี้ (แทน CLIENT_ID):
```
https://discord.com/oauth2/authorize?client_id=CLIENT_ID&permissions=2048&scope=bot
```

---

## เพิ่ม FAQ ใหม่

แก้ในไฟล์ `bot.py` ที่ส่วน `FAQ = [...]`

```python
{
    "keywords": ["คำค้น1", "คำค้น2"],
    "q": "คำถามที่แสดง",
    "a": "คำตอบที่จะส่ง",
},
```

และแก้ในไฟล์ `index.html` ที่ส่วน `const FAQ = [...]` เช่นกันครับ
