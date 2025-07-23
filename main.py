import streamlit as st
import random
from PIL import Image, ImageDraw

# 캔버스 크기 및 자동차/장애물 설정
canvas_width = 400
canvas_height = 600
car_width = 50
car_height = 80
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 10

st.set_page_config(layout="wide")

# 세션 초기화
if "car_x" not in st.session_state:
    st.session_state.car_x = canvas_width // 2 - car_width // 2

if "obstacles" not in st.session_state:
    st.session_state.obstacles = []

# 장애물 생성
def create_obstacle():
    x = random.randint(0, canvas_width - obstacle_width)
    y = -obstacle_height
    return [x, y]

# 장애물 이동
def move_obstacles():
    new_obs = []
    for x, y in st.session_state.obstacles:
        y += obstacle_speed
        if y < canvas_height:
            new_obs.append([x, y])
    st.session_state.obstacles = new_obs

# 충돌 판정
def check_collision():
    car_rect = [st.session_state.car_x, canvas_height - car_height,
                st.session_state.car_x + car_width, canvas_height]
    for ox, oy in st.session_state.obstacles:
        obstacle_rect = [ox, oy, ox + obstacle_width, oy + obstacle_height]
        if not (car_rect[2] < obstacle_rect[0] or car_rect[0] > obstacle_rect[2] or
                car_rect[3] < obstacle_rect[1] or car_rect[1] > obstacle_rect[3]):
            return True
    return False

# 마우스 위치 받기 (JavaScript -> Streamlit)
st.markdown("""
    <script>
    const doc = window.parent.document;
    doc.addEventListener('mousemove', (e) => {
        const x = e.clientX;
        const width = window.innerWidth;
        const relativeX = Math.floor((x / width) * 400); // 400: canvas width
        const input = doc.querySelector('input[data-testid="cursor-x"]');
        if (input) {
            input.value = relativeX;
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
    });
    </script>
""", unsafe_allow_html=True)

cursor_x = st.number_input("마우스X", min_value=0, max_value=canvas_width, key="cursor-x", label_visibility="collapsed")

# 자동차 위치 업데이트
st.session_state.car_x = max(0, min(canvas_width - car_width, cursor_x - car_width // 2))

# 장애물 생성 및 이동
if random.random() < 0.1:  # 확률적으로 생성
    st.session_state.obstacles.append(create_obstacle())

move_obstacles()
crash = check_collision()

# 이미지 그리기
img = Image.new("RGB", (canvas_width, canvas_height), color="white")
draw = ImageDraw.Draw(img)

# 자동차 그리기
draw.rectangle([st.session_state.car_x,
                canvas_height - car_height,
                st.session_state.car_x + car_width,
                canvas_height],
               fill="blue")

# 장애물 그리기
for ox, oy in st.session_state.obstacles:
    draw.rectangle([ox, oy, ox + obstacle_width, oy + obstacle_height], fill="red")

st.image(img, caption="장애물을 피하세요!", use_column_width=False)

# 충돌시 메시지
if crash:
    st.error("💥 충돌! 게임 오버!")

# 자동 새로고침 (게임 루프)
st.experimental_rerun()
