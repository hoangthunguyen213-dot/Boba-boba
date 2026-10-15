import random
import time
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Tiệm Trà Nhỏ - Game Quản Lý Chill",
    page_icon="🍵",
    layout="wide",
)

# ----------------- TÙY CHỈNH CSS ẤM CÚNG PHONG CÁCH GỖ & KEM -----------------
st.markdown(
    """
    <style>
    /* Nền kem ấm áp */
    .stApp {
        background-color: #f5ebe0;
        color: #4a3b32;
    }
    
    /* Nút bấm tông màu gỗ */
    .stButton>button {
        background-color: #8d5b4c;
        color: #ffffff;
        border-radius: 12px;
        font-weight: bold;
        border: none;
        padding: 8px 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #6a4035;
        color: #ffffff;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }

    /* Khung Bảng Đen Menu */
    .blackboard-menu {
        background-color: #2b2b2b;
        color: #f1f1f1;
        padding: 20px;
        border-radius: 16px;
        border: 8px solid #8d5b4c;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        font-family: 'Courier New', Courier, monospace;
        margin-bottom: 20px;
    }
    .blackboard-title {
        text-align: center;
        color: #f8c291;
        font-weight: bold;
        border-bottom: 2px dashed #f8c291;
        padding-bottom: 8px;
        margin-bottom: 15px;
    }
    .menu-item {
        font-size: 15px;
        margin-bottom: 8px;
    }

    /* Thẻ hóa đơn order của khách */
    .receipt-card {
        background-color: #ffffff;
        border: 2px dashed #8d5b4c;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ----------------- KHỞI TẠO TRẠNG THÁI GAME -----------------
if "money" not in st.session_state:
  st.session_state.money = 250
if "reputation" not in st.session_state:
  st.session_state.reputation = 20
if "day" not in st.session_state:
  st.session_state.day = 1

# Nguyên liệu pha chế (Cốt trà & Topping)
if "ingredients" not in st.session_state:
  st.session_state.ingredients = {
      "Trà ô long": 15,
      "Trà nhài": 15,
      "Sữa tươi": 15,
      "Đường đen": 12,
      "Hạt trân châu": 12,
      "Thạch trái cây": 10,
  }

# Trang trí & Nâng cấp tiệm
if "upgrades" not in st.session_state:
  st.session_state.upgrades = {
      "Bàn ghế gỗ mộc mạc": False,
      "Đèn LED neon Tiệm Trà Nhỏ": False,
      "Loa phát nhạc Lofi chill": False,
  }

if "current_customer" not in st.session_state:
  st.session_state.current_customer = None

if "customers_served" not in st.session_state:
  st.session_state.customers_served = 0
if "daily_revenue" not in st.session_state:
  st.session_state.daily_revenue = 0


# Hàm tạo khách hàng và món gọi ngẫu nhiên
def generate_customer():
  names = [
      "An Nhiên",
      "Minh Trí",
      "Thảo Nguyên",
      "Bảo An",
      "Đăng Khoa",
      "Hà My",
  ]
  menu_options = [
      {
          "drink": "TRÀ MỘC TRUYỀN THỐNG",
          "base": "Trà ô long",
          "topping": "Không topping",
          "price": 30,
      },
      {
          "drink": "TRÀ Ô LONG SỮA",
          "base": "Trà ô long",
          "topping": "Hạt trân châu",
          "price": 30,
      },
      {
          "drink": "TRÀ NHÀI THẠCH TRÁI CÂY",
          "base": "Trà nhài",
          "topping": "Thạch trái cây",
          "price": 30,
      },
      {
          "drink": "TRÀ SỮA ĐƯỜNG ĐEN",
          "base": "Trà ô long",
          "topping": "Đường đen",
          "price": 35,
      },
  ]

  chosen = random.choice(menu_options)
  price = chosen["price"]

  # Thưởng thêm tiền nếu đã nâng cấp không gian tiệm
  if st.session_state.upgrades["Bàn ghế gỗ mộc mạc"]:
    price += 5

  st.session_state.current_customer = {
      "name": random.choice(names),
      "drink": chosen["drink"],
      "base": chosen["base"],
      "topping": chosen["topping"],
      "price": price,
  }


if st.session_state.current_customer is None:
  generate_customer()

# ----------------- TIÊU ĐỀ & THANH CHỈ SỐ GIỐNG HÌNH MÔ PHỎNG -----------------
st.title("🍵 TIỆM TRÀ NHỎ")
st.markdown(
    "*Mùi thơm của trà, vị ngọt của sữa và góc quán gỗ nhỏ ấm cúng...*"
)

# Thanh hiển thị chỉ số (Metrics) giống hệt thanh trạng thái trong ảnh mô phỏng
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("💰 Ngân sách", f"${st.session_state.money}")
col_m2.metric("⭐ Điểm yêu thích", f"{st.session_state.reputation} điểm")
col_m3.metric("📅 Thời gian", f"Ngày thứ {st.session_state.day}")
col_m4.metric("🍵 Trà đã bán", f"{st.session_state.customers_served} ly")

st.divider()

# BẢNG ĐEN THỰC ĐƠN (MENU BANNER)
st.markdown(
    """
<div class="blackboard-menu">
    <div class="blackboard-title">📋 THỰC ĐƠN TIỆM TRÀ NHỎ ☕</div>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
        <div class="menu-item">🍃 <b>TRÀ MỘC TRUYỀN THỐNG</b><br>&nbsp;&nbsp;&nbsp;&nbsp;<i>Giá: $30 | Trà ô long</i></div>
        <div class="menu-item">🧋 <b>TRÀ Ô LONG SỮA</b><br>&nbsp;&nbsp;&nbsp;&nbsp;<i>Giá: $30 | Trà ô long + Hạt trân châu</i></div>
    </div>
    <br>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
        <div class="menu-item">🌸 <b>TRÀ NHÀI THẠCH TRÁI CÂY</b><br>&nbsp;&nbsp;&nbsp;&nbsp;<i>Giá: $30 | Trà nhài + Thạch trái cây</i></div>
        <div class="menu-item">🍮 <b>TRÀ SỮA ĐƯỜNG ĐEN</b><br>&nbsp;&nbsp;&nbsp;&nbsp;<i>Giá: $35 | Trà ô long + Đường đen</i></div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ----------------- GIAO DIỆN CHÍNH (QUẦY PHA CHẾ & KHO/NÂNG CẤP) -----------------
col_left, col_right = st.columns([1.2, 0.8])

with col_left:
  st.subheader("🧑‍🍳 Quầy Pha Chế Trực Tiếp")

  customer = st.session_state.current_customer
  if customer:
    st.markdown(
        f"""
        <div class="receipt-card">
            <h4>📜 HÓA ĐƠN ORDER - KHÁCH HÀNG: {customer['name'].upper()}</h4>
            <p>🧋 Món gọi: <b>{customer['drink']}</b></p>
            <p>📝 Yêu cầu công thức: <b>{customer['base']}</b> + <b>{customer['topping']}</b></p>
            <p>💵 Tiền thu về: <b>${customer['price']}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("---")
    st.write("### 🫖 Chọn nguyên liệu pha chế:")

    selected_base = st.selectbox(
        "1. Chọn Cốt Trà / Nước Nền:",
        ["-- Chọn cốt trà --", "Trà ô long", "Trà nhài"],
    )
    selected_topping = st.selectbox(
        "2. Chọn Topping Đi Kèm:",
        [
            "-- Chọn topping --",
            "Hạt trân châu",
            "Thạch trái cây",
            "Đường đen",
            "Không topping",
        ],
    )

    if st.button("🍵 Pha chế & Giao cho khách", use_container_width=True):
      if (
          selected_base == "-- Chọn cốt trà --"
          or selected_topping == "-- Chọn topping --"
      ):
        st.warning("⚠️ Cậu nhớ chọn đầy đủ cốt trà và topping cho vị khách nhé!")
      else:
        # Kiểm tra kho
        has_base = st.session_state.ingredients.get(selected_base, 0) > 0
        has_top = True
        if selected_topping != "Không topping":
          has_top = st.session_state.ingredients.get(selected_topping, 0) > 0

        if not has_base or not has_top:
          st.error(
              "❌ Tiệm hết nguyên liệu này rồi! Cậu sang mục Nhập Kho bên phải"
              " lấy thêm nha."
          )
        else:
          # Đối chiếu công thức
          if (
              selected_base == customer["base"]
              and selected_topping == customer["topping"]
          ):
            st.session_state.ingredients[selected_base] -= 1
            if selected_topping != "Không topping":
              st.session_state.ingredients[selected_topping] -= 1

            earned = customer["price"]
            st.session_state.money += earned
            st.session_state.reputation += 2
            st.session_state.customers_served += 1
            st.session_state.daily_revenue += earned

            st.success(
                f"🎉 {customer['name']} rất thích vị trà này và đã trả"
                f" ${earned}!"
            )
            time.sleep(0.4)
            st.session_state.current_customer = None
            st.rerun()
          else:
            st.session_state.reputation = max(
                0, st.session_state.reputation - 3
            )
            st.error(
                "❌ Pha sai vị trà rồi! Vị khách thất vọng ra về... (-3 điểm"
                " yêu thích)"
            )
            st.session_state.current_customer = None
            time.sleep(0.4)
            st.rerun()

with col_right:
  st.subheader("🏡 Căn Bếp & Trang Trí")

  tab1, tab2 = st.tabs(["🛒 Nhập Nguyên Liệu", "🪵 Nâng Cấp Tiệm Gỗ"])

  with tab1:
    st.write("Nguyên liệu còn trong kệ bếp:")
    for item, qty in st.session_state.ingredients.items():
      c1, c2 = st.columns([2, 1])
      c1.write(f"- {item}: **{qty}** phần")
      if c2.button(f"Lấy (+5) [$10]", key=f"ing_{item}"):
        if st.session_state.money >= 10:
          st.session_state.money -= 10
          st.session_state.ingredients[item] += 5
          st.success(f"Đã nhập 5 phần {item}!")
          st.rerun()
        else:
          st.error("Chưa đủ tiền nhập thêm!")

  with tab2:
    st.write("Sắm sửa để Tiệm Trà Nhỏ thêm lung linh:")
    upgrades_cost = {
        "Bàn ghế gỗ mộc mạc": 100,
        "Đèn LED neon Tiệm Trà Nhỏ": 150,
        "Loa phát nhạc Lofi chill": 200,
    }

    for up_name, is_bought in st.session_state.upgrades.items():
      cost = upgrades_cost[up_name]
      if is_bought:
        st.success(f"✅ {up_name} (Đã trang trí)")
      else:
        if st.button(f"Sắm {up_name} (${cost})", key=f"up_{up_name}"):
          if st.session_state.money >= cost:
            st.session_state.money -= cost
            st.session_state.upgrades[up_name] = True
            st.success(f"Đã trang trí {up_name} cho tiệm!")
            st.rerun()
          else:
            st.error("Chưa đủ tiền sắm đồ!")

  st.divider()
  if st.button("🌙 Khép cửa tiệm & Nghỉ ngơi", use_container_width=True):
    st.session_state.day += 1
    st.balloons()
    st.info(
        f"📊 **TỔNG KẾT NGÀY THỨ {st.session_state.day - 1}:**\n- Số ly trà đã"
        f" bán: {st.session_state.customers_served} ly\n- Doanh thu đạt được:"
        f" ${st.session_state.daily_revenue}"
    )
    st.session_state.customers_served = 0
    st.session_state.daily_revenue = 0
    st.rerun()
