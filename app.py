import random
import time
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Tiệm Trà Nhỏ - Boba Master", page_icon="🧋", layout="centered"
)

# ----------------- CSS GIAO DIỆN GAME STYLE XINH XẮN -----------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #faf6f0;
        color: #4a3b32;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Thanh trạng thái game */
    .game-header {
        background: linear-gradient(135deg, #ffb7b2, #ff9aa2);
        padding: 12px 20px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 16px;
        color: #fff;
        text-align: center;
        box-shadow: 0 4px 10px rgba(255, 183, 178, 0.4);
        margin-bottom: 15px;
    }
    /* Bong bóng order của khách */
    .customer-bubble {
        background-color: #ffffff;
        border: 3px solid #ffb7b2;
        padding: 16px;
        border-radius: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    /* Tiêu đề khu vực */
    .section-title {
        background-color: #b5838d;
        color: white;
        padding: 8px 15px;
        border-radius: 12px;
        font-size: 14px;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    /* Tùy chỉnh nút bấm */
    .stButton>button {
        background: linear-gradient(135deg, #e5989b, #b5838d);
        color: white;
        border-radius: 15px;
        font-weight: bold;
        border: none;
        padding: 12px 20px;
        width: 100%;
        box-shadow: 0 4px 10px rgba(181, 131, 141, 0.3);
        transition: 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #b5838d, #6d597a);
        color: white;
    }
    /* Khung selectbox và radio */
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 12px;
        border-color: #ffb7b2;
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
  customers = [
      "Bé Na 👧",
      "Minh Quân 👦",
      "Hà An 👩",
      "Gia Hân 🌸",
      "Tuấn Khải ☕",
  ]
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
    📅 Ngày {st.session_state.day} &nbsp;&nbsp;|&nbsp;&nbsp; 💰 {st.session_state.money:,.0f} đ &nbsp;&nbsp;|&nbsp;&nbsp; ⭐ {st.session_state.reputation} / 5.0
</div>
""",
    unsafe_allow_html=True,
)

# ----------------- 2. BONG BÓNG ORDER CỦA KHÁCH -----------------
st.markdown(
    f"""
<div class="customer-bubble">
    <h4 style="margin: 0 0 8px 0; color: #b5838d;">🗣️ Khách hàng: {cust['name']}</h4>
    <p style="font-size: 16px; margin: 0; line-height: 1.5;">💬 <i>"Cho tớ 1 ly <b>{cust['tea']}</b> size <b>{cust['size']}</b>, thêm <b>{cust['topping']}</b>, ngọt <b>{cust['sugar']}</b> và đá <b>{cust['ice']}</b> nhé!"</i></p>
</div>
""",
    unsafe_allow_html=True,
)

# ----------------- 3. KHU VỰC PHA CHẾ (VÒI TRÀ & SIZE) -----------------
st.markdown(
    '<div class="section-title">🧋 1. HỆ THỐNG VÒI TRÀ & CHỌN SIZE LY</div>',
    unsafe_allow_html=True,
)
col_t1, col_t2 = st.columns(2)
with col_t1:
  selected_tea = st.selectbox(
      "Chọn vòi trà cốt:",
      ["Trà sữa", "Matcha", "Hồng trà", "Lục trà", "Oolong"],
  )
with col_t2:
  selected_size = st.selectbox("Chọn kích thước ly:", ["Size M", "Size L"])

# ----------------- 4. KHAY TOPPING -----------------
st.markdown(
    '<div class="section-title">🍮 2. KHU VỰC KHAY TOPPING</div>',
    unsafe_allow_html=True,
)

selected_topping = st.radio(
    "Chọn loại topping cho vào ly:",
    [
        "Trân châu đen",
        "Trân châu hoàng kim",
        "Thạch phô mai",
        "Thạch trái cây",
        "Pudding trứng",
    ],
    horizontal=True,
)

# ----------------- 5. ĐƯỜNG & ĐÁ -----------------
st.markdown(
    '<div class="section-title">🥛 3. MỨC ĐƯỜNG & ĐÁ</div>',
    unsafe_allow_html=True,
)
col_s1, col_s2 = st.columns(2)
with col_s1:
  selected_sugar = st.selectbox(
      "Mức đường:", ["0% đường", "50% đường", "100% đường"]
  )
with col_s2:
  selected_ice = st.selectbox("Mức đá:", ["Không đá", "Ít đá", "Đá bình thường"])

st.write("")

# ----------------- 6. NÚT GIAO HÀNG -----------------
if st.button("🚀 HOÀN TẤT & GIAO LY TRÀ CHO KHÁCH"):
  if (
      selected_tea == cust["tea"]
      and selected_size == cust["size"]
      and selected_topping == cust["topping"]
      and selected_sugar == cust["sugar"]
      and selected_ice == cust["ice"]
  ):
    earned = cust["price"]
    st.session_state.money += earned
    st.success(
        f"🎉 Khách hàng uống rất ngon và thưởng cho quán {earned:,.0f}đ!"
    )
    time.sleep(0.5)
    st.session_state.current_customer = None
    st.rerun()
  else:
    st.error("❌ Pha chưa đúng ý khách rồi! Khách buồn phiền bỏ đi...")
    st.session_state.reputation = round(
        max(1.0, st.session_state.reputation - 0.1), 1
    )
    time.sleep(0.5)
    st.session_state.current_customer = None
    st.rerun()
