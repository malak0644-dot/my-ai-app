import os
import streamlit as st
from google import genai

# إعدادات واجهة الصفحة
st.set_page_config(
    page_title="المولد الذكي للإعلانات احترافية",
    page_icon="🚀",
    layout="wide"
)

# عنوان التطبيق وتصميمه
st.title("🚀 صانع الإعلانات التسويقية بالذكاء الاصطناعي")
st.markdown("---")

# قراءة المفتاح بأمان من Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ لم يتم العثور على المفتاح! تأكدي من إضافته في Streamlit Secrets.")
else:
    client = genai.Client(api_key=api_key)

    # القائمة الجانبية للخيارات المتقدمة
    with st.sidebar:
        st.header("⚙️ إعدادات الإعلان")
        
        platform = st.selectbox(
            "📍 منصة النشر",
            ["إنستغرام (Instagram)", "تيك توك (TikTok)", "فيسبوك (Facebook)", "إكس / تويتر (X)", "سناب شات (Snapchat)"]
        )
        
        tone = st.selectbox(
            "ش النبرة التسويقية",
            ["حماسي ومشوق 🔥", "فاخر وراقي ✨", "مقنع وعملي 💡", "عاطفي ودافئ ❤️", "مرح وفكاهي 😄"]
        )
        
        target_audience = st.selectbox(
            "👥 الجمهور المستهدف",
            ["الجميع", "الشباب واليافعين", "النساء", "الرجال", "أصحاب الأعمال والمستثمرين", "الأمهات والعائلات"]
        )

        offer_type = st.selectbox(
            "🎁 نوع العرض / الهدف",
            ["بدون عرض خاص", "خصم لفترة محدودة", "شحن مجاني", "منتج جديد حصري", "اشتري واحد واحصل على الثاني مجاناً"]
        )

        ad_length = st.select_slider(
            "📏 طول الإعلان",
            options=["قصير جداً", "متوسط", "مفصل وشامل"]
        )

    # المنطقة الرئيسية للتطبيق
    col_input, col_result = st.columns([1, 1], gap="large")

    with col_input:
        st.subheader("📝 تفاصيل المنتج")
        product_name = st.text_input("اسم المنتج أو الخدمة", placeholder="مثال: ساعة يد ذكية فاخرة")
        product_description = st.text_area(
            "وصف أو مميزات المنتج (اختياري)",
            placeholder="مثال: مقاومة للماء، بطارية تدوم 7 أيام، تتبع نبضات القلب والرياضة...",
            height=120
        )
        
        generate_btn = st.button("توليد الإعلان والأفكار البصرية ✨", type="primary", use_container_width=True)

    with col_result:
        st.subheader("🎯 النتيجة الاحترافية")
        if generate_btn:
            if product_name:
                with st.spinner("جاري صياغة المحتوى التسويقي والأفكار البصرية..."):
                    try:
                        prompt = f"""
                        أنت خبير تسويق إلكتروني وصانع محتوى إعلاني محترف. 
                        قم بكتابة إعلان تسويقي مميز جداً بناءً على المعطيات التالية:
                        - اسم المنتج: {product_name}
                        - تفاصيل إضافية: {product_description if product_description else 'لا يوجد'}
                        - المنصة: {platform}
                        - نبرة الصوت: {tone}
                        - الجمهور المستهدف: {target_audience}
                        - نوع العرض/الهدف: {offer_type}
                        - طول النص المطلوب: {ad_length}

                        المطلوب منك تقديم الإجابة بالشكل التالي:
                        1. **نص الإعلان الإبداعي** (مع استخدام الإيموجيات والهاشتاجات المناسبة ودعوة لاتخاذ إجراء CTA).
                        2. **فكرة التصميم/الفيديو المقترحة (Image/Video Prompt)**: وصف باللغة الإنجليزية لإنشاء صورة أو فيديو إعلاني يناسب هذا الإعلان بواسطة الذكاء الاصطناعي.
                        """

                        response = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=prompt
                        )

                        st.success("تم التوليد بنجاح! 🎉")
                        st.markdown(response.text)

                    except Exception as e:
                        st.error(f"حدث خطأ أثناء الاتصال: {e}")
            else:
                st.warning("الرجاء إدخال اسم المنتج أو الخدمة أولاً!")
