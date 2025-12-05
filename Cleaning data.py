def clean_financial_data(df: pd.DataFrame, ticker_symbol: str) -> pd.DataFrame:
    if df.empty:
        print("DataFrame rỗng, bỏ qua quá trình làm sạch.")
        return pd.DataFrame()

    df = df.copy()
    price_cols = ['Open', 'High', 'Low','Close','Adj Close', 'Volume']
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    missing_cols = [col for col in price_cols if col not in df.columns]
    if missing_cols:
        return pd.DataFrame()

    # --- ĐẢM BẢO TÍNH NHẤT QUÁN & SẮP XẾP ---
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # --- XỬ LÝ DỮ LIỆU THIẾU (MISSING DATA - NaN) --
    df[price_cols] = df[price_cols].ffill().bfill() # Kết hợp ffill và bfill

    original_rows = len(df)
    df.dropna(subset=['Adj Close'], inplace=True)
    if original_rows > len(df):
        print(f"Đã xóa {original_rows - len(df)} hàng vẫn còn NaN sau khi điền.")


    # --- XỬ LÝ VOLUME = 0 HOẶC VÔ LÝ ---
    original_rows = len(df)
    df = df[df['Volume'] > 0]
    removed_volume_rows = original_rows - len(df)

    if removed_volume_rows > 0:
        print(f"Đã xóa {removed_volume_rows} hàng có Volume <= 0.")

    # --- KIỂM TRA VÀ XỬ LÝ DỮ LIỆU LỖI OHLC ---
    invalid_ohlc = df[
        (df['Low'] > df['High']) |
        (df['Close'] > df['High']) |
        (df['Close'] < df['Low']) |
        (df['Open'] < df['Low']) |
        (df['Open'] > df['High'])
    ]

    if not invalid_ohlc.empty:
        removed_ohlc_rows = len(invalid_ohlc)
        df.drop(invalid_ohlc.index, inplace=True)
        print(f" -> Đã xóa {removed_ohlc_rows} hàng bị lỗi OHLC.")

    # --- XỬ LÝ DỮ LIỆU NGOẠI LAI (Outliers) ---

    # 5.1. Xử lý Volume Outliers (Giả định Volume quá lớn là ngoại lai)
    Q1_vol = df['Volume'].quantile(0.25)
    Q3_vol = df['Volume'].quantile(0.75)
    IQR_vol = Q3_vol - Q1_vol
    # Sử dụng hệ số 3.0 (thay vì 1.5) để chỉ loại bỏ các giá trị cực đoan
    upper_bound_vol = Q3_vol + 3.0 * IQR_vol

    original_rows_vol = len(df)
    # Giữ lại các hàng có Volume nhỏ hơn ngưỡng trên
    df = df[df['Volume'] < upper_bound_vol]

    removed_outlier_vol_rows = original_rows_vol - len(df)
    if removed_outlier_vol_rows > 0:
        print(f" 	-> Đã xóa {removed_outlier_vol_rows} hàng có Volume quá lớn (> 3x IQR).")

    # 5.2. Xử lý Daily Return Outliers (Lợi nhuận cực đoan)
    df['Temp_Return'] = df['Adj Close'].pct_change()
    df.dropna(subset=['Temp_Return'], inplace=True)

    Q1_ret = df['Temp_Return'].quantile(0.25)
    Q3_ret = df['Temp_Return'].quantile(0.75)
    IQR_ret = Q3_ret - Q1_ret
    lower_bound_ret = Q1_ret - 3.0 * IQR_ret
    upper_bound_ret = Q3_ret + 3.0 * IQR_ret

    original_rows_ret = len(df)
    df = df[(df['Temp_Return'] > lower_bound_ret) & (df['Temp_Return'] < upper_bound_ret)]

    removed_ret_outlier_rows = original_rows_ret - len(df)
    if removed_ret_outlier_rows > 0:
        print(f" 	-> Đã xóa {removed_ret_outlier_rows} hàng có Daily Return ngoại lai (> 3x IQR).")
    df = df.drop(columns=['Temp_Return'])

    df['Daily_Return'] = df['Adj Close'].pct_change()
    df.dropna(subset=['Daily_Return'], inplace=True)
    print("\n" + "="*50)
    print(f"QUÁ TRÌNH LÀM SẠCH HOÀN TẤT CHO {ticker_symbol}.")
    print(f"Số hàng dữ liệu cuối cùng: {len(df)}")
    print("="*50)

    return df

def download_and_clean(ticker: str, start: str, end: str = date.today().strftime('%Y-%m-%d'), interval: str = '1d') -> pd.DataFrame:
    try:
        df_raw = yf.download(
            ticker,
            start=actual_start_date,
            end=actual_end_date,
            interval=interval,
            progress=False,
            auto_adjust=False,
        )
        if df_raw.empty:
            raise ValueError("Không tìm thấy dữ liệu.")
    except Exception as e:
        print(f"[DATA PIPELINE] LỖI TẢI DỮ LIỆU: {e}.")
        return pd.DataFrame()

    return clean_financial_data(df_raw, ticker)


# 3. CHẠY CODE VÀ HIỂN THỊ KẾT QUẢ
if __name__ == '__main__':
    cleaned_data = clean_financial_data(df_raw, TICKER)

    if not cleaned_data.empty:

        file_name = f"Cleaned_Data_{TICKER}_{date.today().strftime('%Y%m%d')}.xlsx"

        try:
            cleaned_data.to_excel(file_name, index=True)
            print(f"Tên file: {file_name}")
            print("*"*50)

        except Exception as e:
            print(f"\nLỖI XUẤT FILE EXCEL: {e}")
cleaned_data