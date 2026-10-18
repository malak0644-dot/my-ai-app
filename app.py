import os
import streamlit as st
from google import genai

# إعدادات واجهة الصفحة
st.set_page_config(
    page_title="صانع الإعلانات الخرافي | AI Ad Generator PRO",
    page_icon="👑",
    layout="wide"
)

# قراءة المفتاح بأمان من Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

# إدارة حالة الاشتراك والتفعيل
if "is_pro" not in st.session_state:
    st.session_state.is_pro = False

# تفعيل ثيمات الألوان الحقيقية للواجهة بأكملها عبر CSS
if st.session_state.is_pro:
    # ألوان فاخرة وملونة وجذابة جداً للنسخة المدفوعة (Gradient Theme)
    st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
            color: #ffffff;
        }
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
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
            transition: all 0.3s ease !important;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0px 6px 25px rgba(236, 72, 153, 0.6) !important;
        }
        .pro-card {
            background: rgba(255, 255, 255, 0.07);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        .plan-badge {
            background: linear-gradient(90deg, #f59e0b, #ef4444);
            color: white;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    # ثيم عادي بون ألوان (أبيض وأسود ورمادي) للنسخة المجانية
    st.markdown("""
    <style>
        .main {
            background-color: #121212;
            color: #e0e0e0;
        }
        .stApp {
            background-color: #121212;
        }
        h1, h2, h3, h4, label, .stMarkdown {
            color: #b0b0b0 !important;
        }
        .stButton>button {
            background-color: #333333 !important;
            color: #ffffff !important;
            border: 1px solid #555555 !important;
            border-radius: 6px !important;
            font-size: 16px !important;
        }
        .free-card {
            background-color: #1e1e1e;
            border: 1px solid #333333;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# رأس الصفحة
col_title, col_status = st.columns([3, 1])
with col_title:
    st.title("👑 صانع الإعلانات الذكي العالمي")
    st.caption("التطبيق الأقوى والأجمل عالمياً لصنع المحتوى التسويقي بالذكاء الاصطناعي")

with col_status:
    if st.session_state.is_pro:
        st.markdown('<br><span class="plan-badge">✨ الحساب الفاخر PRO (نشط)</span>', unsafe_allow_html=True)
    else:
        st.markdown('<br><span style="background-color: #444; color: #fff; padding: 6px 12px; border-radius: 20px; font-size: 13px;">⚪ الخطة المجانية (أبيض وأسود)</span>', unsafe_allow_html=True)

st.markdown("---")

# القائمة الجانبية وعروض الاشتراكات
with st.sidebar:
    st.header("⚙️ لوحة التحكم والاشتراك")
    
    if not st.session_state.is_pro:
        st.error("🔒 أنتِ تستخدمين النسخة العادية (أبيض وأسود)")
        st.markdown("### 💳 باقات الاشتراك الفاخرة:")
        
        st.markdown("""
        <div style="background-color: #222; padding: 15px; border-radius: 10px; border: 1px solid #444; margin-bottom: 10px;">
            <h4 style="color: #60a5fa !important; margin:0;">🗓️ الاشتراك الأسبوعي</h4>
            <p style="font-size: 20px; font-weight: bold; margin: 5px 0; color: #fff !important;">$4.99 <span style="font-size:12px;">/ أسبوعياً</span></p>
            <p style="font-size: 12px; color: #aaa;">تجربة منخفضة التكلفة لجميع الخصائص والألوان!</p>
        </div>
        
        <div style="background-color: #2e1065; padding: 15px; border-radius: 10px; border: 1px solid #8b5cf6; margin-bottom: 10px;">
            <h4 style="color: #f472b6 !important; margin:0;">🔥 الاشتراك الشهري (الأكثر طلباً)</h4>
            <p style="font-size: 22px; font-weight: bold; margin: 5px 0; color: #fff !important;">$14.99 <span style="font-size:12px;">/ شهرياً</span></p>
            <p style="font-size: 12px; color: #ddd;">جدول محتوى شهري 30 يوم + الألوان الفاخرة كاملة!</p>
        </div>

        <div style="background-color: #064e3b; padding: 15px; border-radius: 10px; border: 1px solid #10b981; margin-bottom: 15px;">
            <h4 style="color: #34d399 !important; margin:0;">👑 الاشتراك السنوي (أعلى قيمة)</h4>
            <p style="font-size: 22px; font-weight: bold; margin: 5px 0; color: #fff !important;">$99.99 <span style="font-size:12px;">/ سنوياً</span></p>
            <p style="font-size: 12px; color: #ddd;">وفّري أكثر من 45% + دعم مباشر واستخدام غير محدود!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("[💳 الدفع عبر Visa / MasterCard / Apple Pay (Stripe)](https://stripe.com)")
        st.markdown("[🅿️ الدفع عبر PayPal](https://paypal.com)")
        
        st.markdown("---")
        activation_key = st.text_input("🔑 أدخلي رمز التفعيل بعد الدفع:", type="password")
        if st.button("تفعيل الاشتراك الفاخر 🚀"):
            if activation_key in ["PRO2026", "VIP100", "MALAK2026"]:
                st.session_state.is_pro = True
                st.success("تم تفعيل النسخة الاحترافية الفاخرة والألوان بنجاح! 🎉")
                st.rerun()
            else:
                st.error("رمز التفعيل غير صحيح! قم بالشراء أولاً للحصول عليه.")
    else:
        st.success("🎉 جميع الألوان والمميزات الفاخرة مفتوحة بالكامل!")
        if st.button("تسجيل الخروج من PRO"):
            st.session_state.is_pro = False
            st.rerun()

# النموذج الرئيسي للعمل
if not api_key:
    st.error("⚠️ لم يتم العثور على المفتاح! تأكدي من إضافته في Streamlit Secrets.")
else:
    client = genai.Client(api_key=api_key)

    card_class = "pro-card" if st.session_state.is_pro else "free-card"
    
    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
    st.subheader("🎯 إعدادات المحتوى والإعلان")
    
    product_name = st.text_input("اسم المنتج أو الخدمة", placeholder="مثال: مجموعتي الفاخرة للعناية بالبشرة")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.is_pro:
            platform = st.selectbox("📍 المنصة الفاخرة (PRO)", ["تيك توك (TikTok)", "إنستغرام (Instagram)", "سناب شات (Snapchat)", "إكس (X)", "فيسبوك (Facebook)"])
            tone = st.selectbox("🎭 النبرة التسويقية (PRO)", ["فاخر وراقي ✨", "حماسي ومشوق 🔥", "عاطفي ومقنع ❤️", "مرح وفكاهي 😄"])
        else:
            platform = "فيسبوك (Facebook)"
            tone = "عادي (أبيض وأسود)"
            st.info("💡 المنصات الفاخرة والنبرات المتعددة متاحة في اشتراك PRO")

    with col2:
        if st.session_state.is_pro:
            task_type = st.radio("✨ ميزات الذكاء الاصطناعي الفاخرة:", ["توليد إعلان احترافي + فكرة فيديو/صورة", "📅 جدول محتوى تسويقي ملون لمدة شهر كامل (30 يوم)"])
        else:
            task_type = "توليد إعلان احترافي"
            st.info("💡 جدول المحتوى الشهري 30 يوم متاح حصرياً للمشتركين")

    generate_btn = st.button("توليد المحتوى الآن ✨", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # المخرجات والنتائج
    if generate_btn:
        if product_name:
            with st.spinner("جاري الإبداع والتوليد بذكاء خيالي..."):
                try:
                    if st.session_state.is_pro and "جدول محتوى" in task_type:
                        prompt = f"""
                        قم بإنشاء خطة تسويقية وجدول محتوى شهري شامل ومكتمل لمدة 30 يوماً لمنتج: {product_name}.
                        المنصة المستهدفة: {platform}، والنبرة: {tone}.
                        نظم الجدول بتنسيق أنيق جداً وقسمه إلى 4 أسابيع مع أفكار منشورات يومية، هاشتاجات، ودعوات لاتخاذ إجراء (CTA).
                        """
                    else:
                        prompt = f"""
                        اكتب إعلاناً تسويقياً خرافياً ومحترفاً لـ: {product_name}.
                        المنصة: {platform}، النبرة: {tone}.
                        قدم أيضاً موجه بصري (Image Prompt بالإنجليزية) لتصميم صورة/فيديو الإعلان بالذكاء الاصطناعي.
                        """

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )

                    st.markdown("### 📋 النتيجة:")
                    if st.session_state.is_pro:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #1e1b4b 0%, #431407 100%); padding: 25px; border-radius: 16px; border: 2px solid #ec4899; box-shadow: 0 10px 30px rgba(236,72,153,0.3);">
                            <h3 style="color: #f472b6 !important;">💎 محتوى الخطة الاحترافية الفاخرة (PRO):</h3>
                            <hr style="border-color: #ec4899;">
                            {response.text}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.code(response.text, language="markdown")

                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال: {e}")
        else:
            st.warning("الرجاء إدخال اسم المنتج أو الخدمة أولاً!")
