import random
import time
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Boba Master - Tiệm Trà Sữa Siêu Tốc",
    page_icon="🧋",
    layout="wide",
)

# ----------------- TÙY CHỈNH CSS GIAO DIỆN CUTE & HOT HIT -----------------
st.markdown(
    """
    <style>
    .main {
        background-color: #faf6f0;
    }
    .stButton>button {
        background-color: #d2b48c;
        color: white;
        border-radius: 12px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #bc8f8f;
        color: white;
    }
    .menu-box {
        background-color: #fffaf0;
        padding: 15px;
        border-radius: 10px;
        border: 2px dashed #d2b48c;
        text-align: center;
        margin-bottom: 15px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ----------------- KHỞI TẠO TRẠNG THÁI GAME -----------------
if "money" not in st.session_state:
  st.session_state.money = 250
if "reputation" not in st.session_state:
  st.session_state.reputation = 15
if "day" not in st.session_state:
  st.session_state.day = 1

# Nguyên liệu kho
if "ingredients" not in st.session_state:
  st.session_state.ingredients = {
      "Trà đen": 12,
      "Sữa tươi": 12,
      "Trân châu đen": 10,
      "Thạch phô mai": 8,
      "Trái cây tươi": 8,
  }

# Nâng cấp cửa hàng
if "upgrades" not in st.session_state:
  st.session_state.upgrades = {
      "Máy ép nắp tự động": False,
      "Ly giữ nhiệt cao cấp": False,
      "Quảng cáo TikTok/Reels": False,
  }

if "current_customer" not in st.session_state:
  st.session_state.current_customer = None

if "customers_served" not in st.session_state:
  st.session_state.customers_served = 0
if "daily_revenue" not in st.session_state:
  st.session_state.daily_revenue = 0


# Hàm tạo khách hàng và order ngẫu nhiên
def generate_customer():
  names = [
      "Hà Anh",
      "Minh Quân",
      "Phương Linh",
      "Gia Hân",
      "Tuấn Khang",
      "Bảo Ngọc",
  ]
  bases = ["Trà sữa đường đen", "Hồng trà to cọc", "Trà trái cây tươi"]
  toppings = ["Trân châu đen", "Thạch phô mai", "Không topping"]

  chosen_base = random.choice(bases)
  chosen_topping = random.choice(toppings)

  # Định giá tiền dựa trên món
  base_price = 35 if "Trái cây" in chosen_base or "Đường đen" in chosen_base else 25
  if chosen_topping != "Không topping":
    base_price += 10
  if st.session_state.upgrades["Ly giữ nhiệt cao cấp"]:
    base_price += 10  # Bán giá cao hơn nhờ ly xịn

  st.session_state.current_customer = {
      "name": random.choice(names),
      "base": chosen_base,
      "topping": chosen_topping,
      "price": base_price,
  }


if st.session_state.current_customer is None:
  generate_customer()

# ----------------- TIÊU ĐỀ & BANNER GAME -----------------
st.title("🧋 BOBA MASTER - TIỆM TRÀ SỮA VIỆT NAM")
st.markdown(
    "*Pha chế cực nhanh - Phục vụ cực đỉnh - Trở thành ông chủ chuỗi trà sữa hot"
    " nhất phố!*"
)

# Hiển thị hình ảnh minh họa phong cách quán trà sữa hot hit (từ ảnh tham khảo)
st.image(
    "https://images.unsplash.com/photo-1541658016709-82535e94bc69?q=80&w=1200&auto=format&fit=crop",
    caption=(
        "Không gian quầy pha chế Boba Master nhộn nhịp khách ra vào mỗi ngày!"
    ),
    use_column_width=True,
)

# Bảng Menu quán trực quan
st.markdown(
    """
<div class="menu-box">
    <h3>📋 MENU HOT TREND HÔM NAY</h3>
    <p>🧋 <b>Trà Sữa Đường Đen</b> (Trà đen + Sữa tươi + Trân châu đen) | <i>Giá chuẩn: $35-45</i></p>
    <p>🥤 <b>Hồng Trà To Cọc</b> (Trà đen + Thạch phô mai) | <i>Giá chuẩn: $35</i></p>
    <p>🍓 <b>Trà Trái Cây Tươi</b> (Trái cây tươi + Trà đen) | <i>Giá chuẩn: $35</i></p>
</div>
""",
    unsafe_allow_html=True,
)

# Thanh chỉ số game (Metrics)
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("💰 Tiền vốn", f"${st.session_state.money}")
col_m2.metric("⭐ Danh vọng", f"{st.session_state.reputation} điểm")
col_m3.metric("📅 Ngày kinh doanh", f"Ngày {st.session_state.day}")
col_m4.metric("🥤 Đã bán hôm nay", f"{st.session_state.customers_served} ly")

st.divider()

# Chia giao diện thành 2 cột: Quầy pha chế (trái) và Kho / Nâng cấp (phải)
col_left, col_right = st.columns([1.2, 0.8])

with col_left:
  st.subheader("🧑‍🍳 Quầy Pha Chế & Order Khách Hàng")

  customer = st.session_state.current_customer
  if customer:
    st.info(
        f"🔔 **Khách hàng {customer['name']}** đang chờ gọi món:\n\n"
        f"👉 **Yêu cầu:** Món **{customer['base']}** + Topping:"
        f" **{customer['topping']}**\n"
        f"💵 **Tiền thưởng khi xong:** ${customer['price']}"
    )

    st.write("---")
    st.write("### 🛠️ Thao tác pha chế:")

    # Lựa chọn thành phần pha chế tương ứng với menu
    selected_base = st.selectbox(
        "Chọn loại nước nền / Trà:",
        [
            "-- Chọn loại --",
            "Trà sữa đường đen",
            "Hồng trà to cọc",
            "Trà trái cây tươi",
        ],
    )
    selected_topping = st.selectbox(
        "Chọn Topping đi kèm:",
        ["-- Chọn topping --", "Trân châu đen", "Thạch phô mai", "Không topping"],
    )

    if st.button("🚀 Giao ly trà sữa cho khách", use_container_width=True):
      # Kiểm tra thành phần cơ bản trong kho
      needed_ing = "Trà đen"
      if "Sữa" in customer["base"]:
        needed_ing = "Sữa tươi"
      elif "Trái cây" in customer["base"]:
        needed_ing = "Trái cây tươi"

      has_base = (
          selected_base != "-- Chọn loại --"
          and st.session_state.ingredients.get("Trà đen", 0) > 0
      )
      has_topping = True
      if selected_topping != "Không topping" and selected_topping != "-- Chọn --":
        has_topping = st.session_state.ingredients.get(selected_topping, 0) > 0

      if (
          selected_base == "-- Chọn loại --"
          or selected_topping == "-- Chọn --"
      ):
        st.warning("⚠️ Vui lòng chọn đầy đủ loại nước và topping theo order!")
      elif not has_base or not has_topping:
        st.error(
            "❌ Nguyên liệu trong kho đã cạn! Hãy sang mục **Nhập Kho** bên phải"
            " để mua thêm nguyên liệu."
        )
      else:
        # Đối chiếu công thức đơn hàng
        match_base = (
            (customer["base"] == "Trà sữa đường đen" and selected_base in ["Trà sữa đường đen", "Hồng trà to cọc"])
            or (customer["base"] == "Hồng trà to cọc" and selected_base in ["Hồng trà to cọc", "Trà sữa đường đen"])
            or (customer["base"] == "Trà trái cây tươi" and selected_base == "Trà trái cây tươi")
        )
        match_topping = selected_topping == customer["topping"]

        if match_base and match_topping:
          # Trừ nguyên liệu kho
          st.session_state.ingredients["Trà đen"] = max(
              0, st.session_state.ingredients["Trà đen"] - 1
          )
          if selected_topping != "Không topping":
            st.session_state.ingredients[selected_topping] = max(
                0, st.session_state.ingredients[selected_topping] - 1
            )

          earned = customer["price"]
          st.session_state.money += earned
          st.session_state.reputation += 3
          st.session_state.customers_served += 1
          st.session_state.daily_revenue += earned

          st.success(
              f"🎉 Xuất sắc! Khách hàng khen ngon hết lời và trả bạn"
              f" ${earned}."
          )
          time.sleep(0.4)
          st.session_state.current_customer = None
          st.rerun()
        else:
          st.session_state.reputation = max(
              0, st.session_state.reputation - 4
          )
          st.error(
              "❌ Pha sai công thức khiến khách hàng chê và bỏ đi! (-4 điểm danh"
              " vọng)"
          )
          st.session_state.current_customer = None
          time.sleep(0.4)
          st.rerun()

with col_right:
  st.subheader("📦 Kho Hàng & Nâng Cấp Quán")

  tab1, tab2 = st.tabs(["🛒 Nhập Nguyên Liệu", "⚙️ Nâng Cấp Cửa Hàng"])

  with tab1:
    st.write("Tình trạng kho nguyên liệu hiện tại:")
    for item, qty in st.session_state.ingredients.items():
      c1, c2 = st.columns([2, 1])
      c1.write(f"- {item}: **{qty}** phần")
      if c2.button(f"Mua (+5) [$12]", key=f"buy_ing_{item}"):
        if st.session_state.money >= 12:
          st.session_state.money -= 12
          st.session_state.ingredients[item] += 5
          st.success(f"Nhập thành công 5 {item}!")
          st.rerun()
        else:
          st.error("Không đủ tiền vốn!")

  with tab2:
    st.write("Đầu tư trang thiết bị để tối ưu hóa quán:")
    upgrades_cost = {
        "Máy ép nắp tự động": 120,
        "Ly giữ nhiệt cao cấp": 160,
        "Quảng cáo TikTok/Reels": 220,
    }

    for up_name, is_bought in st.session_state.upgrades.items():
      cost = upgrades_cost[up_name]
      if is_bought:
        st.success(f"✅ {up_name} (Đã sở hữu)")
      else:
        if st.button(f"Nâng cấp {up_name} (${cost})", key=f"upgrade_{up_name}"):
          if st.session_state.money >= cost:
            st.session_state.money -= cost
            st.session_state.upgrades[up_name] = True
            st.success(f"Đã kích hoạt nâng cấp {up_name} thành công!")
            st.rerun()
          else:
            st.error("Ví của bạn không đủ tiền để nâng cấp!")

  st.divider()
  if st.button("🌅 Chốt sổ & Kết thúc ngày kinh doanh", use_container_width=True):
    st.session_state.day += 1
    st.balloons()
    st.info(
        f"📊 **Báo cáo tổng kết ngày {st.session_state.day - 1}:**\n- Tổng số ly"
        f" đã bán: {st.session_state.customers_served}\n- Tổng doanh thu:"
        f" ${st.session_state.daily_revenue}"
    )
    st.session_state.customers_served = 0
    st.session_state.daily_revenue = 0
    st.rerun()
