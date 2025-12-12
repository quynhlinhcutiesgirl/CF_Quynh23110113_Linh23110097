
from financetoolkit import Toolkit

API_KEY = "YzOe6wbjIGGJ1DZJPvPQ50lCVGk7LzYD"
companies = Toolkit(
    ["AAPL", "AMZN", "META", "WMT", "MSFT"], api_key=API_KEY, start_date="2022-10-10",end_date="2025-10-10"
)
companies.ratios.collect_solvency_ratios(diluted=False, growth=True)

# |level\_0|level\_1|2022|2023|2024|2025|
# |---|---|---|---|---|---|
# |AAPL|Debt-to-Assets Ratio|NaN|-0\.0642|-0\.072|-0\.1582|
# |AAPL|Debt-to-Equity Ratio|NaN|-0\.2373|0\.0483|-0\.36|
# |AAPL|Debt Service Coverage Ratio|NaN|0\.0141|-0\.112|0\.15|
# |AAPL|Equity Multiplier|NaN|7\.0598|-0\.0363|-0\.0802|
# |AAPL|Free Cash Flow Yield|NaN|-0\.3781|-0\.1398|-0\.159|
# |AAPL|Net-Debt to EBITDA Ratio|NaN|-0\.1042|-0\.1138|-0\.3453|
# |AAPL|Cash Flow Coverage Ratio|NaN|-0\.0325|0\.1135|0\.1377|
# |AAPL|CAPEX Coverage Ratio|NaN|-0\.1158|0\.241|-0\.2996|
# |AAPL|Dividend CAPEX Coverage Ratio|NaN|-0\.1102|0\.1262|-0\.173|
# |AMZN|Debt-to-Assets Ratio|NaN|-0\.1516|-0\.1845|-19\.9131|
# |AMZN|Debt-to-Equity Ratio|NaN|-0\.2998|-0\.3187|-9\.657|
# |AMZN|Debt Service Coverage Ratio|NaN|1\.8363|0\.7105|-11\.3644|
# |AMZN|Equity Multiplier|NaN|35\.1294|-0\.17|-2\.6769|
# |AMZN|Free Cash Flow Yield|NaN|-2\.0457|-0\.3058|-278\.0839|
# |AMZN|Net-Debt to EBITDA Ratio|NaN|-0\.5429|-0\.4098|-10\.2275|
# |AMZN|Cash Flow Coverage Ratio|NaN|0\.8771|0\.4132|-5\.4762|
# |AMZN|CAPEX Coverage Ratio|NaN|1\.193|-0\.1334|1\.8381|
# |AMZN|Dividend CAPEX Coverage Ratio|NaN|1\.193|-0\.1334|1\.8381|
# |META|Debt-to-Assets Ratio|NaN|0\.1327|0\.0956|-23\.2977|
# |META|Debt-to-Equity Ratio|NaN|0\.1494|0\.1049|-15\.7517|
# |META|Debt Service Coverage Ratio|NaN|0\.3658|0\.4117|-2\.9187|
# |META|Equity Multiplier|NaN|0\.3906|0\.0111|-3\.6312|
# |META|Free Cash Flow Yield|NaN|-0\.1834|-0\.2432|-109\.8544|
# |META|Net-Debt to EBITDA Ratio|NaN|-1\.2524|-1\.7622|-66\.0624|
# |META|Cash Flow Coverage Ratio|NaN|0\.0062|-0\.0253|-3\.1284|
# |META|CAPEX Coverage Ratio|NaN|0\.6241|-0\.0601|0\.6163|
# |META|Dividend CAPEX Coverage Ratio|NaN|0\.6241|-0\.1727|0\.8364|
# |MSFT|Debt-to-Assets Ratio|NaN|-0\.1328|-0\.0996|-0\.2532|
# |MSFT|Debt-to-Equity Ratio|NaN|-0\.2096|-0\.1403|-0\.2944|
# |MSFT|Debt Service Coverage Ratio|NaN|-0\.0308|0\.0276|0\.0419|
# |MSFT|Equity Multiplier|NaN|1\.3762|-0\.0658|-0\.0505|
# |MSFT|Free Cash Flow Yield|NaN|-0\.4144|0\.1132|-0\.1568|
# |MSFT|Net-Debt to EBITDA Ratio|NaN|-0\.4901|0\.5022|-0\.4968|
# |MSFT|Cash Flow Coverage Ratio|NaN|0\.0051|0\.2091|0\.2725|
# |MSFT|CAPEX Coverage Ratio|NaN|-0\.1641|-0\.1446|-0\.2086|
# |MSFT|Dividend CAPEX Coverage Ratio|NaN|-0\.1372|-0\.0212|-0\.1415|
# |WMT|Debt-to-Assets Ratio|NaN|0\.035|0\.0029|-0\.0514|
# |WMT|Debt-to-Equity Ratio|NaN|0\.1246|-0\.0349|-0\.0911|
# |WMT|Debt Service Coverage Ratio|NaN|-0\.2536|0\.319|0\.0397|
# |WMT|Equity Multiplier|NaN|8\.3462|0\.0231|-0\.0398|
# |WMT|Free Cash Flow Yield|NaN|-0\.0036|-0\.2581|-0\.343|
# |WMT|Net-Debt to EBITDA Ratio|NaN|0\.3786|-0\.1742|-0\.0884|
# |WMT|Cash Flow Coverage Ratio|NaN|0\.1605|0\.1902|0\.0405|
# |WMT|CAPEX Coverage Ratio|NaN|-0\.0727|0\.0134|-0\.1162|
# |WMT|Dividend CAPEX Coverage Ratio|NaN|-0\.0001|0\.064|-0\.1047| ""

companies.ratios.collect_solvency_ratios(diluted=False, growth=True)
# |level\_0|level\_1|2022|2023|2024|2025|
# |---|---|---|---|---|---|
# |AAPL|Debt-to-Assets Ratio|NaN|-0\.0642|-0\.072|-0\.1582|
# |AAPL|Debt-to-Equity Ratio|NaN|-0\.2373|0\.0483|-0\.36|
# |AAPL|Debt Service Coverage Ratio|NaN|0\.0141|-0\.112|0\.15|
# |AAPL|Equity Multiplier|NaN|7\.0598|-0\.0363|-0\.0802|
# |AAPL|Free Cash Flow Yield|NaN|-0\.3781|-0\.1398|-0\.159|
# |AAPL|Net-Debt to EBITDA Ratio|NaN|-0\.1042|-0\.1138|-0\.3453|
# |AAPL|Cash Flow Coverage Ratio|NaN|-0\.0325|0\.1135|0\.1377|
# |AAPL|CAPEX Coverage Ratio|NaN|-0\.1158|0\.241|-0\.2996|
# |AAPL|Dividend CAPEX Coverage Ratio|NaN|-0\.1102|0\.1262|-0\.173|
# |AMZN|Debt-to-Assets Ratio|NaN|-0\.1516|-0\.1845|-19\.9131|
# |AMZN|Debt-to-Equity Ratio|NaN|-0\.2998|-0\.3187|-9\.657|
# |AMZN|Debt Service Coverage Ratio|NaN|1\.8363|0\.7105|-11\.3644|
# |AMZN|Equity Multiplier|NaN|35\.1294|-0\.17|-2\.6769|
# |AMZN|Free Cash Flow Yield|NaN|-2\.0457|-0\.3058|-278\.0839|
# |AMZN|Net-Debt to EBITDA Ratio|NaN|-0\.5429|-0\.4098|-10\.2275|
# |AMZN|Cash Flow Coverage Ratio|NaN|0\.8771|0\.4132|-5\.4762|
# |AMZN|CAPEX Coverage Ratio|NaN|1\.193|-0\.1334|1\.8381|
# |AMZN|Dividend CAPEX Coverage Ratio|NaN|1\.193|-0\.1334|1\.8381|
# |META|Debt-to-Assets Ratio|NaN|0\.1327|0\.0956|-23\.2977|
# |META|Debt-to-Equity Ratio|NaN|0\.1494|0\.1049|-15\.7517|
# |META|Debt Service Coverage Ratio|NaN|0\.3658|0\.4117|-2\.9187|
# |META|Equity Multiplier|NaN|0\.3906|0\.0111|-3\.6312|
# |META|Free Cash Flow Yield|NaN|-0\.1834|-0\.2432|-109\.8544|
# |META|Net-Debt to EBITDA Ratio|NaN|-1\.2524|-1\.7622|-66\.0624|
# |META|Cash Flow Coverage Ratio|NaN|0\.0062|-0\.0253|-3\.1284|
# |META|CAPEX Coverage Ratio|NaN|0\.6241|-0\.0601|0\.6163|
# |META|Dividend CAPEX Coverage Ratio|NaN|0\.6241|-0\.1727|0\.8364|
# |MSFT|Debt-to-Assets Ratio|NaN|-0\.1328|-0\.0996|-0\.2532|
# |MSFT|Debt-to-Equity Ratio|NaN|-0\.2096|-0\.1403|-0\.2944|
# |MSFT|Debt Service Coverage Ratio|NaN|-0\.0308|0\.0276|0\.0419|
# |MSFT|Equity Multiplier|NaN|1\.3762|-0\.0658|-0\.0505|
# |MSFT|Free Cash Flow Yield|NaN|-0\.4144|0\.1132|-0\.1568|
# |MSFT|Net-Debt to EBITDA Ratio|NaN|-0\.4901|0\.5022|-0\.4968|
# |MSFT|Cash Flow Coverage Ratio|NaN|0\.0051|0\.2091|0\.2725|
# |MSFT|CAPEX Coverage Ratio|NaN|-0\.1641|-0\.1446|-0\.2086|
# |MSFT|Dividend CAPEX Coverage Ratio|NaN|-0\.1372|-0\.0212|-0\.1415|
# |WMT|Debt-to-Assets Ratio|NaN|0\.035|0\.0029|-0\.0514|
# |WMT|Debt-to-Equity Ratio|NaN|0\.1246|-0\.0349|-0\.0911|
# |WMT|Debt Service Coverage Ratio|NaN|-0\.2536|0\.319|0\.0397|
# |WMT|Equity Multiplier|NaN|8\.3462|0\.0231|-0\.0398|
# |WMT|Free Cash Flow Yield|NaN|-0\.0036|-0\.2581|-0\.343|
# |WMT|Net-Debt to EBITDA Ratio|NaN|0\.3786|-0\.1742|-0\.0884|
# |WMT|Cash Flow Coverage Ratio|NaN|0\.1605|0\.1902|0\.0405|
# |WMT|CAPEX Coverage Ratio|NaN|-0\.0727|0\.0134|-0\.1162|
# |WMT|Dividend CAPEX Coverage Ratio|NaN|-0\.0001|0\.064|-0\.1047| 