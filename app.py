import random
import time
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Boba Master - Tiệm Trà Sữa Siêu Tốc",
    page_icon="🧋",
    layout="wide",
)

# ----------------- KHỞI TẠO TRẠNG THÁI GAME -----------------
if "money" not in st.session_state:
    st.session_state.money = 200  # Tiền vốn ban đầu
if "reputation" not in st.session_state:
    st.session_state.reputation = 10  # Điểm danh vọng
if "day" not in st.session_state:
    st.session_state.day = 1

# Nguyên liệu
if "ingredients" not in st.session_state:
    st.session_state.ingredients = {
        "Trà đen": 10,
        "Sữa tươi": 10,
        "Trân châu đen": 10,
        "Thạch phô mai": 5,
    }

# Nâng cấp
if "upgrades" not in st.session_state:
    st.session_state.upgrades = {
        "Máy pha trà tự động": False,
        "Ly giữ nhiệt cao cấp": False,
        "Quảng cáo mạng xã hội": False,
    }

# Khách hàng hiện tại
if "current_customer" not in st.session_state:
    st.session_state.current_customer = None

# Thống kê ngày
if "customers_served" not in st.session_state:
    st.session_state.customers_served = 0
if "daily_revenue" not in st.session_state:
    st.session_state.daily_revenue = 0


# Hàm tạo khách hàng mới
def generate_customer():
  names = ["Hà Anh", "Minh Quân", "Phương Linh", "Gia Hân", "Tuấn Khang"]
  toppings = ["Trân châu đen", "Thạch phô mai", "Không topping"]
  bases = ["Trà đen", "Sữa tươi"]

  chosen_base = random.choice(bases)
  chosen_topping = random.choice(toppings)

  # Giá tiền dựa trên order
  price = 30 if chosen_topping != "Không topping" else 20
  if st.session_state.upgrades["Ly giữ nhiệt cao cấp"]:
    price += 10  # Bán giá cao hơn nếu có ly xịn

  st.session_state.current_customer = {
      "name": random.choice(names),
      "base": chosen_base,
      "topping": chosen_topping,
      "price": price,
  }


if st.session_state.current_customer is None:
  generate_customer()

# ----------------- GIAO DIỆN CHÍNH -----------------
st.title("🧋 Boba Master - Tiệm Trà Sữa Đường Phố")
st.markdown(
    "Trở thành chủ quán trà sữa đỉnh cao, pha chế nhanh tay và làm hài lòng mọi"
    " thực khách!"
)

# Thanh hiển thị chỉ số (Metrics)
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("💰 Tiền vốn", f"${st.session_state.money}")
col_m2.metric("⭐ Danh vọng", f"{st.session_state.reputation} điểm")
col_m3.metric("📅 Ngày kinh doanh", f"Ngày {st.session_state.day}")
col_m4.metric("🥤 Đã bán hôm nay", f"{st.session_state.customers_served} ly")

st.divider()

# Chia giao diện thành 2 cột: Quầy pha chế (trái) và Quản lý / Kho hàng (phải)
col_left, col_right = st.columns([1.2, 0.8])

with col_left:
  st.subheader("🧑‍🍳 Quầy Pha Chế Trực Tuyến")

  customer = st.session_state.current_customer
  if customer:
    st.info(
        f"**Khách hàng:** {customer['name']} đang gọi món!\n\n"
        f"👉 **Yêu cầu:** Nền **{customer['base']}** + Topping:"
        f" **{customer['topping']}**\n"
        f"💵 **Tiền thưởng:** ${customer['price']}"
    )

    st.write("---")
    st.write("### Chọn nguyên liệu để pha:")

    # Chọn nguyên liệu pha chế
    selected_base = st.selectbox(
        "Chọn nước nền:", ["-- Chọn --", "Trà đen", "Sữa tươi"]
    )
    selected_topping = st.selectbox(
        "Chọn topping:",
        ["-- Chọn --", "Trân châu đen", "Thạch phô mai", "Không topping"],
    )

    if st.button("🚀 Phục vụ ly trà sữa", type="primary", use_container_width=True):
      # Kiểm tra nguyên liệu
      has_base = (
          selected_base != "-- Chọn --"
          and st.session_state.ingredients.get(selected_base, 0) > 0
      )
      has_topping = True
      if selected_topping != "Không topping" and selected_topping != "-- Chọn --":
        has_topping = st.session_state.ingredients.get(selected_topping, 0) > 0

      if selected_base == "-- Chọn --" or selected_topping == "-- Chọn --":
        st.warning("⚠️ Vui lòng chọn đủ nước nền và topping!")
      elif not has_base or not has_topping:
        st.error(
            "❌ Nguyên liệu trong kho đã hết! Hãy vào mục **Kho hàng** để nhập"
            " thêm."
        )
      else:
        # Kiểm tra đúng order hay không
        if (
            selected_base == customer["base"]
            and selected_topping == customer["topping"]
        ):
          # Trừ nguyên liệu
          st.session_state.ingredients[selected_base] -= 1
          if selected_topping != "Không topping":
            st.session_state.ingredients[selected_topping] -= 1

          # Thưởng tiền và danh vọng
          earned = customer["price"]
          st.session_state.money += earned
          st.session_state.reputation += 2
          st.session_state.customers_served += 1
          st.session_state.daily_revenue += earned

          st.success(
              f"🎉 Thành công! Khách hàng rất hài lòng và trả bạn ${earned}."
          )
          time.sleep(0.5)
          st.session_state.current_customer = None
          st.rerun()
        else:
          st.session_state.reputation = max(
              0, st.session_state.reputation - 3
          )
          st.error(
              "❌ Pha sai công thức khiến khách hàng tức giận bỏ đi! (-3 điểm"
              " danh vọng)"
          )
          st.session_state.current_customer = None
          time.sleep(0.5)
          st.rerun()

with col_right:
  st.subheader("📦 Kho Hàng & Nâng Cấp")

  tab1, tab2 = st.tabs(["🛒 Nhập Kho", "⚙️ Nâng Cấp Quán"])

  with tab1:
    st.write("Quản lý nguyên liệu hiện tại:")
    for item, qty in st.session_state.ingredients.items():
      c1, c2 = st.columns([2, 1])
      c1.write(f"- {item}: **{qty}**")
      if c2.button(f"Nhập (+5) [$10]", key=f"buy_{item}"):
        if st.session_state.money >= 10:
          st.session_state.money -= 10
          st.session_state.ingredients[item] += 5
          st.success(f"Đã nhập thêm 5 {item}!")
          st.rerun()
        else:
          st.error("Không đủ tiền!")

  with tab2:
    st.write("Nâng cấp trang thiết bị để tăng giá trị và thu hút:")

    upgrades_cost = {
        "Máy pha trà tự động": 100,
        "Ly giữ nhiệt cao cấp": 150,
        "Quảng cáo mạng xã hội": 200,
    }

    for up_name, is_bought in st.session_state.upgrades.items():
      cost = upgrades_cost[up_name]
      if is_bought:
        st.success(f"✅ {up_name} (Đã sở hữu)")
      else:
        if st.button(f"Mua {up_name} (${cost})", key=f"up_{up_name}"):
          if st.session_state.money >= cost:
            st.session_state.money -= cost
            st.session_state.upgrades[up_name] = True
            st.success(f"Nâng cấp thành công {up_name}!")
            st.rerun()
          else:
            st.error("Không đủ tiền để nâng cấp!")

  st.divider()
  if st.button("🌅 Kết thúc ngày kinh doanh", use_container_width=True):
    st.session_state.day += 1
    st.balloons()
    st.info(
        f"📊 Tổng kết ngày {st.session_state.day - 1}:\n- Đã bán:"
        f" {st.session_state.customers_served} ly\n- Doanh thu:"
        f" ${st.session_state.daily_revenue}"
    )
    st.session_state.customers_served = 0
    st.session_state.daily_revenue = 0
    st.rerun()
