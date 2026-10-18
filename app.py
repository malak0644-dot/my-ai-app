import os
import streamlit as st
from google import genai

# إعدادات واجهة الصفحة
st.set_page_config(
    page_title="صانع الإعلانات الذكي | Pro & Free",
    page_icon="🚀",
    layout="wide"
)

# تخصيص التصميم والأنماط بناءً على الخطة
st.markdown("""
<style>
    .stButton>button {
        border-radius: 8px;
        font-weight: bold;
    }
    .pro-badge {
        background-color: #FFD700;
        color: #000;
        padding: 4px 8px;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 صانع الإعلانات التسويقية بالذكاء الاصطناعي")

# قراءة المفتاح من Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ لم يتم العثور على المفتاح! تأكدي من إضافته في Streamlit Secrets.")
else:
    client = genai.Client(api_key=api_key)

    # الشريط الجانبي باختيار الخطة
    with st.sidebar:
        st.header("💳 نوع الاشتراك")
        plan = st.radio(
            "اختر خطتك الحاليّة:",
            ["⚪ الخطة المجانية (Free)", "👑 الخطة الاحترافية (PRO) - $19/شهر"]
        )

        st.markdown("---")

        if "PRO" in plan:
            st.success("✨ أنتِ تستخدمين النسخة الذهبية الفاخرة!")
            theme_color = st.color_picker("🎨 اختر لون الواجهة المفضل لديك (PRO)", "#6C5CE7")
            platform = st.selectbox(
                "📍 منصة النشر (PRO)",
                ["إنستغرام (Instagram)", "تيك توك (TikTok)", "سناب شات (Snapchat)", "فيسبوك (Facebook)", "إكس (X)"]
            )
            tone = st.selectbox(
                "🎭 النبرة التسويقية (PRO)",
                ["حماسي ومشوق 🔥", "فاخر وراقي ✨", "عاطفي ودافئ ❤️", "مرح وفكاهي 😄", "مقنع وعملي 💡"]
            )
            feature_type = st.radio(
                "🎯 الميزة المطلوبة:",
                ["توليد إعلان مخصص", "📅 توليد جدول محتوى تسويقي لمدة شهر (30 يوم)"]
            )
        else:
            st.info("ℹ️ أنتِ على الخطة العادية (أبيض وأسود). اشتركي للحصول على الألوان والجدول الشهر!")
            platform = "فيسبوك (Facebook)"
            tone = "عادي"
            feature_type = "توليد إعلان مخصص"

    # المنطقة الرئيسية للتطبيق
    st.subheader("📝 بيانات المنتج")
    product_name = st.text_input("اسم المنتج أو الخدمة", placeholder="مثال: عطر نسائي فاخر")
    
    if "PRO" in plan:
        product_desc = st.text_area("تفاصيل المنتج الإضافية (متاحة في PRO)", placeholder="اذكري الروائح، السعر، العروض...")
    else:
        product_desc = ""

    generate_btn = st.button("توليد المحتوى ✨", type="primary")

    st.markdown("---")

    if generate_btn:
        if product_name:
            with st.spinner("جاري صياغة المحتوى..."):
                try:
                    if "PRO" in plan and feature_type == "📅 توليد جدول محتوى تسويقي لمدة شهر (30 يوم)":
                        prompt = f"""
                        أنت خبير تسويق رقمي. قم بإنشاء خطة تسويقية وجدول محتوى لمدة 4 أسابيع للمنتج: {product_name}.
                        لكل أسبوع، قدم 3 أفكار إعلانية مخصصة لمنصة {platform} بنبرة {tone}.
                        اجعل الخطة مكتوبة بشكل ملون ومرح ومنظم بجدول.
                        """
                    else:
                        prompt = f"""
                        اكتب إعلاناً تسويقياً للمنتج: {product_name}.
                        المنصة: {platform}.
                        النبرة: {tone}.
                        التفاصيل: {product_desc if product_desc else 'لا يوجد'}.
                        """

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )

                    st.success("تم التوليد بنجاح!")

                    # عرض النتيجة بتصميم مجاني (أبيض وأسود) أو مدفوع (ملون)
                    if "PRO" in plan:
                        st.markdown(f"""
                        <div style="background-color: {theme_color}; color: white; padding: 20px; border-radius: 12px; font-size: 18px;">
                            <h3 style="color: white;">🌟 النتيجة الاحترافية الفاخرة (PRO):</h3>
                            {response.text}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.code(response.text, language="markdown")

                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال: {e}")
        else:
            st.warning("الرجاء إدخال اسم المنتج أولاً!")
