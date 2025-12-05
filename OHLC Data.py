TICKER = 'PMMAF'
START_DATE_REQUEST = '2022-10-10'
END_DATE = '2025-10-11'
INTERVAL = '1d'
try:
    data = yf.download(
        TICKER,
        start=START_DATE_REQUEST,
        end=END_DATE,
        interval=INTERVAL,
        progress=False,
        auto_adjust=False,
    )

    if data.empty:
        df_raw = pd.DataFrame()
    else:
        actual_start_date = data.index.min().strftime('%Y-%m-%d')
        actual_end_date = data.index.max().strftime('%Y-%m-%d')
        df_raw = data.copy()
except Exception as e:
    df_raw = pd.DataFrame()
data

