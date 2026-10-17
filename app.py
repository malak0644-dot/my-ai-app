import os
import streamlit as st
from google import genai

# ضبط المفتاح
os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6IeKeTT3-ouWau1VUUcpcLj2LDNHCGosbW6LBocI8Ks6w"
client = genai.Client()

st.title("🚀 مولد الإعلانات بالذكاء الاصطناعي")
st.write("أدخلي اسم منتجكِ للحصول على إعلان تسويقي جاهز!")

product_name = st.text_input("اسم المنتج", placeholder="مثال: حقيبة جلدية فاخرة")

if st.button("توليد الإعلان ✨"):
    if product_name:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=f"اكتب إعلاناً تسويقياً جذاباً وقصيراً لمنصات التواصل الاجتماعي للمنتج التالي: {product_name}",
        )
        st.success("تم توليد الإعلان بنجاح!")
        st.write(response.text)
    else:
        st.warning("رجاءً أدخلي اسم المنتج أولاً.")
