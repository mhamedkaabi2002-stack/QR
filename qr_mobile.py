import streamlit as st
import qrcode
import cv2
import numpy as np
from PIL import Image

# إعدادات الصفحة لتكون مناسبة لشاشة الموبايل
st.set_page_config(page_title="تطبيق QR الذكي", layout="centered")

# السطر المعدل والمصحح هنا لتجنب الخطأ السابق
st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>📱 تطبيق QR المتكامل للموبايل</h1>", unsafe_allow_html=True)
st.write("---")

# عمل تبويبين (Tabs) واحد للتوليد وواحد للقراءة العكسية
tab1, tab2 = st.tabs(["✨ توليد باركود جديد", "🔍 قراءة باركود من صورة"])

# --- التبويب الأول: توليد QR ---
with tab1:
    st.subheader("اكتب النص أو الرابط لتوليد الـ QR")
    text = st.text_input("أدخل الرابط هنا:", placeholder="https://example.com")
    
    if st.button("توليد الباركود الآن"):
        if text:
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(text)
            qr.make(fit=True)
            img = qr.make_image(fill_color="#1e3a8a", back_color="white")
            img.save("mobile_qr.png")
            
            # عرض النتيجة
            st.image("mobile_qr.png", caption="الباركود الخاص بك جاهز", width=250)
        else:
            st.warning("الرجاء كتابة شيء أولاً!")

# --- التبويب الثاني: قراءة QR (العكسي) ---
with tab2:
    st.subheader("ارفع صورة الباركود لمعرفة محتواها")
    
    # يتيح للمستخدم رفع صورة من الموبايل (سواء من الإستوديو أو الكاميرا)
    uploaded_file = st.file_uploader("اختر صورة الـ QR أو التقطها...", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        # عرض الصورة المرفوعة أمام المستخدم
        image = Image.open(uploaded_file)
        st.image(image, caption="الصورة التي تم رفعها", width=200)
        
        # معالجة الصورة باستخدام أداة OpenCV لقراءة محتواها
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)
        
        # تشغيل كاشف وقارئ الـ QR Code
        detector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = detector.detectAndDecode(opencv_image)
        
        st.write("---")
        if data:
            st.success("🎉 تم قراءة الباركود بنجاح!")
            st.markdown(f"النص أو الرابط المخفي داخل الباركود هو:")
            st.code(data, language="text") # يظهر النص بداخل صندوق منسق
        else:
            st.error("❌ لم نتمكن من قراءة الباركود. تأكد أن الصورة واضحة ومربعة بشكل صحيح.")