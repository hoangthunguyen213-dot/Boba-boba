import random
import time
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Tiệm Trà Nhỏ - Boba Master", page_icon="🧋", layout="centered"
)

# ----------------- CSS GIAO DIỆN GAME MOBILE MÔ PHỎNG -----------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #fff8f0;
        color: #4a3b32;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .game-header {
        background: linear-gradient(135deg, #ff9aa2, #ffb7b2);
        padding: 10px 15px;
        border-radius: 16px;
        font-weight: bold;
        font-size: 15px;
        color: #fff;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 8px rgba(255, 154, 162, 0.3);
        margin-bottom: 12px;
    }
    .customer-bubble {
        background-color: #ffffff;
        border: 3px solid #ff9aa2;
        padding: 14px;
        border-radius: 18px;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .station-box {
        background-color: #fffaf5;
        border: 2px solid #e5989b;
        border-radius: 14px;
        padding: 12px;
        margin-bottom: 12px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.03);
    }
    .station-title {
        font-weight: bold;
        color: #b5838d;
        font-size: 14px;
        margin-bottom: 8px;
        text-transform: uppercase;
    }
    .stButton>button {
        background: linear-gradient(135deg, #e5989b, #b5838d);
        color: white;
        border-radius: 14px;
        font-weight: bold;
        border: none;
        padding: 12px 20px;
        width: 100%;
        box-shadow: 0 4px 10px rgba(181, 131, 141, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #b5838d, #6d597a);
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
  customers = ["Bé Na 👧", "Minh Quân 👦", "Hà An 👩", "Gia Hân 🌸", "Tuấn Khải ☕"]
  sizes = ["Size M", "Size L"]
  teas = ["Trà sữa", "Matcha", "Hồng trà", "Lục trà", "Oolong", "Trà thái"]

  # 12 loại topping tương ứng với 12 ô lưới trong ảnh
  toppings = [
      "Trân châu đen",
      "Thạch matcha",
      "Đá viên muối",
      "Pudding trứng",
      "Thạch trắng nhỏ",
      "Thạch trái cây hồng",
      "Thạch trái cây hỗn hợp",
      "Thạch đen",
      "Thạch cacao",
      "Trân châu hoàng kim",
      "Thạch phô mai",
      "Thạch dừa",
  ]
  foams = ["Không", "Foam cheese", "Foam matcha", "Foam muối", "Foam ube"]
  sugars = ["0% đường", "50% đường", "100% đường"]
  ices = ["Không đá", "Ít đá", "Đá bình thường"]

  st.session_state.current_customer = {
      "name": random.choice(customers),
      "size": random.choice(sizes),
      "tea": random.choice(teas),
      "topping": random.choice(toppings),
      "foam": random.choice(foams),
      "sugar": random.choice(sugars),
      "ice": random.choice(ices),
      "price": random.randint(45000, 75000),
  }


if st.session_state.current_customer is None:
  generate_order()

# ----------------- 1. THANH TRẠNG THÁI -----------------
cust = st.session_state.current_customer
st.markdown(
    f"""
<div class="game-header">
    <span>⏸️ &nbsp; 📅 Ngày {st.session_state.day} &nbsp; ⏱️ 11:10</span>
    <span>💰 {st.session_state.money:,.1f}k đ</span>
    <span>⭐ {st.session_state.reputation} (581 đánh giá)</span>
</div>
""",
    unsafe_allow_html=True,
)

# ----------------- 2. BONG BÓNG ORDER CỦA KHÁCH -----------------
st.markdown(
    f"""
<div class="customer-bubble">
    <h4 style="margin: 0 0 6px 0; color: #b5838d;">👧 {cust['name']} đang gọi món:</h4>
    <p style="font-size: 15px; margin: 0; line-height: 1.4;">💬 <i>"Ly 1: <b>{cust['tea']}</b> với <b>{cust['size']}</b>, thêm <b>{cust['topping']}</b>, lớp phủ <b>{cust['foam']}</b>, <b>{cust['sugar']}</b> và <b>{cust['ice']}</b> nhé!"</i></p>
    <div style="background-color: #f0f0f0; border-radius: 10px; height: 8px; width: 100%; margin-top: 10px;">
        <div style="background-color: #52b788; height: 8px; width: 75%; border-radius: 10px;"></div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ----------------- 3. TRẠM 1: VÒI TRÀ & CỐC -----------------
st.markdown(
    """
<div class="station-box">
    <div class="station-title">🧋 Trạm Quầy Trà & Chọn Cốc</div>
""",
    unsafe_allow_html=True,
)

col_v1, col_v2 = st.columns(2)
with col_v1:
  selected_tea = st.selectbox(
      "Chọn vòi trà:",
      ["Trà sữa", "Matcha", "Hồng trà", "Lục trà", "Oolong", "Trà thái"],
  )
with col_v2:
  selected_size = st.selectbox("Chọn kích thước ly:", ["Size M", "Size L"])

st.markdown("</div>", unsafe_allow_html=True)

# ----------------- 4. TRẠM 2: 12 Ô LƯỚI KHAY TOPPING -----------------
st.markdown(
    """
<div class="station-box">
    <div class="station-title">🍮 Trạm Khay Topping (12 Ô Lưới)</div>
""",
    unsafe_allow_html=True,
)

# Chia 12 ô topping thành 3 hàng (mỗi hàng 4 ô) cho trực quan y hệt game
t_col1, t_col2, t_col3, t_col4 = st.columns(4)

topping_options = [
    "Trân châu đen",
    "Thạch matcha",
    "Đá viên muối",
    "Pudding trứng",
    "Thạch trắng nhỏ",
    "Thạch trái cây hồng",
    "Thạch trái cây hỗn hợp",
    "Thạch đen",
    "Thạch cacao",
    "Trân châu hoàng kim",
    "Thạch phô mai",
    "Thạch dừa",
]

# Lưu lựa chọn topping qua radio/selectbox dạng lưới thu gọn
selected_topping = st.selectbox("Chọn topping từ 12 ô khay:", topping_options)

st.markdown("</div>", unsafe_allow_html=True)

# ----------------- 5. TRẠM 3: FOAM, ĐÁ & ĐƯỜNG -----------------
st.markdown(
    """
<div class="station-box">
    <div class="station-title">🥛 Trạm Foam, Đá & Đường</div>
""",
    unsafe_allow_html=True,
)

col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
  selected_foam = st.selectbox(
      "Lớp Foam:", ["Không", "Foam cheese", "Foam matcha", "Foam muối", "Foam ube"]
  )
with col_f2:
  selected_sugar = st.selectbox(
      "Mức đường:", ["0% đường", "50% đường", "100% đường"]
  )
with col_f3:
  selected_ice = st.selectbox("Mức đá:", ["Không đá", "Ít đá", "Đá bình thường"])

st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# ----------------- 6. NÚT GIAO TRÀ -----------------
if st.button("🚀 GIAO LY TRÀ CHO KHÁCH"):
  if (
      selected_tea == cust["tea"]
      and selected_size == cust["size"]
      and selected_topping == cust["topping"]
      and selected_foam == cust["foam"]
      and selected_sugar == cust["sugar"]
      and selected_ice == cust["ice"]
  ):
    earned = cust["price"]
    st.session_state.money += earned
    st.success(f"🎉 Khách rất hài lòng và thưởng cho quán {earned:,.0f} đ!")
    time.sleep(0.4)
    st.session_state.current_customer = None
    st.rerun()
  else:
    st.error(
        "❌ Pha chưa chuẩn công thức khách gọi rồi! Khách hàng trừ điểm uy"
        " tín..."
    )
    st.session_state.reputation = round(
        max(1.0, st.session_state.reputation - 0.1), 1
    )
    time.sleep(0.4)
    st.session_state.current_customer = None
    st.rerun()
