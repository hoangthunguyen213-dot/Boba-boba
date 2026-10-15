 import random
import time
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Tiệm Trà Nhỏ - Boba Game Style", page_icon="🧋", layout="wide"
)

# ----------------- TÙY CHỈNH CSS GIAO DIỆN GAME MOBILE -----------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #fff9f4;
        color: #4a3b32;
    }
    .game-header {
        background-color: #ffb7b2;
        padding: 12px 20px;
        border-radius: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.08);
        margin-bottom: 15px;
    }
    .customer-bubble {
        background-color: #ffffff;
        border: 3px solid #ffb7b2;
        padding: 16px;
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.06);
    }
    .section-title {
        background-color: #e5989b;
        color: white;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    .stButton>button {
        background-color: #e5989b;
        color: white;
        border-radius: 12px;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
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
  st.session_state.money = 856800  # 856,8k như trong game
if "day" not in st.session_state:
  st.session_state.day = 28
if "reputation" not in st.session_state:
  st.session_state.reputation = 4.7
if "customers_served" not in st.session_state:
  st.session_state.customers_served = 142

if "current_customer" not in st.session_state:
  st.session_state.current_customer = None


# Hàm tạo khách hàng và order ngẫu nhiên chuẩn game
def generate_order():
  customers = ["Bé Na", "Minh Quân", "Hà An", "Gia Hân", "Tuấn Khải", "Phương Linh"]
  sizes = ["Size M", "Size L"]
  teas = ["Trà sữa", "Matcha", "Hồng trà", "Lục trà", "Oolong", "Trà hoa"]
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
      "price": random.randint(35000, 65000),
  }


if st.session_state.current_customer is None:
  generate_order()

# ----------------- 1. THANH TRẠNG THÁI TRÊN CÙNG (HEADER) -----------------
st.markdown(
    f"""
<div class="game-header">
    <span>📅 Ngày {st.session_state.day}</span>
    <span>💰 {st.session_state.money:,.0f} đ</span>
    <span>⭐ {st.session_state.reputation} (581 đánh giá)</span>
</div>
""",
    unsafe_allow_html=True,
)

# ----------------- 2. BONG BÓNG ORDER CỦA KHÁCH HÀNG -----------------
cust = st.session_state.current_customer
st.markdown(
    f"""
<div class="customer-bubble">
    <h4 style="margin: 0 0 8px 0; color: #b5838d;">👧 Khách hàng: {cust['name']}</h4>
    <p style="font-size: 16px; margin: 0;">💬 <i>"Cho tớ 1 ly <b>{cust['tea']}</b> với <b>{cust['size']}</b>, thêm <b>{cust['topping']}</b>, <b>{cust['sugar']}</b> và <b>{cust['ice']}</b> nhé!"</i></p>
</div>
""",
    unsafe_allow_html=True,
)

st.divider()

# ----------------- 3. QUẦY TRÀ & CHỌN SIZE -----------------
st.markdown(
    '<div class="section-title">🧋 1. QUẦY TRÀ & CHỌN SIZE LY</div>',
    unsafe_allow_html=True,
)

col_tea, col_size = st.columns([2, 1])

with col_tea:
  selected_tea = st.selectbox(
      "Chọn vòi trà (Hệ thống vòi rót):",
      ["Trà sữa", "Matcha", "Hồng trà", "Lục trà", "Oolong", "Trà hoa"],
  )

with col_size:
  selected_size = st.selectbox("Chọn kích thước ly:", ["Size M", "Size L"])

# ----------------- 4. KHAY TOPPING (LƯỚI CHỌN TOPPING) -----------------
st.markdown(
    '<div class="section-title">🍮 2. KHAY TOPPING (CHỌN TOPPING)</div>',
    unsafe_allow_html=True,
)

selected_topping = st.selectbox(
    "Chọn Topping:",
    [
        "Trân châu đen",
        "Trân châu hoàng kim",
        "Trân châu trắng",
        "Thạch trái cây",
        "Thạch phô mai",
        "Thạch matcha",
        "Thạch dừa",
        "Pudding trứng",
        "Hạt nổ cam",
        "Hạt nổ việt quất",
        "Sương sáo",
        "Đậu đỏ",
    ],
)

# ----------------- 5. ĐƯỜNG, ĐÁ & FOAM -----------------
st.markdown(
    '<div class="section-title">🥛 3. ĐƯỜNG, ĐÁ & FOAM</div>',
    unsafe_allow_html=True,
)

col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
  selected_sugar = st.selectbox(
      "Mức đường:", ["0% đường", "50% đường", "100% đường"]
  )
with col_f2:
  selected_ice = st.selectbox("Mức đá:", ["Không đá", "Ít đá", "Đá bình thường"])
with col_f3:
  selected_foam = st.selectbox(
      "Lớp phủ / Foam:", ["Không", "Foam matcha", "Kem cheese"]
  )

st.write("")

# ----------------- 6. NÚT HOÀN TẤT & GIAO HÀNG -----------------
if st.button("🚀 HOÀN TẤT & GIAO LY TRÀ CHO KHÁCH", use_container_width=True):
  # Kiểm tra độ chính xác so với đơn order của khách
  if (
      selected_tea == cust["tea"]
      and selected_size == cust["size"]
      and selected_topping == cust["topping"]
      and selected_sugar == cust["sugar"]
      and selected_ice == cust["ice"]
  ):
    earned = cust["price"]
    st.session_state.money += earned
    st.session_state.customers_served += 1
    st.success(
        f"🎉 Tuyệt vời! Khách hàng uống rất ngon và thưởng cho quán"
        f" {earned:,.0f}đ!"
    )
    time.sleep(0.4)
    st.session_state.current_customer = None
    st.rerun()
  else:
    st.error(
        "❌ Pha chưa đúng ý khách rồi! Khách hàng không hài lòng và bỏ đi... (-0.1"
        " sao uy tín)"
    )
    st.session_state.reputation = round(
        max(1.0, st.session_state.reputation - 0.1), 1
    )
    time.sleep(0.4)
    st.session_state.current_customer = None
    st.rerun()
