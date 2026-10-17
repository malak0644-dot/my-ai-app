import os
import streamlit as st
from google import genai

st.title("🚀 مولد الإعلانات بالذكاء الاصطناعي")
st.write("أدخلي اسم منتجكِ للحصول على إعلان تسويقي جاهز!")

# قراءة المفتاح بأمان من Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ لم يتم العثور على المفتاح! تأكدي من إضافته في Streamlit Secrets.")
else:
    client = genai.Client(api_key=api_key)

    product_name = st.text_input("اسم المنتج", placeholder="مثال: حقيبة جلدية فاخرة")

    if st.button("توليد الإعلان ✨"):
        if product_name:
            with st.spinner("جاري كتابة الإعلان..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=f"اكتب إعلاناً تسويقياً جذاباً وقصيراً لمنصات التواصل الاجتماعي للمنتج التالي: {product_name}"
                    )
                    st.success("تم إنشاء الإعلان بنجاح!")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال: {e}")
        else:
            st.warning("الرجاء إدخال اسم المنتج أولاً!")
