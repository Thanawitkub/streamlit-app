
import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.datasets import load_iris

# -------------------------------------------------------------------
# ตั้งค่าหน้าเว็บให้กว้างขึ้น (Wide mode) เหมาะสำหรับ Dashboard
st.set_page_config(page_title="Iris Species Dashboard", page_icon="🌸", layout="wide")

# 1. โหลดข้อมูลและโมเดล
@st.cache_resource
def load_data_and_model():
    model = joblib.load('iris_model.pkl') 
    target_names = ['Setosa', 'Versicolor', 'Virginica']
    
    # โหลดข้อมูล Iris ดั้งเดิมมาเพื่อหา "ค่าเฉลี่ย" เอาไปทำกราฟเปรียบเทียบ
    iris = load_iris()
    dataset_means = iris.data.mean(axis=0) 
    
    return model, target_names, dataset_means

model, target_names, dataset_means = load_data_and_model()
feature_names = ['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']

# -------------------------------------------------------------------
# ตกแต่งด้วย CSS เพื่อทำกล่องแสดงผลลัพธ์สวยๆ
st.markdown("""
<style>
    .predict-box {
        padding: 20px; 
        border-radius: 15px; 
        text-align: center; 
        color: white; 
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .species-text { font-size: 40px; font-weight: bold; margin: 0; padding: 10px 0;}
    .conf-text { font-size: 18px; opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# 2. สร้าง Sidebar สำหรับรับค่า
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/869/869045.png", width=100)
st.sidebar.title("⚙️ Input Features")
st.sidebar.write("ปรับค่าขนาดของดอกไม้เพื่อดูผลลัพธ์แบบ Real-time")

sepal_length = st.sidebar.slider('Sepal Length (cm)', 4.0, 8.0, 5.8)
sepal_width = st.sidebar.slider('Sepal Width (cm)', 2.0, 4.5, 3.0)
petal_length = st.sidebar.slider('Petal Length (cm)', 1.0, 7.0, 4.3)
petal_width = st.sidebar.slider('Petal Width (cm)', 0.1, 2.5, 1.3)

user_inputs = [sepal_length, sepal_width, petal_length, petal_width]

# -------------------------------------------------------------------
# 3. เตรียมข้อมูลและทำนายผล
input_array = np.array([user_inputs])
prediction = model.predict(input_array)[0]
# ใช้ predict_proba เพื่อหาความน่าจะเป็น (เปอร์เซ็นต์ความมั่นใจ) ของทุกคลาส
probabilities = model.predict_proba(input_array)[0] 

predicted_species = target_names[prediction]
confidence = probabilities[prediction] * 100

# กำหนดสีของกล่องผลลัพธ์ตามสายพันธุ์ที่ทายได้ (Gradient colors)
bg_colors = {
    'Setosa': 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)', # ชมพูพาสเทล
    'Versicolor': 'linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)', # ม่วงพาสเทล
    'Virginica': 'linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)' # ฟ้าเขียวพาสเทล
}
box_color = bg_colors[predicted_species]

# -------------------------------------------------------------------
# 4. ออกแบบ Main Layout ของ Dashboard (แบ่งเป็น 2 คอลัมน์)
st.title("🌸 Iris Flower Species Predictor Pro")
st.write("Dashboard วิเคราะห์และจำแนกสายพันธุ์ดอกไอริสด้วย Machine Learning")
st.markdown("---")

col1, col2 = st.columns([1, 1.5]) # แบ่งสัดส่วนคอลัมน์ซ้ายแคบกว่าขวานิดหน่อย

with col1:
    st.subheader("🎯 Prediction Result")
    # แสดงกล่องผลลัพธ์ที่ตกแต่งด้วย CSS
    st.markdown(f"""
        <div class="predict-box" style="background: {box_color}; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">
            <div>Predicted Species</div>
            <div class="species-text">{predicted_species}</div>
            <div class="conf-text">Confidence: {confidence:.2f}%</div>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("📊 Probability Distribution")
    # กราฟแท่งแสดงความน่าจะเป็นของแต่ละสายพันธุ์
    fig_prob = go.Figure(data=[
        go.Bar(x=target_names, y=probabilities * 100, 
               text=[f"{p*100:.1f}%" for p in probabilities], textposition='auto',
               marker_color=['#ff9a9e', '#a18cd1', '#84fab0'])
    ])
    fig_prob.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=300, 
                           yaxis=dict(title='Probability (%)', range=[0, 100]))
    st.plotly_chart(fig_prob, use_container_width=True)

with col2:
    st.subheader("📈 Your Input vs Dataset Average")
    # กราฟแท่งเปรียบเทียบข้อมูลที่กรอก กับค่าเฉลี่ยของข้อมูลดั้งเดิม
    fig_compare = go.Figure(data=[
        go.Bar(name='Your Input', x=feature_names, y=user_inputs, marker_color='#ff4b4b'),
        go.Bar(name='Dataset Mean', x=feature_names, y=dataset_means, marker_color='#e0e0e0')
    ])
    fig_compare.update_layout(barmode='group', margin=dict(l=0, r=0, t=30, b=0), height=500,
                              yaxis=dict(title='Centimeters (cm)'),
                              legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_compare, use_container_width=True)