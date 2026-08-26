import streamlit as st
import requests
import json
import os
from datetime import datetime

# ============================================================
# SOZLAMALAR VA RANGLAR (yangi logotipga mos: ko'k -> yashil)
# ============================================================
st.set_page_config(page_title="UzSkill", page_icon="🎓", layout="wide")

DEEP = "#0A1628"      # chuqur qorong'i fon
BLUE = "#1E5FD9"      # logotipdagi ko'k
GREEN = "#1DBE6E"     # logotipdagi yashil
GREEN_LIGHT = "#5CF2A6"
ICE = "#CFE3FF"
GRAY = "#6B7280"

DATA_FILE = "uzskill_data.json"
CATALOG_FILE = "uzskill_catalog.json"
PORTFOLIO_DIR = "portfolio_uploads"
ADMIN_PASSWORD = "uzskill2026"
FOUNDER_EMAILS = ["niginaismoilova086@gmail.com"]  # Boshlang'ich asoschi email(lar)i — zaxira sifatida

# ============================================================
# CUSTOM CSS — "Raqamli tun" (Digital Night) uslubi, logotipga mos
# ============================================================
st.markdown(
    f"""
    <style>
    /* ---- Umumiy fon: chuqur ko'k gradient + nozik sxema naqshi ---- */
    .stApp {{
        background:
            radial-gradient(circle at 15% 20%, rgba(30,95,217,0.18) 0%, transparent 35%),
            radial-gradient(circle at 85% 75%, rgba(29,190,110,0.16) 0%, transparent 40%),
            linear-gradient(160deg, {DEEP} 0%, #0D1F38 45%, #0A1628 100%);
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: "";
        position: fixed; inset: 0; pointer-events: none; opacity: 0.05;
        background-image:
            linear-gradient(rgba(92,242,166,0.6) 1px, transparent 1px),
            linear-gradient(90deg, rgba(92,242,166,0.6) 1px, transparent 1px);
        background-size: 46px 46px;
    }}

    /* ---- Matn ranglari ---- */
    h1, h2, h3, h4, .stMarkdown, label, p {{ color: #EAF2FF; }}
    .stCaption, [data-testid="stCaptionContainer"] {{ color: #93A5C4 !important; }}

    /* ---- Shishasimon (glass) kartalar ---- */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(255,255,255,0.045);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(92,242,166,0.15);
        border-radius: 14px;
    }}

    /* ---- Metrikalar ---- */
    div[data-testid="stMetric"] {{
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(8px);
        padding: 14px; border-radius: 12px;
        border: 1px solid rgba(30,95,217,0.25);
    }}
    div[data-testid="stMetricValue"] {{ color: {GREEN_LIGHT}; }}
    div[data-testid="stMetricLabel"] {{ color: #93A5C4; }}

    /* ---- Tugmalar: yorqinlik (glow) effekti bilan ---- */
    .stButton>button {{
        border-radius: 10px; font-weight: 600;
        background: rgba(255,255,255,0.06);
        color: #EAF2FF; border: 1px solid rgba(92,242,166,0.25);
        transition: all 0.2s ease;
    }}
    .stButton>button:hover {{
        border-color: {GREEN_LIGHT};
        box-shadow: 0 0 14px rgba(92,242,166,0.35);
    }}
    .stButton>button[kind="primary"] {{
        background: linear-gradient(90deg, {BLUE}, {GREEN});
        color: white; border: none;
        box-shadow: 0 0 16px rgba(29,190,110,0.4);
    }}
    .stButton>button[kind="primary"]:hover {{
        box-shadow: 0 0 22px rgba(92,242,166,0.6);
    }}

    /* ---- Progress-bar: yashil-ko'k gradient ---- */
    div[data-testid="stProgress"] > div > div > div {{
        background: linear-gradient(90deg, {BLUE}, {GREEN_LIGHT}) !important;
    }}

    /* ---- Kirish maydonlari ---- */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {{
        background: rgba(255,255,255,0.06) !important;
        color: #EAF2FF !important;
        border: 1px solid rgba(147,165,196,0.25) !important;
    }}

    /* ---- Chap panel (sidebar) ---- */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0D1F38, #08131F);
        border-right: 1px solid rgba(92,242,166,0.12);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# MA'LUMOTLAR OMBORI — FOYDALANUVCHILAR
# ============================================================
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"users": {}}
    return {"users": {}}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_current_user():
    if st.session_state.user is None:
        return
    data = load_data()
    email = st.session_state.user["email"]
    data["users"][email] = {
        "name": st.session_state.user["name"],
        "phone": st.session_state.user["phone"],
        "email": email,
        "kurs_progress": st.session_state.kurs_progress,
        "til_progress": st.session_state.til_progress,
        "arizalar": st.session_state.arizalar,
        "portfolio": st.session_state.get("portfolio", []),
        "bildirishnomalar": st.session_state.get("bildirishnomalar", []),
        "royxatdan_otgan_sana": st.session_state.user.get(
            "royxatdan_otgan_sana", datetime.now().strftime("%Y-%m-%d %H:%M")
        ),
    }
    save_data(data)


def push_notification(email, text):
    """Berilgan foydalanuvchiga bildirishnoma qo'shadi (fayl orqali, doimiy saqlanadi)."""
    data = load_data()
    if email not in data["users"]:
        return
    notifs = data["users"][email].get("bildirishnomalar", [])
    notifs.append({"text": text, "sana": datetime.now().strftime("%Y-%m-%d %H:%M"), "oqilgan": False})
    data["users"][email]["bildirishnomalar"] = notifs
    save_data(data)
    if st.session_state.user and st.session_state.user["email"] == email:
        st.session_state.bildirishnomalar = notifs


def broadcast_notification(text):
    """Barcha ro'yxatdan o'tgan foydalanuvchilarga bildirishnoma yuboradi (masalan yangi yangilik e'lon qilinganda)."""
    data = load_data()
    for email in data["users"]:
        notifs = data["users"][email].get("bildirishnomalar", [])
        notifs.append({"text": text, "sana": datetime.now().strftime("%Y-%m-%d %H:%M"), "oqilgan": False})
        data["users"][email]["bildirishnomalar"] = notifs
    save_data(data)


def get_thread_id(user_email, vakansiya_id):
    return f"{user_email}::{vakansiya_id}"


def load_messages():
    data = load_data()
    return data.get("xabarlar", {})


def send_message(thread_id, sender, text):
    data = load_data()
    threads = data.get("xabarlar", {})
    msgs = threads.get(thread_id, [])
    msgs.append({"from": sender, "text": text, "sana": datetime.now().strftime("%Y-%m-%d %H:%M")})
    threads[thread_id] = msgs
    data["xabarlar"] = threads
    save_data(data)


# ============================================================
# KATALOG OMBORI — ADMIN BOSHQARADIGAN YO'NALISH/KURSLAR
# ============================================================
def default_catalog():
    """Boshlang'ich namuna kataloq — 6 ta kasbiy yo'nalish + 5 ta til kursi."""
    return {
        "yonalishlar": {
            "dizayn": {"name": "Grafik dizayn", "turi": "kasb", "desc": "Logotip, banner, ijtimoiy tarmoq vizuallari", "darslar": []},
            "dasturlash": {"name": "Web dasturlash", "turi": "kasb", "desc": "Sayt va ilova qurish asoslari", "darslar": []},
            "video": {"name": "Video montaj", "turi": "kasb", "desc": "Reels, YouTube va reklama videolari", "darslar": []},
            "tikuvchilik": {"name": "Tikuvchilik va hunarmandchilik", "turi": "kasb", "desc": "Qo'lda tikilgan mahsulotlarni xalqaro bozorda sotish", "darslar": []},
            "smm": {"name": "Ijtimoiy tarmoq boshqaruvi (SMM)", "turi": "kasb", "desc": "Instagram/TikTok kontent boshqaruvi", "darslar": []},
            "malumot": {"name": "Virtual yordamchi", "turi": "kasb", "desc": "Jadval, kalendar, elektron pochta boshqaruvi", "darslar": []},
        },
        "til_kurslari": {
            "ingliz": {"name": "Ingliz tili", "turi": "til", "desc": "Xalqaro mijozlar bilan muloqot uchun", "darslar": []},
            "rus": {"name": "Rus tili", "turi": "til", "desc": "MDH bozori uchun", "darslar": []},
            "arab": {"name": "Arab tili", "turi": "til", "desc": "Yaqin Sharq bozori uchun", "darslar": []},
            "nemis": {"name": "Nemis tili", "turi": "til", "desc": "Yevropa bozori uchun", "darslar": []},
            "koreys": {"name": "Koreys tili", "turi": "til", "desc": "Osiyo bozori uchun", "darslar": []},
        },
        "eʼlonlar": [],  # Asoschi eʼlonlari / videolari
    }


def load_catalog():
    if os.path.exists(CATALOG_FILE):
        try:
            with open(CATALOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    cat = default_catalog()
    save_catalog(cat)
    return cat


def save_catalog(cat):
    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        json.dump(cat, f, ensure_ascii=False, indent=2)


def get_admin_emails():
    data = load_data()
    return data.get("admin_emails", [])


def add_admin_email(email):
    data = load_data()
    admins = data.get("admin_emails", [])
    if email not in admins:
        admins.append(email)
    data["admin_emails"] = admins
    save_data(data)


def remove_admin_email(email):
    data = load_data()
    admins = data.get("admin_emails", [])
    if email in admins:
        admins.remove(email)
    data["admin_emails"] = admins
    save_data(data)


def is_founder():
    """Admin huquqi ikki yo'l bilan beriladi:
    1) Admin parol orqali kirilgan bo'lsa (taqdimot/demo uchun, hech qanday emailga bog'liq emas)
    2) Foydalanuvchi ro'yxatdan o'tgan email FOUNDER_EMAILS yoki dinamik admin ro'yxatida bo'lsa
    """
    if st.session_state.get("admin_logged_in"):
        return True
    if st.session_state.user is not None:
        email = st.session_state.user["email"]
        if email in FOUNDER_EMAILS or email in get_admin_emails():
            return True
    return False


# ============================================================
# SESSION STATE
# ============================================================
defaults = {
    "page": "bosh_sahifa", "user": None,
    "kurs_progress": {}, "til_progress": {},
    "arizalar": [], "portfolio": [], "api_key": "", "admin_logged_in": False,
    "bildirishnomalar": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def goto(page_name):
    st.session_state.page = page_name


catalog = load_catalog()


def ensure_progress(key, group="yonalishlar"):
    """Foydalanuvchi progress lug'atida shu kurs uchun joy borligiga ishonch hosil qiladi."""
    target = st.session_state.kurs_progress if group == "yonalishlar" else st.session_state.til_progress
    n = len(catalog[group if group == "yonalishlar" else "til_kurslari"][key]["darslar"])
    if key not in target or len(target[key]) != n:
        target[key] = [False] * n


# ============================================================
# LOGOTIP BLOKI (matn asosida — rasm keyinroq biriktiriladi)
# ============================================================
def logo_block(size="large"):
    fs = 46 if size == "large" else 22
    st.markdown(
        f"""
        <div style="text-align:center;">
            <span style="font-size:{fs}px; font-weight:900; color:white;">Uz</span><span style="font-size:{fs}px; font-weight:900; background: linear-gradient(90deg,{BLUE},{GREEN}); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Skill</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# LANDING (KIRISHDAN OLDINGI BOSH SAHIFA)
# ============================================================
if (st.session_state.user is None and not st.session_state.get("admin_logged_in")) and st.session_state.page in ("bosh_sahifa", "royxat"):
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, {DEEP}, #0F2A4A); padding: 60px 30px; border-radius: 16px; text-align:center; margin-bottom: 20px;">
        """,
        unsafe_allow_html=True,
    )
    logo_block("large")
    st.markdown(
        f"""
        <p style="color:{ICE}; font-size:16px; margin-top:10px;">LEARN · BUILD · GROW · SUCCEED</p>
        <h2 style="color:white; margin-top:30px;">Xush kelibsiz, UzSkill platformasiga!</h2>
        <p style="color:{ICE}; font-size:15px; max-width:600px; margin:10px auto;">
            Qobiliyatingizni aniqlang, o'rganing va xalqaro bozorda daromad toping.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.page == "bosh_sahifa":
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            b1, b2 = st.columns(2)
            with b1:
                if st.button("🔑 Kirish", use_container_width=True):
                    st.session_state.page = "royxat"
                    st.session_state["_auth_tab"] = "login"
                    st.rerun()
            with b2:
                if st.button("📝 Ro'yxatdan o'tish", use_container_width=True, type="primary"):
                    st.session_state.page = "royxat"
                    st.session_state["_auth_tab"] = "register"
                    st.rerun()

        st.divider()
        st.markdown("### Xizmat yo'nalishlarimiz")
        cols = st.columns(3)
        all_tracks = list(catalog["yonalishlar"].items())
        for i, (key, v) in enumerate(all_tracks):
            with cols[i % 3]:
                st.markdown(f"**{v['name']}**")
                st.caption(v["desc"])

        st.divider()
        with st.expander("🔒 Admin sifatida kirish (namoyish / boshqaruv uchun)"):
            st.caption("Ro'yxatdan o'tmasdan, to'g'ridan-to'g'ri admin huquqi bilan kirish — taqdimot/demo uchun qulay.")
            admin_pwd = st.text_input("Admin parolini kiriting", type="password", key="landing_admin_pwd")
            if st.button("Admin sifatida kirish", key="landing_admin_btn"):
                if admin_pwd == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    goto("kabinet_bosh")
                    st.rerun()
                else:
                    st.error("Parol noto'g'ri.")

    else:
        tab_default = 0 if st.session_state.get("_auth_tab") == "register" else 1
        tab1, tab2 = st.tabs(["Ro'yxatdan o'tish", "Kirish"])

        with tab1:
            st.warning(
                "🔒 **Xavfsizlik eslatmasi:** Bu — pilot/demo bosqichidagi platforma. "
                "Hozircha parol tizimi mavjud emas (faqat email orqali kirish). "
                "Iltimos, real to'lov kartasi raqami yoki maxfiy hujjat ma'lumotlarini kiritmang."
            )
            with st.form("royxat_form"):
                name = st.text_input("Ism familiya")
                phone = st.text_input("Telefon raqam", placeholder="+998 90 123 45 67")
                email = st.text_input("Email", placeholder="email@misol.uz")
                submitted = st.form_submit_button("Ro'yxatdan o'tish", type="primary")
                if submitted:
                    if not name or not phone or not email:
                        st.error("Barcha maydonlarni to'ldiring.")
                    else:
                        data = load_data()
                        if email in data["users"]:
                            st.error("Bu email bilan allaqachon ro'yxatdan o'tilgan.")
                        else:
                            st.session_state.user = {"name": name, "phone": phone, "email": email,
                                                      "royxatdan_otgan_sana": datetime.now().strftime("%Y-%m-%d %H:%M")}
                            save_current_user()
                            st.success("Muvaffaqiyatli ro'yxatdan o'tdingiz!")
                            goto("kabinet_bosh")
                            st.rerun()

        with tab2:
            with st.form("login_form"):
                login_email = st.text_input("Ro'yxatdan o'tgan emailingiz")
                login_submitted = st.form_submit_button("Kirish", type="primary")
                if login_submitted:
                    data = load_data()
                    if login_email in data["users"]:
                        rec = data["users"][login_email]
                        st.session_state.user = {"name": rec["name"], "phone": rec["phone"], "email": rec["email"],
                                                  "royxatdan_otgan_sana": rec.get("royxatdan_otgan_sana", "")}
                        st.session_state.kurs_progress = rec.get("kurs_progress", {})
                        st.session_state.til_progress = rec.get("til_progress", {})
                        st.session_state.arizalar = rec.get("arizalar", [])
                        st.session_state.portfolio = rec.get("portfolio", [])
                        st.session_state.bildirishnomalar = rec.get("bildirishnomalar", [])
                        st.success(f"Xush kelibsiz, {rec['name']}!")
                        goto("kabinet_bosh")
                        st.rerun()
                    else:
                        st.error("Bu email bilan ro'yxatdan o'tilmagan.")

        if st.button("⬅️ Orqaga"):
            goto("bosh_sahifa")
            st.rerun()


# ============================================================
# KIRGANDAN KEYINGI QISM — SHAXSIY KABINET
# ============================================================
else:
    with st.sidebar:
        logo_block("small")
        if st.session_state.user:
            st.caption(f"👤 {st.session_state.user['name']}")
        else:
            st.caption("🔒 Admin rejimi (mehmon)")
        st.divider()

        nav = [
            ("kabinet_bosh", "🏠 Kabinet bosh sahifasi"),
            ("dashboard", "📊 Progress dashboard"),
            ("bildirishnomalar", "🔔 Bildirishnomalar"),
            ("loyiha_haqida", "ℹ️ Loyiha haqida"),
            ("kataloglar", "📚 Kataloglar (Yo'nalishlar)"),
            ("til_kurslari", "🌐 Til kurslari"),
            ("mijozlar", "🌍 Xalqaro vakansiyalar"),
            ("tarjimon", "🤖 AI Tarjimon"),
            ("xabarlar", "💬 Xabarlar"),
            ("sertifikatlarim", "📜 Sertifikatlarim"),
            ("sozlamalar", "⚙️ Sozlamalar"),
        ]
        for key, label in nav:
            if st.button(label, use_container_width=True, key=f"nav_{key}"):
                goto(key)

        if is_founder():
            st.divider()
            st.caption("👑 ASOSCHI PANELI")
            if st.button("📢 Yangilik / video joylash", use_container_width=True):
                goto("asoschi_panel")
            if st.button("🛠️ Kataloglarni boshqarish", use_container_width=True):
                goto("admin_katalog")

        st.divider()
        with st.expander("🔒 Admin panel (statistika)"):
            if st.button("Kirish", use_container_width=True, key="goto_admin_stat"):
                goto("admin")

        st.divider()
        if st.button("🚪 Chiqish", use_container_width=True):
            st.session_state.user = None
            st.session_state.admin_logged_in = False
            st.session_state.kurs_progress = {}
            st.session_state.til_progress = {}
            st.session_state.arizalar = []
            st.session_state.portfolio = []
            goto("bosh_sahifa")
            st.rerun()

    u = st.session_state.user or {"name": "Admin (mehmon)", "phone": "—", "email": "admin@uzskill.local"}

    # ---------------- KABINET BOSH SAHIFASI ----------------
    if st.session_state.page == "kabinet_bosh":
        st.title(f"Xush kelibsiz, {u['name']}! 👋")

        if catalog.get("eʼlonlar"):
            st.markdown("### 📢 So'nggi yangiliklar")
            for e in reversed(catalog["eʼlonlar"][-3:]):
                with st.container(border=True):
                    st.markdown(f"**{e['sarlavha']}**  \n{e['matn']}")
                    if e.get("video_url"):
                        st.video(e["video_url"])
                    st.caption(e["sana"])
            st.divider()

        c1, c2, c3, c4 = st.columns(4)
        total_kurs = sum(1 for v in st.session_state.kurs_progress.values() if any(v))
        total_ariza = len(st.session_state.arizalar)
        oqilmagan = sum(1 for n in st.session_state.get("bildirishnomalar", []) if not n.get("oqilgan"))
        c1.metric("Boshlagan kurslar", total_kurs)
        c2.metric("Yuborilgan arizalar", total_ariza)
        c3.metric("Portfolio fayllari", len(st.session_state.portfolio))
        c4.metric("🔔 O'qilmagan bildirishnoma", oqilmagan)

        st.divider()
        st.markdown("### Tezkor havolalar")
        qc1, qc2, qc3 = st.columns(3)
        with qc1:
            if st.button("📚 Kataloglarga o'tish", use_container_width=True):
                goto("kataloglar")
        with qc2:
            if st.button("🌍 Vakansiyalarni ko'rish", use_container_width=True):
                goto("mijozlar")
        with qc3:
            if st.button("🤖 AI Tarjimondan foydalanish", use_container_width=True):
                goto("tarjimon")

    # ---------------- PROGRESS DASHBOARD ----------------
    elif st.session_state.page == "dashboard":
        st.title("📊 Progress dashboard")

        kasb_done = sum(1 for v in st.session_state.kurs_progress.values() if v and all(v))
        kasb_total = len(catalog["yonalishlar"])
        til_done = sum(1 for v in st.session_state.til_progress.values() if v and all(v))
        til_total = len(catalog["til_kurslari"])

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Tugatilgan kasb kurslari", f"{kasb_done}/{kasb_total}")
        c2.metric("Tugatilgan til kurslari", f"{til_done}/{til_total}")
        c3.metric("Yuborilgan arizalar", len(st.session_state.arizalar))
        c4.metric("Portfolio fayllari", len(st.session_state.portfolio))

        st.divider()
        st.markdown("### Kasb yo'nalishlari bo'yicha progress")
        for key, track in catalog["yonalishlar"].items():
            ensure_progress(key, "yonalishlar")
            prog = st.session_state.kurs_progress[key]
            total = len(prog)
            done = sum(prog)
            pct = (done / total) if total else 0
            st.write(f"**{track['name']}** — {done}/{total} dars")
            st.progress(pct)

        st.divider()
        st.markdown("### Til kurslari bo'yicha progress")
        for key, til in catalog["til_kurslari"].items():
            ensure_progress(key, "til")
            prog = st.session_state.til_progress[key]
            total = len(prog)
            done = sum(prog)
            pct = (done / total) if total else 0
            st.write(f"**{til['name']}** — {done}/{total} dars")
            st.progress(pct)

        st.divider()
        st.markdown("### Arizalarim holati")
        if not st.session_state.arizalar:
            st.caption("Hali hech qanday arizangiz yo'q.")
        else:
            for aid in st.session_state.arizalar:
                st.write(f"— Vakansiya #{aid}: **yuborilgan**, javob kutilmoqda")

    # ---------------- BILDIRISHNOMALAR ----------------
    elif st.session_state.page == "bildirishnomalar":
        st.title("🔔 Bildirishnomalar")
        notifs = st.session_state.get("bildirishnomalar", [])
        if not notifs:
            st.info("Hozircha bildirishnoma yo'q.")
        else:
            for n in reversed(notifs):
                icon = "🟢" if not n.get("oqilgan") else "⚪"
                with st.container(border=True):
                    st.write(f"{icon} {n['text']}")
                    st.caption(n["sana"])
            if st.button("Barchasini o'qilgan deb belgilash"):
                for n in st.session_state.bildirishnomalar:
                    n["oqilgan"] = True
                save_current_user()
                st.rerun()

    # ---------------- LOYIHA HAQIDA ----------------
    elif st.session_state.page == "loyiha_haqida":
        st.title("ℹ️ Loyiha haqida")
        st.markdown("### UzSkill nima?")
        st.write(
            "UzSkill — o'z uyidan chiqmasdan xalqaro bozorda ishlashni istagan o'zbek yoshlari va "
            "kattalari uchun qobiliyatini aniqlab, o'rgatib, xalqaro mijozlar bilan bog'laydigan platforma."
        )
        st.markdown("### Nega UzSkill?")
        st.write(
            "- Nafaqat AI/IT sohasi — hunarmandchilik, tikuvchilik va boshqa amaliy kasblar ham qamrab olinadi\n"
            "- Har bir kurs oxirida test va foiz asosidagi sertifikat\n"
            "- Til bilmaydiganlar uchun til kurslari va AI tarjimon\n"
            "- Xalqaro vakansiyalarga to'g'ridan-to'g'ri ariza"
        )
        st.markdown("### Aloqa")
        st.write("📧 niginaismoilova086@gmail.com")
        st.write("💬 Telegram: @Isma1lova_14")

    # ---------------- KATALOGLAR (YO'NALISHLAR) ----------------
    elif st.session_state.page == "kataloglar":
        st.title("📚 Kataloglar — Yo'nalishlar")
        st.caption("Sizga mos yo'nalishni tanlang. Har bir kurs video darslar va test bilan tugaydi.")

        tracks = catalog["yonalishlar"]
        qidiruv = st.text_input("🔎 Yo'nalish nomini qidirish", placeholder="Masalan: dizayn, tikuvchilik...")
        filtered_keys = [k for k in tracks if qidiruv.lower() in tracks[k]["name"].lower()] if qidiruv else list(tracks.keys())
        if not filtered_keys:
            st.warning("Hech narsa topilmadi.")
            filtered_keys = list(tracks.keys())

        selected = st.selectbox("Yo'nalishni tanlang:", options=filtered_keys,
                                 format_func=lambda k: tracks[k]["name"])
        ensure_progress(selected, "yonalishlar")
        track = tracks[selected]
        st.subheader(track["name"])
        st.write(track["desc"])

        reytinglar = track.get("reytinglar", [])
        if reytinglar:
            orta = sum(r["ball"] for r in reytinglar) / len(reytinglar)
            st.caption(f"⭐ O'rtacha baho: {orta:.1f} / 5  ({len(reytinglar)} ta baho)")

        if not track["darslar"]:
            st.info("Bu yo'nalish uchun hozircha darslar joylanmagan. Asoschi tez orada video darslarni qo'shadi.")
        else:
            progress = st.session_state.kurs_progress[selected]
            completed = sum(progress)
            total = len(track["darslar"])
            st.progress(completed / total)
            st.caption(f"{completed} / {total} dars tugallandi")

            for i, dars in enumerate(track["darslar"]):
                with st.container(border=True):
                    checked = st.checkbox(dars["title"], value=progress[i], key=f"y_{selected}_{i}")
                    if checked != progress[i]:
                        st.session_state.kurs_progress[selected][i] = checked
                        save_current_user()
                    if dars.get("video_url"):
                        st.video(dars["video_url"])

            if completed == total and total > 0:
                foiz = 100
                st.success(f"🎉 Kurs tugallandi! Natijangiz: {foiz}%")
                st.info(f"📜 Sertifikat: **{track['name']}** yo'nalishi bo'yicha {foiz}% natija bilan tugatildi.")

                if st.session_state.user and f"notif_sent_{selected}" not in st.session_state:
                    push_notification(st.session_state.user["email"], f"Tabriklaymiz! Siz \"{track['name']}\" kursini tugatdingiz va sertifikat qo'lga kiritdingiz.")
                    st.session_state[f"notif_sent_{selected}"] = True

                already_rated = any(r["email"] == (st.session_state.user or {}).get("email") for r in reytinglar)
                if not already_rated and st.session_state.user:
                    with st.form(f"rate_{selected}"):
                        st.markdown("#### Kursni baholang")
                        ball = st.slider("Baho (1-5)", 1, 5, 5)
                        sharh = st.text_area("Sharh (ixtiyoriy)")
                        if st.form_submit_button("Baholashni yuborish"):
                            cat_fresh = load_catalog()
                            cat_fresh["yonalishlar"][selected].setdefault("reytinglar", []).append(
                                {"email": st.session_state.user["email"], "ball": ball, "sharh": sharh}
                            )
                            save_catalog(cat_fresh)
                            st.success("Baholaganingiz uchun rahmat!")
                            st.rerun()

                if st.button("Xalqaro vakansiyalarni ko'rish ➡️", type="primary"):
                    goto("mijozlar")

    # ---------------- TIL KURSLARI ----------------
    elif st.session_state.page == "til_kurslari":
        st.title("🌐 Til kurslari")
        st.caption("Xalqaro mijozlar bilan muloqot uchun til ko'nikmalaringizni oshiring.")

        tils = catalog["til_kurslari"]
        selected = st.selectbox("Tilni tanlang:", options=list(tils.keys()), format_func=lambda k: tils[k]["name"])
        ensure_progress(selected, "til")
        til = tils[selected]
        st.subheader(til["name"])
        st.write(til["desc"])

        if not til["darslar"]:
            st.info("Bu til kursi uchun hozircha darslar joylanmagan.")
        else:
            progress = st.session_state.til_progress[selected]
            completed = sum(progress)
            total = len(til["darslar"])
            st.progress(completed / total)
            st.caption(f"{completed} / {total} dars tugallandi")
            for i, dars in enumerate(til["darslar"]):
                with st.container(border=True):
                    checked = st.checkbox(dars["title"], value=progress[i], key=f"t_{selected}_{i}")
                    if checked != progress[i]:
                        st.session_state.til_progress[selected][i] = checked
                        save_current_user()
                    if dars.get("video_url"):
                        st.video(dars["video_url"])
            if completed == total and total > 0:
                st.success(f"🎉 {til['name']} kursi tugallandi! Sertifikat qo'lga kiritildi.")

    # ---------------- XALQARO VAKANSIYALAR ----------------
    elif st.session_state.page == "mijozlar":
        st.title("🌍 Xalqaro vakansiyalar")
        st.caption("O'ziga munosib vakansiyani tanlang va onlayn ariza yuboring.")

        # Namuna vakansiyalar (keyinchalik admin orqali boshqariladi)
        vakansiyalar = [
            {"id": 1, "kompaniya": "Marta Design Studio", "mamlakat": "Germaniya 🇩🇪", "lavozim": "Grafik dizayner (frilanс)", "yonalish": "dizayn", "desc": "Kichik bizneslar uchun vizual materiallar tayyorlash."},
            {"id": 2, "kompaniya": "Nordic Web", "mamlakat": "Shvetsiya 🇸🇪", "lavozim": "Junior web dasturchi", "yonalish": "dasturlash", "desc": "Landing sahifalar va kichik veb-loyihalar."},
            {"id": 3, "kompaniya": "EtsyCraft Collective", "mamlakat": "AQSH 🇺🇸", "lavozim": "Qo'lda tikilgan mahsulot yetkazib beruvchi", "yonalish": "tikuvchilik", "desc": "O'zbek milliy naqshli mahsulotlarni xalqaro bozorga chiqarish."},
        ]

        filtr_col1, filtr_col2 = st.columns(2)
        with filtr_col1:
            yon_filtr = st.selectbox("Yo'nalish bo'yicha filtrlash", options=["Barchasi"] + list(catalog["yonalishlar"].keys()),
                                      format_func=lambda k: "Barchasi" if k == "Barchasi" else catalog["yonalishlar"][k]["name"])
        with filtr_col2:
            matn_filtr = st.text_input("🔎 Lavozim yoki kompaniya bo'yicha qidirish")

        korsatilgan = vakansiyalar
        if yon_filtr != "Barchasi":
            korsatilgan = [v for v in korsatilgan if v["yonalish"] == yon_filtr]
        if matn_filtr:
            korsatilgan = [v for v in korsatilgan if matn_filtr.lower() in v["lavozim"].lower() or matn_filtr.lower() in v["kompaniya"].lower()]

        if not korsatilgan:
            st.info("Hech qanday vakansiya topilmadi.")

        for v in korsatilgan:
            with st.container(border=True):
                st.markdown(f"**{v['lavozim']}** — {v['kompaniya']} ({v['mamlakat']})")
                st.write(v["desc"])
                if v["id"] in st.session_state.arizalar:
                    st.success("✓ Ariza yuborilgan")
                else:
                    if st.button("Ariza yuborish", key=f"ariza_btn_{v['id']}"):
                        st.session_state[f"ariza_form_{v['id']}"] = True

                if st.session_state.get(f"ariza_form_{v['id']}"):
                    with st.form(f"ariza_{v['id']}"):
                        st.markdown("#### Ariza topshirish")
                        ism = st.text_input("Ism Familiya", value=u["name"])
                        tel = st.text_input("Telefon", value=u["phone"])
                        em = st.text_input("Email", value=u["email"])
                        yon = st.selectbox("Yo'nalish", options=list(catalog["yonalishlar"].keys()),
                                            format_func=lambda k: catalog["yonalishlar"][k]["name"],
                                            index=list(catalog["yonalishlar"].keys()).index(v["yonalish"]) if v["yonalish"] in catalog["yonalishlar"] else 0)
                        st.markdown("**Sertifikatlar**")
                        st.caption("UzSkill platformasidan olingan sertifikatlaringiz avtomatik biriktiriladi.")
                        boshqa_sert = st.file_uploader("Boshqa sertifikatlaringizni yuklang (ixtiyoriy)", accept_multiple_files=True)
                        nega = st.text_area("Nega aynan bu ishni tanladingiz?")
                        nega_siz = st.text_area("Nega aynan sizni tanlashlari kerak?")
                        tajriba = st.text_area("Tegishli tajribangiz bormi? Qisqacha yozing.")
                        yuborish = st.form_submit_button("Arizani yuborish", type="primary")
                        if yuborish:
                            st.session_state.arizalar.append(v["id"])
                            save_current_user()
                            if st.session_state.user:
                                push_notification(u["email"], f"Arizangiz \"{v['lavozim']}\" ({v['kompaniya']}) uchun yuborildi.")
                                thread_id = get_thread_id(u["email"], v["id"])
                                send_message(thread_id, "sistema", f"Ariza qabul qilindi: {v['lavozim']} — {v['kompaniya']}. Savol-javob shu yerda davom etadi.")
                            st.success("Arizangiz yuborildi! Tez orada ko'rib chiqiladi. Yozishmani 'Xabarlar' bo'limidan kuzatishingiz mumkin.")
                            st.session_state[f"ariza_form_{v['id']}"] = False
                            st.rerun()

    # ---------------- AI TARJIMON ----------------
    elif st.session_state.page == "tarjimon":
        st.title("🤖 AI Tarjimon")
        st.write("O'zbek tilida yozing — professional ingliz tiliga o'giramiz.")

        with st.expander("⚙️ API kalitini sozlash"):
            st.write("Kalitni [console.anthropic.com](https://console.anthropic.com) dan oling.")
            key_input = st.text_input("API kalit", type="password", value=st.session_state.api_key)
            if key_input:
                st.session_state.api_key = key_input

        matn = st.text_area("O'zbekcha xabaringiz", height=120)
        if st.button("Ingliz tiliga o'girish", type="primary"):
            if not st.session_state.api_key:
                st.error("Avval API kalitini kiriting.")
            elif not matn.strip():
                st.warning("Avval matn kiriting.")
            else:
                with st.spinner("Tarjima qilinmoqda..."):
                    try:
                        response = requests.post(
                            "https://api.anthropic.com/v1/messages",
                            headers={"x-api-key": st.session_state.api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
                            json={"model": "claude-sonnet-4-6", "max_tokens": 500,
                                  "messages": [{"role": "user", "content": f"Translate the following message from Uzbek to natural, professional English. Only output the translation.\n\nMessage: {matn}"}]},
                            timeout=30,
                        )
                        data = response.json()
                        if "content" in data:
                            natija = "".join(b.get("text", "") for b in data["content"])
                            st.success("Tayyor!")
                            st.info(natija)
                        else:
                            st.error(f"Xatolik: {data.get('error', {}).get('message', 'Noma\'lum')}")
                    except Exception as e:
                        st.error(f"Xatolik: {e}")

    # ---------------- XABARLAR ----------------
    elif st.session_state.page == "xabarlar":
        st.title("💬 Xabarlar")
        VAKANSIYA_NOMLARI = {1: "Grafik dizayner — Marta Design Studio", 2: "Junior web dasturchi — Nordic Web", 3: "Hunarmandchilik yetkazib beruvchi — EtsyCraft Collective"}
        all_threads = load_messages()

        if is_founder():
            st.caption("Admin ko'rinishi — barcha foydalanuvchilarning yozishmalarini ko'rasiz va javob bera olasiz.")
            if not all_threads:
                st.info("Hozircha hech qanday yozishma yo'q.")
            else:
                thread_ids = list(all_threads.keys())
                chosen = st.selectbox("Suhbatni tanlang", options=thread_ids,
                                       format_func=lambda t: f"{t.split('::')[0]} — {VAKANSIYA_NOMLARI.get(int(t.split('::')[1]), t.split('::')[1])}")
                st.divider()
                for m in all_threads[chosen]:
                    kimdan = "🏢 Admin/Mijoz" if m["from"] in ("sistema", "admin") else f"👤 {m['from']}"
                    st.markdown(f"**{kimdan}** · _{m['sana']}_")
                    st.write(m["text"])
                    st.divider()
                javob = st.text_area("Javob yozing", key="admin_reply_text")
                if st.button("Yuborish", type="primary", key="admin_reply_btn"):
                    if javob.strip():
                        send_message(chosen, "admin", javob)
                        foydalanuvchi_email = chosen.split("::")[0]
                        push_notification(foydalanuvchi_email, "Arizangiz bo'yicha yangi javob keldi. 'Xabarlar' bo'limini tekshiring.")
                        st.rerun()
        else:
            if not st.session_state.user:
                st.warning("Xabarlarni ko'rish uchun ro'yxatdan o'ting yoki kiring.")
            else:
                my_threads = {tid: msgs for tid, msgs in all_threads.items() if tid.startswith(u["email"] + "::")}
                if not my_threads:
                    st.info("Hali hech qanday yozishmangiz yo'q. Vakansiyaga ariza yuborganingizdan so'ng, shu yerda suhbat boshlanadi.")
                else:
                    thread_ids = list(my_threads.keys())
                    chosen = st.selectbox("Suhbatni tanlang", options=thread_ids,
                                           format_func=lambda t: VAKANSIYA_NOMLARI.get(int(t.split("::")[1]), t.split("::")[1]))
                    st.divider()
                    for m in my_threads[chosen]:
                        kimdan = "🏢 Mijoz / Admin" if m["from"] in ("sistema", "admin") else "👤 Siz"
                        st.markdown(f"**{kimdan}** · _{m['sana']}_")
                        st.write(m["text"])
                        st.divider()
                    javob = st.text_area("Xabar yozing", key="user_reply_text")
                    if st.button("Yuborish", type="primary", key="user_reply_btn"):
                        if javob.strip():
                            send_message(chosen, u["email"], javob)
                            st.rerun()

        st.caption("📱 Kelajakda: real-vaqtli chat va video-qo'ng'iroq (Zoom-ga o'xshash) shu bo'limga qo'shiladi.")

    # ---------------- SERTIFIKATLARIM ----------------
    elif st.session_state.page == "sertifikatlarim":
        st.title("📜 Sertifikatlarim")
        found = False
        for key, prog in st.session_state.kurs_progress.items():
            if prog and all(prog) and key in catalog["yonalishlar"]:
                found = True
                st.success(f"✅ {catalog['yonalishlar'][key]['name']} — 100% natija bilan tugatilgan")
        for key, prog in st.session_state.til_progress.items():
            if prog and all(prog) and key in catalog["til_kurslari"]:
                found = True
                st.success(f"✅ {catalog['til_kurslari'][key]['name']} (til kursi) — tugatilgan")
        if not found:
            st.info("Hali hech qanday kursni to'liq tugatmagansiz.")

    # ---------------- SOZLAMALAR ----------------
    elif st.session_state.page == "sozlamalar":
        st.title("⚙️ Sozlamalar")
        with st.form("profile_form"):
            new_name = st.text_input("Ism familiya", value=u["name"])
            new_phone = st.text_input("Telefon raqam", value=u["phone"])
            if st.form_submit_button("Saqlash", type="primary"):
                st.session_state.user["name"] = new_name
                st.session_state.user["phone"] = new_phone
                save_current_user()
                st.success("Profil yangilandi!")

        st.divider()
        st.markdown("### 📁 Portfolio")
        uploaded = st.file_uploader("Fayl yuklash", type=["png", "jpg", "jpeg", "pdf"])
        if uploaded is not None:
            user_dir = os.path.join(PORTFOLIO_DIR, u["email"].replace("@", "_at_"))
            os.makedirs(user_dir, exist_ok=True)
            with open(os.path.join(user_dir, uploaded.name), "wb") as f:
                f.write(uploaded.getbuffer())
            if uploaded.name not in st.session_state.portfolio:
                st.session_state.portfolio.append(uploaded.name)
                save_current_user()
            st.success("Yuklandi!")

        st.divider()
        st.markdown("### 🗑️ Hisobni o'chirish")
        confirm = st.checkbox("Hisobimni o'chirishni tasdiqlayman")
        if st.button("Hisobni o'chirish", disabled=not confirm):
            data = load_data()
            if u["email"] in data["users"]:
                del data["users"][u["email"]]
                save_data(data)
            st.session_state.user = None
            goto("bosh_sahifa")
            st.rerun()

    # ---------------- ASOSCHI PANELI: YANGILIK/VIDEO JOYLASH ----------------
    elif st.session_state.page == "asoschi_panel" and is_founder():
        st.title("👑 Asoschi paneli — Yangilik joylash")
        st.caption("Bu yerda joylagan yangilik/video barcha foydalanuvchilarga darhol ko'rinadi.")
        with st.form("elon_form"):
            sarlavha = st.text_input("Sarlavha")
            matn = st.text_area("Matn")
            video_url = st.text_input("Video havolasi (YouTube va h.k., ixtiyoriy)")
            if st.form_submit_button("Joylash", type="primary"):
                cat = load_catalog()
                cat["eʼlonlar"].append({
                    "sarlavha": sarlavha, "matn": matn, "video_url": video_url,
                    "sana": datetime.now().strftime("%Y-%m-%d %H:%M"),
                })
                save_catalog(cat)
                broadcast_notification(f"Yangi yangilik: \"{sarlavha}\" — kabinet bosh sahifasida ko'ring.")
                st.success("Yangilik joylandi! Endi barcha foydalanuvchilar kabinet bosh sahifasida va bildirishnomalarida ko'radi.")
                st.rerun()

    # ---------------- ASOSCHI PANELI: KATALOGNI BOSHQARISH ----------------
    elif st.session_state.page == "admin_katalog" and is_founder():
        st.title("🛠️ Kataloglarni boshqarish")
        cat = load_catalog()

        tab1, tab2, tab3, tab4 = st.tabs(["Yo'nalishga dars qo'shish", "Til kursiga dars qo'shish", "Yangi yo'nalish qo'shish", "👥 Adminlarni boshqarish"])

        with tab1:
            key = st.selectbox("Yo'nalish", options=list(cat["yonalishlar"].keys()),
                                format_func=lambda k: cat["yonalishlar"][k]["name"], key="add_dars_y")
            title = st.text_input("Dars nomi", key="dars_title_y")
            video = st.text_input("Video havolasi", key="dars_video_y")
            if st.button("Darsni qo'shish", key="btn_add_dars_y"):
                if title:
                    cat["yonalishlar"][key]["darslar"].append({"title": title, "video_url": video})
                    save_catalog(cat)
                    st.success("Dars qo'shildi!")
                    st.rerun()

        with tab2:
            key = st.selectbox("Til kursi", options=list(cat["til_kurslari"].keys()),
                                format_func=lambda k: cat["til_kurslari"][k]["name"], key="add_dars_t")
            title = st.text_input("Dars nomi", key="dars_title_t")
            video = st.text_input("Video havolasi", key="dars_video_t")
            if st.button("Darsni qo'shish", key="btn_add_dars_t"):
                if title:
                    cat["til_kurslari"][key]["darslar"].append({"title": title, "video_url": video})
                    save_catalog(cat)
                    st.success("Dars qo'shildi!")
                    st.rerun()

        with tab3:
            new_key = st.text_input("Yo'nalish kaliti (lotincha, bo'sh joysiz, masalan: 'oshpazlik')")
            new_name = st.text_input("Yo'nalish nomi")
            new_desc = st.text_area("Tavsif")
            if st.button("Yo'nalish qo'shish"):
                if new_key and new_name:
                    cat["yonalishlar"][new_key] = {"name": new_name, "turi": "kasb", "desc": new_desc, "darslar": []}
                    save_catalog(cat)
                    st.success("Yangi yo'nalish qo'shildi!")
                    st.rerun()

        with tab4:
            st.caption(
                "Bu yerga qo'shilgan email — o'sha kishi keyingi safar shu email bilan ro'yxatdan o'tib "
                "yoki kirib, avtomatik ravishda Asoschi panelidan foydalana oladi (parolsiz)."
            )
            new_admin_email = st.text_input("Yangi admin email manzili", placeholder="hamkor@misol.uz")
            if st.button("Admin sifatida qo'shish"):
                if new_admin_email:
                    add_admin_email(new_admin_email)
                    st.success(f"{new_admin_email} endi admin huquqiga ega.")
                    st.rerun()

            st.divider()
            st.markdown("**Hozirgi qo'shimcha adminlar:**")
            current_admins = get_admin_emails()
            if not current_admins:
                st.caption("Hozircha qo'shimcha admin yo'q — faqat parol orqali yoki asosiy email orqali kirish mumkin.")
            for em in current_admins:
                c1, c2 = st.columns([4, 1])
                c1.write(em)
                if c2.button("O'chirish", key=f"rm_admin_{em}"):
                    remove_admin_email(em)
                    st.rerun()

    # ---------------- ADMIN PANEL: STATISTIKA ----------------
    elif st.session_state.page == "admin":
        st.title("🔒 Admin panel — statistika")
        if not st.session_state.admin_logged_in:
            pwd = st.text_input("Admin parolini kiriting", type="password")
            if st.button("Kirish", type="primary", key="admin_login_btn"):
                if pwd == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Parol noto'g'ri.")
        else:
            data = load_data()
            users = data.get("users", {})
            st.metric("Jami ro'yxatdan o'tganlar", len(users))
            st.divider()
            for email, rec in users.items():
                with st.container(border=True):
                    st.markdown(f"**{rec['name']}** — {rec['email']}")
                    st.caption(f"📞 {rec['phone']}  ·  Ro'yxatdan o'tgan: {rec.get('royxatdan_otgan_sana', '—')}")
                    st.write(f"Arizalar: {len(rec.get('arizalar', []))}")
