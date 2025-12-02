import yfinance as yf
import numpy as np
import pandas as pd
from typing import Dict, Any, List

DEFAULT_DF = pd.DataFrame()

class FinancialMetricsCalculator:

    def __init__(self,
                 ticker_symbol: str,
                 api_key: str = None,
                 enforce_source: str = None,
                 quarterly: bool = False,
                 rounding: int = 2):
        self.ticker = yf.Ticker(ticker_symbol)
        self.symbol = ticker_symbol
        self.data: Dict[str, Any] = {} 
        self.report_date: str = "N/A"

        self._api_key = api_key
        self._enforce_source = enforce_source
        self._quarterly = quarterly
        self._rounding = rounding
        self._start_date: str = ""
        self._end_date: str = ""

        self._balance_sheet_statement = DEFAULT_DF
        self._income_statement = DEFAULT_DF
        self._cash_flow_statement = DEFAULT_DF

        # 4. Attributes cho dữ liệu lịch sử
        self._quarterly_historical_data = None
        self._yearly_historical_data = None
        self._daily_historical_data = None

        self._load_data()
        self._setup_data_and_checks()


    def _get(self, key: str) -> float:
        value = self.data.get(key)
        if value is None or (isinstance(value, (int, float)) and np.isnan(value)):
            return 0.0
        return float(value)

    def _safe_divide(self, numerator: float, denominator: float) -> float:
        if denominator == 0:
            return np.inf if numerator > 0 else 0.0
        return numerator / denominator

    def _load_data(self):

        print(f"Đang tải dữ liệu cho {self.symbol}...")

        try:
            info = self.ticker.info
            self._income_statement = self.ticker.financials
            self._balance_sheet_statement = self.ticker.balance_sheet
            self._cash_flow_statement = self.ticker.cashflow

            self.data['Share Price'] = info.get('currentPrice', 0)
            self.data['Shares Outstanding'] = info.get('sharesOutstanding', 0)
            self._info = info 

        except Exception as e:
            print(f"Lỗi khi tải dữ liệu yfinance: {e}")
            return

        if self._income_statement.empty or self._balance_sheet_statement.empty or self._cash_flow_statement.empty:
            return

        latest_is = self._income_statement.iloc[:, 0]
        latest_bs = self._balance_sheet_statement.iloc[:, 0]
        latest_cf = self._cash_flow_statement.iloc[:, 0]

        try:
            self.report_date = pd.to_datetime(latest_is.name).strftime('%Y-%m-%d')

            self.data.update(self._extract_period_data(latest_is, latest_bs, latest_cf, self._info))

        except Exception:
            self.report_date = "Lỗi trích xuất ngày/dữ liệu"


    def _extract_period_data(self, is_series: pd.Series, bs_series: pd.Series, cf_series: pd.Series, info_data: Dict[str, Any]) -> Dict[str, float]:

        data_dict = {}
        data_dict['Share Price'] = info_data.get('currentPrice', 0)
        data_dict['Shares Outstanding'] = info_data.get('sharesOutstanding', 0)

        latest_is = is_series.to_dict()
        data_dict['Total Revenue'] = latest_is.get('Total Revenue', 0)
        data_dict['Net Income'] = latest_is.get('Net Income', 0)
        data_dict['Cost Of Revenue'] = latest_is.get('Cost Of Revenue', 0)
        data_dict['EBIT'] = latest_is.get('Ebit', latest_is.get('Operating Income', 0))
        data_dict['Income Before Tax'] = latest_is.get('Income Before Tax', 0) # EBT
        data_dict['Interest Expense'] = latest_is.get('Interest Expense', latest_is.get('Interest expense', 0))

        # Bảng cân đối kế toán (BS)
        latest_bs = bs_series.to_dict()
        data_dict['Total Assets'] = latest_bs.get('Total Assets', latest_bs.get('Assets', 0))
        data_dict['Total Shareholders Equity'] = latest_bs.get('Total Stockholder Equity', latest_bs.get('Stockholders Equity', 0))
        data_dict['Total Current Assets'] = latest_bs.get('Total Current Assets', latest_bs.get('Current Assets', 0))
        data_dict['Total Current Liabilities'] = latest_bs.get('Total Current Liabilities', latest_bs.get('Current Liabilities', 0))
        data_dict['Inventory'] = latest_bs.get('Inventory', 0)
        data_dict['Total Liabilities'] = latest_bs.get('Total Liabilities', latest_bs.get('Total Liab', 0))

        latest_cf = cf_series.to_dict()
        data_dict['CFO'] = latest_cf.get('Total Cash From Operating Activities', latest_cf.get('Cash Flow From Operations', latest_cf.get('Operating Cash Flow', 0)))
        data_dict['CAPEX'] = latest_cf.get('Capital Expenditures', latest_cf.get('Capital expenditure', 0))
        data_dict['Total Dividends Paid'] = abs(latest_cf.get('Common Stock Dividend Paid', 0))

        return data_dict

    def _validate_data(self):
        required_fields = [
            'Total Revenue', 'Net Income', 'Shares Outstanding', 'Share Price',
            'Total Shareholders Equity', 'Total Assets', 'Total Current Liabilities'
        ]

        missing = [field for field in required_fields if self._get(field) == 0.0]
        if missing:
            print(f"CẢNH BÁO: Dữ liệu bị thiếu hoặc bằng 0 cho kỳ gần nhất: {', '.join(missing)}.")
            print("Các chỉ số liên quan sẽ trả về 0.0 hoặc N/A.")

    def _get_statement_placeholder(self, statement_name: str, progress_bar: bool = False):
        """Hàm giả lập việc tải lại."""
        print(f"Thử tải lại {statement_name}...")
        pass

    def _setup_data_and_checks(self):
        """Thực hiện logic kiểm tra tính toàn vẹn và thiết lập dữ liệu lịch sử."""

        empty_data: list = []
        if self._balance_sheet_statement.empty:
            empty_data.append("Balance Sheet Statement")
        if self._income_statement.empty:
            empty_data.append("Income Statement")
        if self._cash_flow_statement.empty:
            empty_data.append("Cash Flow Statement")

        if empty_data:
            print(f"Phát hiện thiếu dữ liệu: {', '.join(empty_data)}. Đang thử lại...")
            for statement in empty_data:
                self._get_statement_placeholder(statement)

        if (
            self._balance_sheet_statement.empty
            and self._income_statement.empty
            and self._cash_flow_statement.empty
        ):
            print("LỖI NGHIÊM TRỌNG: Dữ liệu tài chính không thể được tải.")

        self._validate_data() # Kiểm tra dữ liệu kỳ gần nhất

        # --- Thiết lập ngày bắt đầu/kết thúc ---
        if not self._start_date and not self._balance_sheet_statement.empty:
            try:
                oldest_year = self._balance_sheet_statement.columns[-1].year
                self._start_date = f"{oldest_year - 5}-01-01"
            except: self._start_date = "2000-01-01"

        if not self._end_date and not self._balance_sheet_statement.empty:
            try:
                newest_year = self._balance_sheet_statement.columns[0].year
                self._end_date = f"{newest_year + 5}-01-01"
            except: self._end_date = "2100-01-01"

        self._load_historical_data()


    def _load_historical_data(self):
        """Tải dữ liệu giá lịch sử theo cài đặt yearly/quarterly."""
        try:
            self._daily_historical_data = self.ticker.history(period="max")

            if self._quarterly:
                self._quarterly_historical_data = self.ticker.history(interval="3mo", period="max")
                print("Đã tải dữ liệu lịch sử theo quý.")
            else:
                self._yearly_historical_data = self.ticker.history(interval="1y", period="max")
                print("Đã tải dữ liệu lịch sử theo năm.")
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu giá lịch sử: {e}")

    # --- HELPER METRICS (Hỗ trợ cho các chỉ số phức tạp) ---

    def _income_before_tax(self) -> float:
        """Lấy EBT (Lợi nhuận trước thuế)."""
        ebt = self._get('Income Before Tax')
        if ebt == 0.0:
            return self._get('EBIT') - self._get('Interest Expense')
        return ebt

    def _tax_expense(self) -> float:
        """Công thức: Chi phí Thuế = EBT - Lợi Nhuận Ròng"""
        return self._income_before_tax() - self._get('Net Income')

    def _tax_rate(self) -> float:
        """Công thức: Tỷ lệ Thuế = Chi phí Thuế / EBT (dạng thập phân)"""
        return self._safe_divide(self._tax_expense(), self._income_before_tax())


    # --- PHƯƠNG THỨC TÍNH TOÁN (CORE) ---

    def _calculate_all_metrics_internal(self) -> Dict[str, float]:
        return {
            # 1. PER SHARE & MARKET
            'Earnings per Share (EPS)': self.earnings_per_share(),
            'Price to Earnings (P/E)': self.price_to_earnings_ratio(),
            'Book Value per Share (BPS)': self.book_value_per_share(),
            # 2. LIQUIDITY
            'Current Ratio': self.current_ratio(),
            'Quick Ratio': self.quick_ratio(),
            # 3. LEVERAGE
            'Debt to Equity (D/E)': self.debt_to_equity_ratio(),
            'Interest Coverage': self.interest_coverage_ratio(),
            'Interest Burden Ratio (EBT/EBIT)': self.interest_burden_ratio_new(),
            # 4. PROFITABILITY
            'Gross Margin (%)': self.gross_margin(),
            'Net Margin (%)': self.net_margin(),
            'Operating Margin (EBIT/Rev) (%)': self.operating_margin_new(),
            'Return on Equity (ROE) (%)': self.return_on_equity(),
            'Return on Assets (ROA) (%)': self.return_on_assets(),
            'Return on Invested Capital (ROIC) (%)': self.roic(),
            'Return on Capital Employed (ROCE) (%)': self.roce(),
            # 5. CASH FLOW
            'Free Cash Flow (FCF)': self.free_cash_flow(),
            'Income Quality Ratio (CFO/NI)': self.income_quality_ratio(),
        }

    # --- METRICS (Đã giữ nguyên) ---

    def earnings_per_share(self) -> float:
        return self._safe_divide(self._get('Net Income'), self._get('Shares Outstanding'))

    def book_value_per_share(self) -> float:
        return self._safe_divide(self._get('Total Shareholders Equity'), self._get('Shares Outstanding'))

    def price_to_earnings_ratio(self) -> float:
        eps = self.earnings_per_share()
        return self._safe_divide(self._get('Share Price'), eps)

    def current_ratio(self) -> float:
        return self._safe_divide(self._get('Total Current Assets'), self._get('Total Current Liabilities'))

    def quick_ratio(self) -> float:
        numerator = self._get('Total Current Assets') - self._get('Inventory')
        return self._safe_divide(numerator, self._get('Total Current Liabilities'))

    def debt_to_equity_ratio(self) -> float:
        return self._safe_divide(self._get('Total Liabilities'), self._get('Total Shareholders Equity'))

    def interest_coverage_ratio(self) -> float:
        return self._safe_divide(self._get('EBIT'), self._get('Interest Expense'))

    def gross_margin(self) -> float:
        gross_profit = self._get('Total Revenue') - self._get('Cost Of Revenue')
        return self._safe_divide(gross_profit, self._get('Total Revenue')) * 100

    def net_margin(self) -> float:
        return self._safe_divide(self._get('Net Income'), self._get('Total Revenue')) * 100

    def return_on_equity(self) -> float:
        return self._safe_divide(self._get('Net Income'), self._get('Total Shareholders Equity')) * 100

    def return_on_assets(self) -> float:
        return self._safe_divide(self._get('Net Income'), self._get('Total Assets')) * 100

    def free_cash_flow(self) -> float:
        return self._get('CFO') + self._get('CAPEX')

    def operating_margin_new(self) -> float:
        return self._safe_divide(self._get('EBIT'), self._get('Total Revenue')) * 100

    def interest_burden_ratio_new(self) -> float:
        return self._safe_divide(self._income_before_tax(), self._get('EBIT'))

    def roic(self) -> float:
        tax_rate = self._tax_rate()
        nopat = self._get('EBIT') * (1 - tax_rate)
        invested_capital = self._get('Total Liabilities') + self._get('Total Shareholders Equity')
        return self._safe_divide(nopat, invested_capital) * 100

    def roce(self) -> float:
        capital_employed = self._get('Total Assets') - self._get('Total Current Liabilities')
        return self._safe_divide(self._get('EBIT'), capital_employed) * 100

    def income_quality_ratio(self) -> float:
        return self._safe_divide(self._get('CFO'), self._get('Net Income'))


    # --- PHƯƠNG THỨC HIỂN THỊ KẾT QUẢ ---

    def _format_metric_value(self, val: float, metric: str) -> str:
        """Phương thức hỗ trợ định dạng giá trị dựa trên tên chỉ số."""
        if val == np.inf:
            return "Rất Cao"
        if '(%)' in metric:
            return f"{val:.2f}%"
        if 'per Share' in metric or 'FCF' in metric or val > 1000:
            return f"${val:,.2f}"
        return f"{val:.2f}x"

    def _map_metrics_to_groups(self, metric: str) -> str:
        """
        Ánh xạ chỉ số vào nhóm phân tích ban đầu (để giữ thứ tự sắp xếp),
        nhưng không được sử dụng làm index hiển thị nữa.
        """
        groups = {
            'Earnings per Share (EPS)': '4', 'Price to Earnings (P/E)': '4', 'Book Value per Share (BPS)': '4',
            'Current Ratio': '1', 'Quick Ratio': '1',
            'Debt to Equity (D/E)': '2', 'Interest Coverage': '2', 'Interest Burden Ratio (EBT/EBIT)': '2',
            'Gross Margin (%)': '3', 'Net Margin (%)': '3', 'Operating Margin (EBIT/Rev) (%)': '3',
            'Return on Equity (ROE) (%)': '3', 'Return on Assets (ROA) (%)': '3',
            'Return on Invested Capital (ROIC) (%)': '3', 'Return on Capital Employed (ROCE) (%)': '3',
            'Free Cash Flow (FCF)': '5', 'Income Quality Ratio (CFO/NI)': '5',
        }
        return groups.get(metric, '6')

    def calculate_latest_metrics(self):
        """Tính toán và hiển thị tất cả các chỉ số cho kỳ báo cáo GẦN NHẤT."""

        # 1. Tính toán
        results = self._calculate_all_metrics_internal()

        # 2. Định dạng
        df = pd.DataFrame(list(results.items()), columns=['Metric', 'Value'])
        df['Formatted Value'] = df.apply(lambda row: self._format_metric_value(row['Value'], row['Metric']), axis=1)

        # Thêm cột sắp xếp tạm thời và sắp xếp theo nhóm/metric để giữ thứ tự
        df['Sort_Group'] = df['Metric'].apply(self._map_metrics_to_groups)
        df_display = df.sort_values(by=['Sort_Group', 'Metric']).drop(columns=['Value', 'Sort_Group'])

        # Thiết lập cột Metric làm index
        df_display = df_display.set_index('Metric')

        # 3. Hiển thị thông tin
        print("\n" + "="*70)
        print(f"--- PHÂN TÍCH CƠ BẢN KỲ GẦN NHẤT CHO CỔ PHIẾU {self.symbol} ---")
        print(f"Ngày báo cáo gần nhất: {self.report_date}")
        print(f"Giá cổ phiếu hiện tại: ${self._get('Share Price'):,.2f}")
        print("="*70)

        # In DataFrame chỉ với cột "Formatted Value" và index là Metric
        print(df_display.to_string(index=True, header=True))
        print("="*70)

        return results

    def calculate_historical_metrics(self, num_periods: int = 4):
        """
        Tính toán và hiển thị tất cả các chỉ số tài chính cho nhiều kỳ báo cáo.

        Args:
            num_periods (int): Số lượng kỳ báo cáo (tính từ gần nhất) muốn tính toán. Mặc định là 4.
        """
        if self._income_statement.empty or self._balance_sheet_statement.empty or self._cash_flow_statement.empty:
            print("Lỗi: Dữ liệu tài chính lịch sử không đầy đủ để tính toán.")
            return {}

        all_results_df = pd.DataFrame()
        original_data = self.data.copy() # Lưu lại data kỳ gần nhất

        # Xác định số cột cần lấy (tối đa là số cột có sẵn, không vượt quá num_periods)
        num_cols = min(num_periods, len(self._income_statement.columns))

        # Lấy thông tin thị trường (info)
        info = getattr(self, '_info', self.ticker.info)

        # Dùng .iloc để lấy các cột gần nhất (cột 0 là gần nhất)
        for i in range(num_cols):
            try:
                is_series = self._income_statement.iloc[:, i]
                bs_series = self._balance_sheet_statement.iloc[:, i]
                cf_series = self._cash_flow_statement.iloc[:, i]

                # Chuyển tên cột (là DatetimeIndex) thành chuỗi ngày tháng
                period_date = is_series.name.strftime('%Y-%m-%d')

                # 1. Trích xuất dữ liệu cho kỳ này và tạm thời gán vào self.data
                period_data_dict = self._extract_period_data(is_series, bs_series, cf_series, info)
                self.data = period_data_dict

                # 2. Tính toán metrics
                metrics = self._calculate_all_metrics_internal()

                # 3. Thêm vào DataFrame tổng
                metrics_series = pd.Series(metrics, name=period_date)
                all_results_df = pd.concat([all_results_df, metrics_series], axis=1)

            except Exception as e:
                # Nếu có lỗi tính toán, chỉ in cảnh báo và bỏ qua kỳ đó
                print(f"CẢNH BÁO: Lỗi tính toán cho kỳ {self._income_statement.columns[i].strftime('%Y-%m-%d') if not self._income_statement.empty else 'N/A'}: {e}")
                continue

        self.data = original_data

        if all_results_df.empty:
            print("Không thể tính toán chỉ số cho bất kỳ kỳ báo cáo nào.")
            return {}
        all_results_df = all_results_df.iloc[:, ::-1]
        formatted_df = all_results_df.apply(lambda col: [self._format_metric_value(val, idx) for idx, val in col.items()], axis=0)
        formatted_df.index = all_results_df.index 

        formatted_df['Sort_Group'] = formatted_df.index.to_series().apply(self._map_metrics_to_groups)

        df_display = formatted_df.sort_values(by='Sort_Group').drop(columns=['Sort_Group'])
        df_display.index.name = "Metric" 

        print("\n" + "="*70)
        print(f"--- PHÂN TÍCH CHỈ SỐ LỊCH SỬ CHO CỔ PHIẾU {self.symbol} ---")
        print("Các kỳ: " + ", ".join(all_results_df.columns))
        print("="*70)

        # In DataFrame chỉ với Metric làm index
        print(df_display.to_string(index=True, header=True, justify='center'))
        print("="*70)

        return all_results_df


    def print_historical_fundamentals(self):

        if self._income_statement.empty or self._balance_sheet_statement.empty or self._cash_flow_statement.empty:
            print("Không có dữ liệu báo cáo tài chính lịch sử để hiển thị.")
            return

        periods = self._income_statement.columns

        key_metrics_map = {
            'Total Revenue': 'Tổng Doanh thu',
            'Net Income': 'Lợi nhuận Ròng',
            'Ebit': 'Lợi nhuận HĐ (EBIT)',
            'Total Current Assets': 'TS Ngắn hạn',
            'Total Current Liabilities': 'Nợ Ngắn hạn',
            'Total Assets': 'Tổng Tài sản',
            'Total Stockholder Equity': 'Vốn Chủ sở hữu',
            'Total Liabilities': 'Tổng Nợ',
            'Total Cash From Operating Activities': 'Dòng tiền HĐ (CFO)',
            'Capital Expenditures': 'Chi tiêu Vốn (CAPEX)',
        }

        historical_data = pd.DataFrame(index=key_metrics_map.values())

        is_df = self._income_statement
        bs_df = self._balance_sheet_statement
        cf_df = self._cash_flow_statement

        fallback_map = {
            'Ebit': 'Operating Income',
            'Total Assets': 'Assets',
            'Total Stockholder Equity': 'Stockholders Equity',
            'Total Cash From Operating Activities': 'Operating Cash Flow',
            'Capital Expenditures': 'Capital expenditure'
        }

        for period in periods:
            period_data = {}
            period_str = period.strftime('%Y-%m-%d')
            for yf_key, display_name in key_metrics_map.items():
                value = 0.0

                if display_name in ['Tổng Doanh thu', 'Lợi nhuận Ròng', 'Lợi nhuận HĐ (EBIT)']: df = is_df
                elif display_name in ['TS Ngắn hạn', 'Nợ Ngắn hạn', 'Tổng Tài sản', 'Vốn Chủ sở hữu', 'Tổng Nợ']: df = bs_df
                elif display_name in ['Dòng tiền HĐ (CFO)', 'Chi tiêu Vốn (CAPEX)']: df = cf_df
                else: continue

                if yf_key in df.index:
                    value = df.loc[yf_key, period]
                elif yf_key in fallback_map and fallback_map[yf_key] in df.index:
                    value = df.loc[fallback_map[yf_key], period]

                if pd.isna(value) or value is None:
                    value = 0.0

                period_data[display_name] = value

            historical_data[period_str] = pd.Series(period_data)

        formatted_data = historical_data.apply(lambda x: x / 1_000_000, axis=0)
        formatted_data = formatted_data.applymap(lambda x: f"{x:,.2f}M")

        print("\n" + "="*70)
        print(f"--- DỮ LIỆU TÀI CHÍNH CƠ BẢN QUA CÁC KỲ ({self.symbol}) ---")
        print("(Đơn vị: Triệu)")
        print("="*70)
        print(formatted_data.to_string(index=True, header=True))
        print("="*70)

        return historical_data

### Áp dụng để tải fundamental cho các mã cổ phiếu

SYMBOL = 'NKE'
calculator = FinancialMetricsCalculator(SYMBOL, quarterly=False)
calculator.calculate_historical_metrics(num_periods=4)