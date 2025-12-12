import yfinance as yf
import pandas as pd
import numpy as np
ticker = 'AMZN'
start_date = '2020-10-09'
end_date = '2025-10-11'

print(f"Đang tải dữ liệu cho {ticker} từ {start_date} đến {end_date}...")
try:
    data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)
    print("Tải dữ liệu hoàn tất.")
except Exception as e:
    print(f"Lỗi khi tải dữ liệu: {e}")
    exit()

if data.empty:
    print("Không có dữ liệu nào được tải về. Vui lòng kiểm tra lại ticker và ngày tháng.")
    exit()
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)
    print("\nĐã làm phẳng các tên cột từ MultiIndex.")
data_cleaned = data.dropna().copy()
print(f"\nKích thước dữ liệu sau khi xóa hàng có NaN: {data_cleaned.shape}")
data_cleaned.loc[:, 'Log Return'] = np.log(data_cleaned['Close'] / data_cleaned['Close'].shift(1))
data_cleaned = data_cleaned.dropna(subset=['Log Return'])
print(f"Kích thước dữ liệu sau khi tính Log Return và xóa NaN đầu tiên: {data_cleaned.shape}")
print(f"Ngày bắt đầu của dữ liệu đã làm sạch: **{data_cleaned.index.min().strftime('%Y-%m-%d')}**")
print("\nBắt đầu xử lý Outlier của cột 'Volume' bằng phương pháp 3IQR...")

Q1 = data_cleaned['Volume'].quantile(0.25)
Q3 = data_cleaned['Volume'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = max(0, Q1 - 3 * IQR)
upper_bound = Q3 + 3 * IQR
outliers_count = data_cleaned[(data_cleaned['Volume'] < lower_bound) | (data_cleaned['Volume'] > upper_bound)].shape[0]
print(f"Số lượng Outlier được xác định trong 'Volume': {outliers_count}")

data_cleaned.loc[:, 'Volume_Cleaned'] = data_cleaned['Volume'].clip(lower=lower_bound, upper=upper_bound)
data_cleaned = data_cleaned.drop('Volume', axis=1).rename(columns={'Volume_Cleaned': 'Volume'})
file_name = f'{ticker}_Stock_Data_Cleaned_with_LogReturn.xlsx'
try:
    data_cleaned.to_excel(file_name, index=True)
    print(f"\nĐã xuất dữ liệu đã làm sạch (bắt đầu từ 2020-10-10) ra file: **{file_name}**")
except Exception as e:
    print(f"\nLỗi khi xuất file Excel: {e}")
data_cleaned