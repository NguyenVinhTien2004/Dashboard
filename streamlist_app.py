    import pandas as pd
    import json
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Đọc dữ liệu từ file
    data = pd.read_csv("kf_coffee.csv")

    # Hàm tính tổng số lượng bán từ stock_history
    def total_sold_from_history(stock_history_str):
        try:
            history = json.loads(stock_history_str).get("stock_history", [])
            return sum(float(entry.get("stock_decreased", 0)) for entry in history)
        except:
            return 0

    # Áp dụng hàm để tính số lượng bán
    df['so_luong_ban'] = df['stock_history'].apply(total_sold_from_history)

    # Tính doanh thu
    df['doanh_thu'] = df['so_luong_ban'] * df['price']

    # Tính doanh thu theo sản phẩm
    revenue_by_product = df.groupby('name')['doanh_thu'].sum().sort_values(ascending=False).head(5)

    # Vẽ biểu đồ cột
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x=revenue_by_product.values, y=revenue_by_product.index, palette='pastel')

    # Hiển thị giá trị doanh thu trên từng cột, căn lề bên trong biểu đồ
    for i, v in enumerate(revenue_by_product.values):
        ax.text(v * 0.98, i, f"{int(v):,} VNĐ", color='black', va='center', ha='right', fontweight='bold')

    plt.title("Tỷ lệ doanh thu Top 5 sản phẩm")
    plt.xlabel("Doanh thu (VNĐ)")
    plt.ylabel("Sản phẩm")
    plt.tight_layout()
    plt.show()
