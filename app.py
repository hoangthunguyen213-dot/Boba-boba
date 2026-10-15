import random
import time
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Tiệm Trà Nhỏ - Boba Game", page_icon="🧋", layout="centered"
)

# ----------------- CSS GIAO DIỆN GAME MOBILE -----------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #fff9f4;
        color: #4a3b32;
    }
    .game-header {
        background-color: #ffb7b2;
        padding: 10px 15px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 15px;
        box-shadow: 0 3px 5px rgba(0,0,0,0.06);
        margin-bottom: 12px;
        text-align: center;
    }
    .customer-bubble {
        background-color: #ffffff;
        border: 3px solid #ffb7b2;
        padding: 14px;
        border-radius: 14px;
        margin-bottom: 15px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.05);
    }
    .section-title {
        background-color: #e5989b;
        color: white;
        padding: 5px 10px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
        margin-top: 12px;
        margin-bottom: 8px;
    }
    .stButton>button {
        background-color: #e5989b;
        color: white;
        border-radius: 10px;
        font-weight: bold;
        border: none;
        padding: 10px 15px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #b5838d;
        color: white;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ----------------- KHỞI TẠO TRẠNG THÁI GAME -----------------
if "money" not in st.session_state:
  st.session_state.money = 856800
if "day" not in st.session_state:
  st.session_state.day = 28
if "reputation" not in st.session_state:
  st.session_state.reputation = 4.7
if "current_customer" not in st.session_state:
  st.session_state.current_customer = None


# Hàm tạo đơn order ngẫu nhiên
def generate_order():
  customers = ["Bé Na", "Minh Quân", "Hà An", "Gia Hân", "Tuấn Khải"]
  sizes = ["Size M", "Size L"]
  teas = ["Trà sữa", "Matcha", "Hồng trà", "Lục trà", "Oolong"]
  toppings = [
      "Trân châu đen",
      "Trân châu hoàng kim",
      "Thạch phô mai",
      "Thạch trái cây",
      "Pudding trứng",
  ]
  sugars = ["0% đường", "50% đường", "100% đường"]
  ices = ["Không đá", "Ít đá", "Đá bình thường"]

  st.session_state.current_customer = {
      "name": random.choice(customers),
      "size": random.choice(sizes),
      "tea": random.choice(teas),
      "topping": random.choice(toppings),
      "sugar": random.choice(sugars),
      "ice": random.choice(ices),
      "price": random.randint(35000, 60000),
  }


if st.session_state.current_customer is None:
  generate_order()

# ----------------- 1. THANH TRẠNG THÁI -----------------
cust = st.session_state.current_customer
st.markdown(
    f"""
<div class="game-header">
    📅 Ngày {st.session_state.day} &nbsp;|&nbsp; 💰 {st.session_state.money:,.0f} đ &nbsp;|&nbsp; ⭐ {st.session_state.reputation}
</div>
""",
    unsafe_allow_html=True,
)

# ----------------- 2. BONG BÓNG ORDER -----------------
st.markdown(
    f"""
<div class="customer-bubble">
    <h4 style="margin: 0 0 6px 0; color: #b5838d;">👧 Khách hàng: {cust['name']}</h4>
    <p style="font-size: 15px; margin: 0;">💬 <i>"Cho tớ 1 ly <b>{cust['tea']}</b> với <b>{cust['size']}</b>, thêm <b>{cust['topping']}</b>, <b>{cust['sugar']}</b> và <b>{cust['ice']}</b> nhé!"</i></p>
</div>
""",
    unsafe_allow_html=True,
)

# ----------------- 3. KHU VỰC PHA CHẾ -----------------
st.markdown(
    '<div class="section-title">🧋 1. CHỌN VÒI TRÀ & SIZE</div>',
    unsafe_allow_html=True,
)
selected_tea = st.selectbox(
    "Vòi trà:", ["Trà sữa", "Matcha", "Hồng trà", "Lục trà", "Oolong"]
)
selected_size = st.selectbox("Kích thước ly:", ["Size M", "Size L"])

st.markdown(
    '<div class="section-title">🍮 2. CHỌN TOPPING</div>',
    unsafe_allow_html=True,
)
selected_topping = st.selectbox(
    "Topping:",
    [
        "Trân châu đen",
        "Trân châu hoàng kim",
        "Thạch phô mai",
        "Thạch trái cây",
        "Pudding trứng",
    ],
)

st.markdown(
    '<div class="section-title">🥛 3. ĐƯỜNG & ĐÁ</div>',
    unsafe_allow_html=True,
)
selected_sugar = st.selectbox(
    "Mức đường:", ["0% đường", "50% đường", "100% đường"]
)
selected_ice = st.selectbox("Mức đá:", ["Không đá", "Ít đá", "Đá bình thường"])

st.write("")

# ----------------- 4. NÚT GIAO HÀNG -----------------
if st.button("🚀 HOÀN TẤT & GIAO LY TRÀ"):
  if (
      selected_tea == cust["tea"]
      and selected_size == cust["size"]
      and selected_topping == cust["topping"]
      and selected_sugar == cust["sugar"]
      and selected_ice == cust["ice"]
  ):
    earned = cust["price"]
    st.session_state.money += earned
    st.success(f"🎉 Khách rất thích và thưởng cho quán {earned:,.0f}đ!")
    time.sleep(0.5)
    st.session_state.current_customer = None
    st.rerun()
  else:
    st.error("❌ Pha chưa đúng ý khách rồi! Khách bỏ đi...")
    st.session_state.reputation = round(
        max(1.0, st.session_state.reputation - 0.1), 1
    )
    time.sleep(0.5)
    st.session_state.current_customer = None
    st.rerun()
