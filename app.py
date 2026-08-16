import streamlit as st
import requests

# ============================================================
# SOZLAMALAR VA RANGLAR
# ============================================================
st.set_page_config(page_title="UzSkill", page_icon="🎓", layout="centered")

NAVY = "#1E2761"
GOLD = "#D4A017"
ICE = "#CADCFC"
GRAY = "#5A6178"

# ============================================================
# MA'LUMOTLAR
# ============================================================
YONALISHLAR = {
    "dizayn": {"name": "Grafik dizayn", "desc": "Logotip, banner, ijtimoiy tarmoq vizuallari"},
    "dasturlash": {"name": "Web dasturlash", "desc": "Sayt va ilova qurish, front-end asoslari"},
    "video": {"name": "Video montaj", "desc": "Reels, YouTube va reklama videolari"},
    "yozish": {"name": "Ingliz tilida yozish", "desc": "Kontent, copywriting, tarjima"},
    "tarjima": {"name": "Tarjimonlik", "desc": "Hujjat va matnlarni tarjima qilish"},
}

SAVOLLAR = [
    {
        "q": "Bo'sh vaqtingizda ko'proq nima qilasiz?",
        "opts": [
            ("Rasm chizish / dizayn ilovalarida o'ynash", "dizayn"),
            ("Kompyuter va texnika bilan band bo'lish", "dasturlash"),
            ("Video ko'rish / tahrirlash", "video"),
            ("Kitob o'qish / yozish", "yozish"),
        ],
    },
    {
        "q": "Qaysi fan sizga yengilroq kelgan?",
        "opts": [
            ("Chizmachilik / san'at", "dizayn"),
            ("Matematika / mantiq", "dasturlash"),
            ("Ingliz tili", "yozish"),
            ("Informatika", "dasturlash"),
        ],
    },
    {
        "q": "Diqqatingiz nimaga ko'proq qaratiladi?",
        "opts": [
            ("Ranglar va shakllarga", "dizayn"),
            ("Kod va tuzilmaga", "dasturlash"),
            ("Harakat va ritmga", "video"),
            ("So'z va ma'noga", "yozish"),
        ],
    },
    {
        "q": "Ingliz tili darajangiz qanday?",
        "opts": [
            ("Kuchli, erkin gaplasha olaman", "yozish"),
            ("O'rtacha, tushunaman", "tarjima"),
            ("Boshlang'ich", "dizayn"),
            ("Texnik terminlarni bilaman", "dasturlash"),
        ],
    },
    {
        "q": "Qaysi vazifa sizni charchatmaydi?",
        "opts": [
            ("Soatlab bir dizaynni pardozlash", "dizayn"),
            ("Xatoni topib, tuzatish", "dasturlash"),
            ("Kadrlarni kesish, musiqa qo'yish", "video"),
            ("Matnni qayta-qayta tahrirlash", "yozish"),
        ],
    },
    {
        "q": "Ikkita tilni solishtirib, noaniq so'zni topish sizga yoqadimi?",
        "opts": [
            ("Ha, juda qiziq", "tarjima"),
            ("Yo'q, menga vizual ish yoqadi", "dizayn"),
            ("Yo'q, menga texnik ish yoqadi", "dasturlash"),
            ("Ba'zan, lekin video afzal", "video"),
        ],
    },
    {
        "q": "Do'stlaringiz sizni qanday tasvirlaydi?",
        "opts": [
            ("Ijodkor va estetik did egasi", "dizayn"),
            ("Mantiqiy va tartibli", "dasturlash"),
            ("Tez fikrlaydigan, ritm hissi bor", "video"),
            ("So'zamol va aniq yozadigan", "yozish"),
        ],
    },
    {
        "q": "Yangi dastur yoki ilovani o'rganishda sizga qaysi biri qiziqroq?",
        "opts": [
            ("Uning tashqi ko'rinishi (UI)", "dizayn"),
            ("Uning qanday ishlashi (kod)", "dasturlash"),
            ("Uni tanishtiruvchi video", "video"),
            ("Uning matn va yozuvlari", "yozish"),
        ],
    },
    {
        "q": "Ikki tilda yozilgan matnda xato bo'lsa, buni sezasizmi?",
        "opts": [
            ("Ha, darhol sezaman", "tarjima"),
            ("Faqat o'z tilimda", "yozish"),
            ("Kamdan kam", "dizayn"),
            ("Bunga unchalik e'tibor bermayman", "dasturlash"),
        ],
    },
    {
        "q": "Qaysi natija sizni ko'proq mag'rur qiladi?",
        "opts": [
            ("Chiroyli tayyor dizayn", "dizayn"),
            ("Ishlab turgan dastur/sayt", "dasturlash"),
            ("Ko'p ko'rilgan video", "video"),
            ("Aniq va ta'sirli matn", "yozish"),
        ],
    },
]

# Har bir yo'nalish uchun ALOHIDA mikro-kurs
KURSLAR = {
    "dizayn": {
        "title": "Grafik dizayn asoslari",
        "darslar": [
            "1-dars: Dizayn tamoyillari — rang, shrift va kompozitsiya asoslari",
            "2-dars: Canva bilan ishlash — birinchi bannerni yaratish",
            "3-dars: Logotip yaratish — oddiy va professional logotip qadamlari",
            "4-dars: Portfolio tayyorlash — 3 ta ish namunasini joylashtirish",
            "5-dars: Birinchi buyurtma — boshlang'ich buyurtmalar havzasiga qo'shilish",
        ],
    },
    "dasturlash": {
        "title": "Web dasturlash asoslari",
        "darslar": [
            "1-dars: HTML va CSS asoslari — birinchi sahifani yaratish",
            "2-dars: Responsive dizayn — mobil qurilmalarga moslashtirish",
            "3-dars: Oddiy JavaScript — sahifaga interaktivlik qo'shish",
            "4-dars: Tayyor loyihani GitHub'ga joylash",
            "5-dars: Birinchi buyurtma — boshlang'ich buyurtmalar havzasiga qo'shilish",
        ],
    },
    "video": {
        "title": "Video montaj asoslari",
        "darslar": [
            "1-dars: Montaj dasturi bilan tanishuv (CapCut/Premiere)",
            "2-dars: Kadrlarni kesish va ketma-ketlik qurish",
            "3-dars: Musiqa, matn va effektlar qo'shish",
            "4-dars: Reels/TikTok formatida qisqa video tayyorlash",
            "5-dars: Birinchi buyurtma — boshlang'ich buyurtmalar havzasiga qo'shilish",
        ],
    },
    "yozish": {
        "title": "Ingliz tilida yozish asoslari",
        "darslar": [
            "1-dars: Copywriting asoslari — qisqa va ta'sirli matn yozish",
            "2-dars: Mahsulot tavsiflarini yozish",
            "3-dars: Blog va SEO matnlari",
            "4-dars: Grammatika va uslubni tekshirish vositalari",
            "5-dars: Birinchi buyurtma — boshlang'ich buyurtmalar havzasiga qo'shilish",
        ],
    },
    "tarjima": {
        "title": "Tarjimonlik asoslari",
        "darslar": [
            "1-dars: Tarjima nazariyasi va uslub tanlash",
            "2-dars: Texnik va rasmiy hujjatlarni tarjima qilish",
            "3-dars: Tarjima vositalari (CAT tools) bilan tanishuv",
            "4-dars: Sifat nazorati — o'z tarjimangizni tekshirish",
            "5-dars: Birinchi buyurtma — boshlang'ich buyurtmalar havzasiga qo'shilish",
        ],
    },
}

XALQARO_LOYIHALAR = [
    {
        "id": 1,
        "client": "Marta K.",
        "country": "Germaniya 🇩🇪",
        "title": "Kichik kafe uchun logotip",
        "budget": "$40",
        "category": "dizayn",
        "desc": "Yangi ochilgan kofe do'koni uchun sodda, iliq logotip kerak.",
    },
    {
        "id": 2,
        "client": "James R.",
        "country": "AQSH 🇺🇸",
        "title": "Instagram post shabloni (5 dona)",
        "budget": "$35",
        "category": "dizayn",
        "desc": "Kichik onlayn do'kon uchun 5 ta bir xil uslubdagi post shabloni.",
    },
    {
        "id": 3,
        "client": "Sofia T.",
        "country": "Italiya 🇮🇹",
        "title": "Oddiy landing sahifa (HTML/CSS)",
        "budget": "$70",
        "category": "dasturlash",
        "desc": "Kichik biznes uchun bir sahifali sayt, mobil versiyaga moslashtirilgan.",
    },
    {
        "id": 4,
        "client": "Emma W.",
        "country": "Avstraliya 🇦🇺",
        "title": "TikTok uchun 3 ta qisqa video montaj",
        "budget": "$45",
        "category": "video",
        "desc": "Tayyor xom material asosida 3 ta 30 soniyalik reklama video.",
    },
    {
        "id": 5,
        "client": "Olivia S.",
        "country": "Niderlandiya 🇳🇱",
        "title": "Mahsulot tavsifi matnlarini yozish (10 dona)",
        "budget": "$40",
        "category": "yozish",
        "desc": "Onlayn do'kon uchun 10 ta mahsulotga qisqa, jozibali tavsif.",
    },
    {
        "id": 6,
        "client": "Hana P.",
        "country": "Chexiya 🇨🇿",
        "title": "Hujjatni ingliz tilidan o'zbekchaga tarjima",
        "budget": "$30",
        "category": "tarjima",
        "desc": "5 betlik shartnoma hujjatini aniq va rasmiy uslubda tarjima qilish.",
    },
]

# ============================================================
# SESSION STATE
# ============================================================
defaults = {
    "page": "bosh_sahifa",
    "user": None,
    "diag_step": 0,
    "diag_scores": {},
    "diag_result": None,
    "kurs_progress": {k: [False] * len(v["darslar"]) for k, v in KURSLAR.items()},
    "arizalar": [],
    "api_key": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def goto(page_name):
    st.session_state.page = page_name


# ============================================================
# YUQORI NAVIGATSIYA
# ============================================================
st.markdown(
    f"""
    <div style="background-color:{NAVY}; padding:16px 20px; border-radius:10px; margin-bottom:20px;">
        <span style="color:white; font-size:22px; font-weight:bold;">🎓 UzSkill</span>
    </div>
    """,
    unsafe_allow_html=True,
)

cols = st.columns(6)
labels = ["Bosh sahifa", "Diagnostika", "Kurslar", "AI Tarjimon", "Xalqaro mijozlar", "Kabinet"]
targets = ["bosh_sahifa", "diagnostika", "kurslar", "tarjimon", "mijozlar", "kabinet"]
for c, label, target in zip(cols, labels, targets):
    with c:
        if st.button(label, use_container_width=True):
            goto(target)

st.divider()

# ============================================================
# SAHIFA: BOSH SAHIFA
# ============================================================
if st.session_state.page == "bosh_sahifa":
    st.title("Qobiliyating — chegarasiz valyutang")
    st.write(
        "O'z uyingdan chiqmasdan, qobiliyatingni AI orqali aniqlab, "
        "xalqaro mijozlar bilan bog'lanadigan platforma."
    )
    if st.session_state.user is None:
        st.info("Boshlash uchun avval ro'yxatdan o'ting.")
        if st.button("📝 Ro'yxatdan o'tish", type="primary"):
            goto("royxat")
    else:
        st.success(f"Xush kelibsiz, {st.session_state.user['name']}!")
        if st.button("🚀 Diagnostikani boshlash", type="primary"):
            goto("diagnostika")

# ============================================================
# SAHIFA: RO'YXATDAN O'TISH
# ============================================================
elif st.session_state.page == "royxat":
    st.title("Ro'yxatdan o'tish")
    st.write("Shaxsiy kabinetingizni ochish uchun ma'lumotlaringizni kiriting.")

    with st.form("royxat_form"):
        name = st.text_input("Ism familiya")
        phone = st.text_input("Telefon raqam", placeholder="+998 90 123 45 67")
        email = st.text_input("Email", placeholder="email@misol.uz")
        submitted = st.form_submit_button("Ro'yxatdan o'tish", type="primary")

        if submitted:
            if not name or not phone or not email:
                st.error("Barcha maydonlarni to'ldiring.")
            else:
                st.session_state.user = {"name": name, "phone": phone, "email": email}
                st.success("Muvaffaqiyatli ro'yxatdan o'tdingiz!")
                goto("kabinet")
                st.rerun()

# ============================================================
# SAHIFA: DIAGNOSTIKA
# ============================================================
elif st.session_state.page == "diagnostika":
    st.title("Diagnostika")

    if st.session_state.user is None:
        st.warning("Diagnostikadan o'tish uchun avval ro'yxatdan o'ting.")
        if st.button("Ro'yxatdan o'tish"):
            goto("royxat")

    elif st.session_state.diag_result is not None:
        res = YONALISHLAR[st.session_state.diag_result]
        st.success(f"Sizga eng mos yo'nalish: **{res['name']}**")
        st.write(res["desc"])
        if st.button("Qayta topshirish"):
            st.session_state.diag_step = 0
            st.session_state.diag_scores = {}
            st.session_state.diag_result = None
            st.rerun()
        if st.button("Kursni boshlash ➡️", type="primary"):
            goto("kurslar")

    else:
        step = st.session_state.diag_step
        total = len(SAVOLLAR)
        st.progress(step / total)
        st.caption(f"{step + 1} / {total}")

        savol = SAVOLLAR[step]
        st.subheader(savol["q"])

        for label, tag in savol["opts"]:
            if st.button(label, key=f"opt_{step}_{tag}", use_container_width=True):
                scores = st.session_state.diag_scores
                scores[tag] = scores.get(tag, 0) + 1
                st.session_state.diag_scores = scores

                if step + 1 < total:
                    st.session_state.diag_step += 1
                else:
                    top = max(scores, key=scores.get)
                    st.session_state.diag_result = top
                st.rerun()

# ============================================================
# SAHIFA: KURSLAR (endi diagnostikaga bog'langan)
# ============================================================
elif st.session_state.page == "kurslar":
    diag = st.session_state.diag_result

    if diag is None:
        st.title("Kurslar")
        st.info(
            "Sizga mos kursni tavsiya qilish uchun avval diagnostikadan o'ting. "
            "Xohlasangiz, pastdan kursni qo'lda ham tanlashingiz mumkin."
        )
        if st.button("🚀 Diagnostikaga o'tish", type="primary"):
            goto("diagnostika")
        st.divider()
        tanlangan = st.selectbox(
            "Yoki kursni qo'lda tanlang:",
            options=list(KURSLAR.keys()),
            format_func=lambda k: YONALISHLAR[k]["name"],
        )
    else:
        tanlangan = diag
        st.title(KURSLAR[tanlangan]["title"])
        st.caption(f"Diagnostika natijangizga mos kurs: {YONALISHLAR[tanlangan]['name']}")

    kurs = KURSLAR[tanlangan]
    progress_list = st.session_state.kurs_progress[tanlangan]

    completed = sum(progress_list)
    total = len(kurs["darslar"])
    st.progress(completed / total)
    st.caption(f"{completed} / {total} dars tugallandi")

    for i, dars in enumerate(kurs["darslar"]):
        checked = st.checkbox(dars, value=progress_list[i], key=f"dars_{tanlangan}_{i}")
        st.session_state.kurs_progress[tanlangan][i] = checked

    if all(st.session_state.kurs_progress[tanlangan]):
        st.success("🎉 Tabriklaymiz! Kurs tugallandi. Endi xalqaro mijozlarga ariza berishingiz mumkin.")
        if st.button("Xalqaro mijozlarni ko'rish ➡️", type="primary"):
            goto("mijozlar")

# ============================================================
# SAHIFA: AI TARJIMON
# ============================================================
elif st.session_state.page == "tarjimon":
    st.title("AI Tarjimon")
    st.write("O'zbek tilida yozing — professional ingliz tiliga o'giramiz, xalqaro mijoz bilan yozishma uchun.")

    with st.expander("⚙️ API kalitini sozlash (birinchi marta)"):
        st.write(
            "Bu funksiya ishlashi uchun Anthropic API kaliti kerak. "
            "Kalitni [console.anthropic.com](https://console.anthropic.com) dan olishingiz mumkin. "
            "Kalit faqat shu sessiyada saqlanadi, hech qayerga yuborilmaydi."
        )
        key_input = st.text_input("API kalit", type="password", value=st.session_state.api_key)
        if key_input:
            st.session_state.api_key = key_input

    matn = st.text_area(
        "O'zbekcha xabaringiz",
        placeholder="Masalan: Assalomu alaykum, men sizning loyihangiz uchun logotip tayyorlashga tayyorman.",
        height=120,
    )

    if st.button("Ingliz tiliga o'girish", type="primary"):
        if not st.session_state.api_key:
            st.error("Avval yuqoridagi bo'limda API kalitini kiriting.")
        elif not matn.strip():
            st.warning("Avval matn kiriting.")
        else:
            with st.spinner("Tarjima qilinmoqda..."):
                try:
                    response = requests.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={
                            "x-api-key": st.session_state.api_key,
                            "anthropic-version": "2023-06-01",
                            "content-type": "application/json",
                        },
                        json={
                            "model": "claude-sonnet-4-6",
                            "max_tokens": 500,
                            "messages": [
                                {
                                    "role": "user",
                                    "content": (
                                        "Translate the following message from Uzbek to natural, "
                                        "professional English suitable for writing to an international "
                                        "freelance client. Only output the English translation, nothing else.\n\n"
                                        f"Message: {matn}"
                                    ),
                                }
                            ],
                        },
                        timeout=30,
                    )
                    data = response.json()
                    if "content" in data:
                        natija = "".join(block.get("text", "") for block in data["content"])
                        st.success("Tayyor!")
                        st.info(natija)
                    else:
                        err_msg = data.get("error", {}).get("message", "Noma'lum xato")
                        st.error(f"Xatolik: {err_msg}")
                except Exception as e:
                    st.error(f"Xatolik yuz berdi: {e}")

# ============================================================
# SAHIFA: XALQARO MIJOZLAR
# ============================================================
elif st.session_state.page == "mijozlar":
    st.title("Boshlang'ich buyurtmalar havzasi")

    diag = st.session_state.diag_result
    tanlangan_kurs = diag if diag else None
    completed = sum(st.session_state.kurs_progress[tanlangan_kurs]) if tanlangan_kurs else 0
    total = len(KURSLAR[tanlangan_kurs]["darslar"]) if tanlangan_kurs else 1

    if not diag or completed < total:
        st.warning("Xalqaro buyurtmalarga ariza berish uchun avval diagnostikadan o'ting va tegishli kursni to'liq tugating.")
        if st.button("Diagnostikaga o'tish"):
            goto("diagnostika")
    else:
        st.write(f"**{YONALISHLAR[diag]['name']}** yo'nalishiga mos loyihalar yuqorida ko'rsatiladi.")

        loyihalar = sorted(
            XALQARO_LOYIHALAR,
            key=lambda l: 0 if l["category"] == diag else 1,
        )

        for l in loyihalar:
            mos = l["category"] == diag
            with st.container(border=True):
                badge = "⭐ Sizga mos" if mos else YONALISHLAR[l["category"]]["name"]
                st.markdown(f"**{l['title']}** — {badge}")
                st.caption(f"{l['client']} · {l['country']} · Byudjet: {l['budget']}")
                st.write(l["desc"])

                if l["id"] in st.session_state.arizalar:
                    st.success("✓ Ariza yuborildi — mijoz javobini kutmoqdasiz")
                else:
                    if st.button("Ariza berish", key=f"apply_{l['id']}"):
                        st.session_state.arizalar.append(l["id"])
                        st.rerun()

# ============================================================
# SAHIFA: SHAXSIY KABINET
# ============================================================
elif st.session_state.page == "kabinet":
    st.title("Shaxsiy kabinet")

    if st.session_state.user is None:
        st.warning("Kabinetni ko'rish uchun avval ro'yxatdan o'ting.")
        if st.button("Ro'yxatdan o'tish"):
            goto("royxat")
    else:
        u = st.session_state.user
        st.subheader(f"👤 {u['name']}")
        st.write(f"📞 {u['phone']}")
        st.write(f"✉️ {u['email']}")

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Diagnostika natijasi**")
            if st.session_state.diag_result:
                st.write(YONALISHLAR[st.session_state.diag_result]["name"])
            else:
                st.write("Hali topshirilmagan")
                if st.button("Testni boshlash"):
                    goto("diagnostika")

        with col2:
            diag = st.session_state.diag_result
            st.markdown("**Kurs progressi**")
            if diag:
                completed = sum(st.session_state.kurs_progress[diag])
                total = len(KURSLAR[diag]["darslar"])
                st.write(f"{completed} / {total} dars")
                st.progress(completed / total)
            else:
                st.write("Diagnostikadan o'tilmagan")

        st.divider()
        st.markdown(f"**Xalqaro arizalar:** {len(st.session_state.arizalar)} ta yuborilgan")

        st.divider()
        if st.button("🚪 Chiqish"):
            st.session_state.user = None
            goto("bosh_sahifa")
            st.rerun()
