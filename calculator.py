import streamlit as st

# กำหนดชื่อแอป
st.title("เครื่องคิดเลขอย่างง่าย 🧮")

# สร้างช่องกรอกตัวเลข 2 ช่อง
num1 = st.number_input("ใส่ตัวเลขที่ 1", value=0.0)
num2 = st.number_input("ใส่ตัวเลขที่ 2", value=0.0)

# สร้างเมนู Dropdown สำหรับเลือกเครื่องหมายทางคณิตศาสตร์
operation = st.selectbox("เลือกการคำนวณ", ["บวก (+)", "ลบ (-)", "คูณ (x)", "หาร (/)"])

# สร้างปุ่มสำหรับกดคำนวณ
if st.button("คำนวณ"):
    if operation == "บวก (+)":
        result = num1 + num2
        st.success(f"ผลลัพธ์: {num1} + {num2} = {result}")
        
    elif operation == "ลบ (-)":
        result = num1 - num2
        st.success(f"ผลลัพธ์: {num1} - {num2} = {result}")
        
    elif operation == "คูณ (x)":
        result = num1 * num2
        st.success(f"ผลลัพธ์: {num1} x {num2} = {result}")
        
    elif operation == "หาร (/)":
        if num2 != 0:
            result = num1 / num2
            st.success(f"ผลลัพธ์: {num1} / {num2} = {result}")
        else:
            # ดักจับข้อผิดพลาดกรณีตัวหารเป็น 0
            st.error("ไม่สามารถหารด้วย 0 ได้ กรุณาเปลี่ยนตัวเลขที่ 2")