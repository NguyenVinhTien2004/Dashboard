import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd
import json

# Đọc dữ liệu
df = pd.read_csv("kf_coffee.csv")

# Hàm xử lý
def total_sold_from_history(stock_history_str):
    try:
        history = json.loads(stock_history_str).get("stock_history", [])
        return sum(float(entry.get("stock_decreased", 0)) for entry in history)
    except:
        return 0

# Tính toán
df['so_luong_ban'] = df['stock_history'].apply(total_sold_from_history)
df['doanh_thu'] = df['so_luong_ban'] * df['price']
revenue_by_product = df.groupby('name')['doanh_thu'].sum().sort_values(ascending=False).head(5)

# Vẽ biểu đồ matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=revenue_by_product.values, y=revenue_by_product.index, palette='pastel', ax=ax)

# Thêm nhãn
for i, v in enumerate(revenue_by_product.values):
    ax.text(v * 0.98, i, f"{int(v):,} VNĐ", color='black', va='center', ha='right', fontweight='bold')

ax.set_title("Tỷ lệ doanh thu Top 5 sản phẩm")
ax.set_xlabel("Doanh thu (VNĐ)")
ax.set_ylabel("Sản phẩm")
plt.tight_layout()

# 👉 Hiển thị lên Streamlit
st.pyplot(fig)
