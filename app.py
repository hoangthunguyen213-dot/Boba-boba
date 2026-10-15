import random
import time
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Tiệm Trà Nhỏ - Quản Lý Tiệm Trà",
    page_icon="🍵",
    layout="wide",
)

# ----------------- GIAO DIỆN CSS MÔ PHỎNG QUÁN GỖ ẤM CÚNG -----------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f7f3ed;
        color: #4a3b32;
    }
    .stButton>button {
        background-color: #8b5a2b;
        color: white;
        border-radius: 10px;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #6b4226;
        color: white;
    }
    /* Khung hiển thị trực quan quầy Bar */
    .bar-section {
        background-color: #fffaf0;
        border: 3px solid #b5835a;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    }
    .blackboard {
        background-color: #2b2b2b;
        color: #f8f8f2;
        padding: 15px;
        border-radius: 12px;
        border: 5px solid #d4a373;
        font-family: 'Courier New', Courier, monospace;
    }
    .order-ticket {
        background-color: #ffffff;
        border: 2px dashed #8b5a2b;
        padding: 15px;
        border-radius: 10px;
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

if "ingredients" not in st.session_state:
  st.session_state.ingredients = {
      "Trà ô long": 15,
      "Trà nhài": 15,
      "Hồng trà to cọc": 15,
      "Sữa tươi": 15,
      "Hạt trân châu": 12,
      "Thạch trái cây": 12,
  }

if "upgrades" not in st.session_state:
  st.session_state.upgrades = {
      "Bàn ghế gỗ mộc mạc": False,
      "Đèn vàng ấm áp trang trí": False,
      "Loa phát nhạc Lofi": False,
  }

if "current_customer" not in st.session_state:
  st.session_state.current_customer = None

if "customers_served" not in st.session_state:
  st.session_state.customers_served = 0
if "daily_revenue" not in st.session_state:
  st.session_state.daily_revenue = 0


# Hàm tạo khách hàng và order
def create_new_customer():
  names = ["An Nhiên", "Minh Trí", "Thảo Nguyên", "Bảo An", "Đăng Khoa", "Hà My"]
  recipes = [
      {
          "drink": "Trà Mộc Truyền Thống",
          "base": "Trà ô long",
          "topping": "Không topping",
          "price": 25,
      },
      {
          "drink": "Trà Ô Long Sữa",
          "base": "Trà ô long",
          "topping": "Hạt trân châu",
          "price": 35,
      },
      {
          "drink": "Trà Nhài Thạch",
          "base": "Trà nhài",
          "topping": "Thạch trái cây",
          "price": 25,
      },
      {
          "drink": "Trân Trái Cây Tươi",
          "base": "Hồng trà to cọc",
          "topping": "Thạch trái cây",
          "price": 55,
      },
  ]

  chosen = random.choice(recipes)
  price = chosen["price"]

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
  create_new_customer()

# ----------------- TIÊU ĐỀ & CHỈ SỐ QUẢN LÝ -----------------
st.title("🍵 TIỆM TRÀ NHỎ - GÓC QUẦY PHA CHẾ & ORDER")
st.markdown(
    "*Mô phỏng không gian pha chế rộn ràng, khách hàng xếp hàng order và nhân"
    " viên lắc trà sữa!*"
)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("💰 Ngân sách", f"${st.session_state.money}")
col_m2.metric("⭐ Điểm yêu thích", f"{st.session_state.reputation}")
col_m3.metric("📅 Thời gian", f"Ngày {st.session_state.day}")
col_m4.metric("🍵 Trà đã bán", f"{st.session_state.customers_served} ly")

st.divider()

# ----------------- MÔ PHỎNG KHU VỰC QUẦY (VISUAL BAR LAYOUT) -----------------
st.markdown("### 🖼️ Không Gian Quầy Tiệm Trà Nhỏ")
col_visual1, col_visual2 = st.columns(2)

with col_visual1:
  st.markdown(
      """
    <div class="bar-section">
        <h4 style="color: #8b5a2b; margin-top: 0;">🧑‍🍳 1. Khu Vực Quầy Pha Chế</h4>
        <p>✨ <b>Nhân viên đang lắc Shaker & Máy ép ly:</b> Sẵn sàng pha các món trà thơm ngon từ kệ hũ đựng nguyên liệu (Trà ô long, Hồng trà to cọc, Sữa tươi, Thạch, Trân châu).</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

with col_visual2:
  st.markdown(
      """
    <div class="bar-section">
        <h4 style="color: #8b5a2b; margin-top: 0;">📋 2. Khu Vực Order & Khách Hàng</h4>
        <p>👋 <b>Khách đang xếp hàng & Nhân viên ghi order:</b> Khách hàng xem thực đơn trên bảng đen, gọi món và chờ nhận những ly trà sữa chuẩn vị.</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

# BẢNG ĐEN THỰC ĐƠN TRỰC QUAN
st.markdown(
    """
<div class="blackboard">
    <h3 style="text-align: center; color: #f8c291; margin-top: 0;">📋 THỰC ĐƠN BẢNG ĐEN TIỆM TRÀ NHỎ</h3>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
        <div>🍃 <b>Trà Mộc Truyền Thống</b> ($25)<br>&nbsp;&nbsp;&nbsp;&nbsp;<i>Cốt: Trà ô long</i></div>
        <div>🧋 <b>Trà Ô Long Sữa</b> ($35)<br>&nbsp;&nbsp;&nbsp;&nbsp;<i>Cốt: Trà ô long + Hạt trân châu</i></div>
    </div>
    <br>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
        <div>🌸 <b>Trà Nhài Thạch</b> ($25)<br>&nbsp;&nbsp;&nbsp;&nbsp;<i>Cốt: Trà nhài + Thạch trái cây</i></div>
        <div>🍓 <b>Trân Trái Cây Tươi</b> ($55)<br>&nbsp;&nbsp;&nbsp;&nbsp;<i>Cốt: Hồng trà to cọc + Thạch trái cây</i></div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.write("")

# ----------------- TƯƠNG TÁC GAME CHÍNH -----------------
left_col, right_col = st.columns([1.2, 0.8])

with left_col:
  st.subheader("🥤 Thao Tác Tại Quầy Pha Chế")

  customer = st.session_state.current_customer
  if customer:
    st.markdown(
        f"""
        <div class="order-ticket">
            <h4>🔔 Khách hàng đang đứng chờ: <b>{customer['name']}</b></h4>
            <p>👉 <b>Món yêu cầu:</b> {customer['drink']}</p>
            <p>📝 <i>Công thức chuẩn từ bảng:</i> Cốt trà: <b>{customer['base']}</b> | Topping: <b>{customer['topping']}</b></p>
            <p>💵 <b>Tiền thưởng thanh toán:</b> ${customer['price']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.write("### 🫖 Tiến hành pha chế:")

    selected_base = st.selectbox(
        "Chọn Cốt Trà / Nước Nền:",
        [
            "-- Chọn cốt trà --",
            "Trà ô long",
            "Trà nhài",
            "Hồng trà to cọc",
            "Sữa tươi",
        ],
    )
    selected_topping = st.selectbox(
        "Chọn Topping:",
        [
            "-- Chọn topping --",
            "Hạt trân châu",
            "Thạch trái cây",
            "Không topping",
        ],
    )

    if st.button(
        "✨ Lắc shaker & Giao ly trà cho khách", use_container_width=True
    ):
      if (
          selected_base == "-- Chọn cốt trà --"
          or selected_topping == "-- Chọn topping --"
      ):
        st.warning(
            "⚠️ Cậu hãy chọn đầy đủ cốt trà và topping theo đúng order của khách"
            " nhé!"
        )
      else:
        # Kiểm tra nguyên liệu trong kho
        has_base = st.session_state.ingredients.get(selected_base, 0) > 0
        has_top = True
        if selected_topping != "Không topping":
          has_top = st.session_state.ingredients.get(selected_topping, 0) > 0

        if not has_base or not has_top:
          st.error(
              "❌ Nguyên liệu trong kho đã cạn! Cậu hãy sang mục Nhập Kho bên"
              " phải để lấy thêm."
          )
        else:
          # Kiểm tra đúng công thức khách gọi
          if (
              selected_base == customer["base"]
              and selected_topping == customer["topping"]
          ):
            # Trừ nguyên liệu
            st.session_state.ingredients[selected_base] -= 1
            if selected_topping != "Không topping":
              st.session_state.ingredients[selected_topping] -= 1

            # Cộng thưởng
            earned = customer["price"]
            st.session_state.money += earned
            st.session_state.reputation += 2
            st.session_state.customers_served += 1
            st.session_state.daily_revenue += earned

            st.success(
                f"🎉 Pha chế hoàn hảo! Khách hàng uống rất ngon và trả"
                f" ${earned}."
            )
            time.sleep(0.3)
            st.session_state.current_customer = None
            st.rerun()
          else:
            st.session_state.reputation = max(
                0, st.session_state.reputation - 3
            )
            st.error(
                "❌ Pha nhộn nhạo sai công thức khiến khách hàng thất vọng bỏ"
                " đi! (-3 điểm yêu thích)"
            )
            time.sleep(0.3)
            st.session_state.current_customer = None
            st.rerun()

with right_col:
  st.subheader("📦 Kho Hàng & Nâng Cấp Tiệm")

  tab1, tab2 = st.tabs(["🛒 Nhập Nguyên Liệu", "🪵 Trang Trí Tiệm"])

  with tab1:
    st.write("Kệ đựng nguyên liệu trong quầy:")
    for item, count in st.session_state.ingredients.items():
      col_i1, col_i2 = st.columns([2, 1])
      col_i1.write(f"- {item}: **{count}** phần")
      if col_i2.button(f"Mua (+5) [$10]", key=f"buy_{item}"):
        if st.session_state.money >= 10:
          st.session_state.money -= 10
          st.session_state.ingredients[item] += 5
          st.success(f"Nhập thành công 5 phần {item}!")
          st.rerun()
        else:
          st.error("Ngân sách không đủ để nhập kho!")

  with tab2:
    st.write("Nâng cấp không gian tiệm trà:")
    upgrade_list = {
        "Bàn ghế gỗ mộc mạc": 100,
        "Đèn vàng ấm áp trang trí": 150,
        "Loa phát nhạc Lofi": 200,
    }

    for up_name, is_unlocked in st.session_state.upgrades.items():
      cost = upgrade_list[up_name]
      if is_unlocked:
        st.success(f"✅ {up_name} (Đã trang bị)")
      else:
        if st.button(f"Sắm {up_name} (${cost})", key=f"up_{up_name}"):
          if st.session_state.money >= cost:
            st.session_state.money -= cost
            st.session_state.upgrades[up_name] = True
            st.success(f"Đã trang bị {up_name} thành công!")
            st.rerun()
          else:
            st.error("Ví tiền không đủ để mua món này!")

  st.divider()
  if st.button("🌙 Kết thúc ngày kinh doanh", use_container_width=True):
    st.session_state.day += 1
    st.balloons()
    st.info(
        f"📊 **Báo cáo Ngày {st.session_state.day - 1}:**\n- Số ly trà đã bán:"
        f" {st.session_state.customers_served} ly\n- Tổng doanh thu:"
        f" ${st.session_state.daily_revenue}"
    )
    st.session_state.customers_served = 0
    st.session_state.daily_revenue = 0
    st.rerun()
