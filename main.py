
import streamlit as st
from PIL import Image, ImageDraw

# 캔버스 설정
canvas_width = 500
canvas_height = 500
car_width = 40
car_height = 70
move_step = 20

# 초기 위치 설정
if "x" not in st.session_state:
    st.session_state.x = canvas_width // 2 - car_width // 2
if "y" not in st.session_state:
    st.session_state.y = canvas_height - car_height - 10

# 자동차 이동
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("⬅️ 왼쪽"):
        st.session_state.x = max(0, st.session_state.x - move_step)
with col2:
    if st.button("⬆️ 위쪽"):
        st.session_state.y = max(0, st.session_state.y - move_step)
with col3:
    if st.button("➡️ 오른쪽"):
        st.session_state.x = min(canvas_width - car_width, st.session_state.x + move_step)

col4, _, col5 = st.columns([1, 1, 1])
with col4:
    if st.button("⬇️ 아래쪽"):
        st.session_state.y = min(canvas_height - car_height, st.session_state.y + move_step)
with col5:
    if st.button("🔄 초기화"):
        st.session_state.x = canvas_width // 2 - car_width // 2
        st.session_state.y = canvas_height - car_height - 10

# 자동차 그리기
img = Image.new("RGB", (canvas_width, canvas_height), color="lightgray")
draw = ImageDraw.Draw(img)
draw.rectangle(
    [st.session_state.x, st.session_state.y,
     st.session_state.x + car_width, st.session_state.y + car_height],
    fill="blue"
)

st.image(img, caption="자동차를 움직여보세요!", use_column_width=False)
