import os
import streamlit as st
from google import genai

# إعدادات واجهة الصفحة العالمية
st.set_page_config(
    page_title="Global Ultimate AI Ad Generator",
    page_icon="🌍",
    layout="wide"
)

# إدارة حالة الاشتراك والتفعيل
if "is_pro" not in st.session_state:
    st.session_state.is_pro = False

# تطبيق الألوان الفاخرة للنسخة المدفوعة والرمادية للمجانية
if st.session_state.is_pro:
    st.markdown("""
    <style>
        .main, .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
            color: #ffffff;
        }
        h1, h2, h3, h4, label, .stMarkdown {
            color: #ffffff !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .stButton>button {
            background: linear-gradient(90deg, #ec4899 0%, #8b5cf6 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 12px !important;
            font-size: 18px !important;
            font-weight: bold !important;
            padding: 12px 24px !important;
            box-shadow: 0px 4px 20px rgba(236, 72, 153, 0.4) !important;
        }
        .pro-card {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .main, .stApp {
            background-color: #121212;
            color: #e0e0e0;
        }
        h1, h2, h3, h4, label, .stMarkdown {
            color: #b0b0b0 !important;
        }
        .stButton>button {
            background-color: #333333 !important;
            color: #ffffff !important;
            border-radius: 6px !important;
            border: 1px solid #555555 !important;
        }
        .free-card {
            background-color: #1e1e1e;
            border: 1px solid #333333;
            border-radius: 8px;
            padding: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# قراءة مفتاح API بأمان
api_key = st.secrets.get("GEMINI_API_KEY")

# القائمة الجانبية المتقدمة
with st.sidebar:
    st.header("⚙️ Control Panel / لوحة التحكم")
    
    # قائمة لغات العالم الشاملة
    selected_language = st.selectbox(
        "🌐 Choose Output Language / اختر لغة الإعلان:",
        [
            "العربية (Arabic)",
            "English",
            "Français (French)",
            "Español (Spanish)",
            "Deutsch (German)",
            "Türkçe (Turkish)",
            "Italiano (Italian)",
            "Português (Portuguese)",
            "Русский (Russian)",
            "中文 (Chinese)",
            "日本語 (Japanese)",
            "한국어 (Korean)",
            "हिन्दी (Hindi)",
            "Urdu (أوردو)",
            "أي لغة أخرى... (Custom Language)"
        ]
    )
    
    if selected_language == "أي لغة أخرى... (Custom Language)":
        custom_lang = st.text_input("اكتبي اسم اللغة المطلوبة (e.g. Swahili, Dutch):", value="English")
        target_lang = custom_lang
    else:
        target_lang = selected_language.split(" (")[0]

    st.markdown("---")
    
    # نظام الاشتراكات المباشر المطور
    if not st.session_state.is_pro:
        st.info("⚪ الخطة العادية (أبيض وأسود)")
        st.markdown("### 💳 باقات الاشتراك الفاخرة:")
        
        st.markdown("""
        * 🗓️ **الاشتراك الأسبوعي:** $4.99
        * 🔥 **الاشتراك الشهري:** $14.99
        * 👑 **الاشتراك السنوي:** $99.99
        """)
        
        # زر تفعيل مباشر فور الشراء ودون رموز
        if st.button("🚀 تفعيل اشتراك PRO الفاخر فوراً"):
            st.session_state.is_pro = True
            st.success("تم تفعيل النسخة الاحترافية الفاخرة والألوان بجمالية خرافية! 🎉")
            st.rerun()
    else:
        st.success("✨ اشتراك PRO نشط (جميع اللغات والألوان مجانية)")
        if st.button("الرجوع للخطة المجانية"):
            st.session_state.is_pro = False
            st.rerun()

# رأس الصفحة الرئيسية
st.title("🌍 صانع الإعلانات العالمي بالذكاء الاصطناعي")
st.caption(f"إنشاء إعلانات تسويقية خرافية بجميع لغات العالم | اللغة الحالية: {target_lang}")
st.markdown("---")

if not api_key:
    st.error("⚠️ لم يتم العثور على المفتاح! تأكدي من إضافته في Streamlit Secrets.")
else:
    client = genai.Client(api_key=api_key)
    
    card_class = "pro-card" if st.session_state.is_pro else "free-card"
    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
    
    product_name = st.text_input("اسم المنتج أو الخدمة", placeholder="مثال: ساعة يد ذكية / Smart Watch / Montre Connectée")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.is_pro:
            platform = st.selectbox("📍 منصة النشر", ["تيك توك (TikTok)", "إنستغرام (Instagram)", "سناب شات (Snapchat)", "إكس (X)", "فيسبوك (Facebook)"])
        else:
            platform = "فيسبوك (Facebook)"
            st.info("💡 المنصات الفاخرة متاحة في اشتراك PRO")

    with col2:
        if st.session_state.is_pro:
            tone = st.selectbox("🎭 النبرة التسويقية", ["فاخر وراقي ✨", "حماسي ومشوق 🔥", "عاطفي ومقنع ❤️", "مرح وفكاهي 😄"])
        else:
            tone = "Standard"
            st.info("💡 النبرات المتقدمة متاحة في اشتراك PRO")

    generate_btn = st.button("توليد الإعلان الخرافي ✨", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if generate_btn:
        if product_name:
            with st.spinner("جاري صياغة المحتوى بأعلى مستوى من الاحترافية..."):
                try:
                    prompt = f"""
                    You are a world-class digital marketing expert and advertising copywriter.
                    Write a highly persuasive, high-converting marketing ad for the product: {product_name}.
                    
                    CRITICAL INSTRUCTION:
                    The entire generated response MUST be written in the following language: {target_lang}.
                    
                    Platform: {platform}
                    Tone: {tone}
                    
                    Include:
                    1. Attention-grabbing headline/hook.
                    2. Engaging body text highlighting benefits.
                    3. Relevant emojis and hashtags.
                    4. Strong Call to Action (CTA).
                    5. Image/Video Prompt (in English) for AI design creation.
                    """

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )

                    st.markdown("### 📋 النتيجة الاحترافية:")
                    if st.session_state.is_pro:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #1e1b4b 0%, #431407 100%); padding: 25px; border-radius: 16px; border: 2px solid #ec4899; box-shadow: 0 10px 30px rgba(236,72,153,0.3);">
                            {response.text}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.code(response.text, language="markdown")

                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال: {e}")
        else:
            st.warning("الرجاء إدخال اسم المنتج أو الخدمة أولاً!")
