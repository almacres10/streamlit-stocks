import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fungsi untuk mengambil data saham
def get_stock_data(ticker, start_date, end_date, interval):
    stock_data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    stock_data = stock_data.sort_values(by='Date', ascending=False)  # Mengurutkan berdasarkan tanggal dari yang terbaru
    return stock_data


# Fungsi untuk membuat grafik pergerakan harga saham
def plot_stock_data(stock_data):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(stock_data['Close'], label='Close')
    ax.set_title('Pergerakan Harga Saham')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Harga (USD)')
    ax.legend()
    st.pyplot(fig)

# Fungsi untuk mendapatkan data volume trading
def get_volume_data(ticker, start_date, end_date, interval):
    stock_data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    return stock_data['Volume']

# Fungsi untuk mendapatkan riwayat dividen dari saham
def get_dividend_history(ticker):
    stock = yf.Ticker(ticker)
    dividend_history = stock.dividends
    dividend_history = dividend_history.sort_index(ascending=False)  # Mengurutkan dari yang terbaru
    return dividend_history

# Fungsi untuk mendapatkan informasi saham
def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    return stock.info

def get_stock_info2(ticker):
    stock_info = yf.Ticker(ticker)
    stock_info = stock_info.info
    return stock_info


# Main function
def main():
    st.title('Aplikasi Data Saham')

    # Input ticker saham dan tahun
    ticker = st.text_input('Masukkan Ticker Saham (Contoh: BBNI.JK untuk Bank BNI)', 'BBNI.JK')
    year = st.slider('Pilih Tahun', min_value=2010, max_value=2024, value=2020)
    interval = st.selectbox('Pilih Interval', ['1d', '1wk', '1mo'], index=0)


    # Mendapatkan data saham
    start_date = str(year) + '-01-01'
    end_date = str(year) + '-12-31'
    stock_data = get_stock_data(ticker, start_date, end_date, interval)
    volume_data = get_volume_data(ticker, start_date, end_date, interval)

    # Mendapatkan informasi saham
    stock_info = get_stock_info(ticker)

    if stock_data.empty:
        st.warning('Data saham tidak tersedia. Mohon periksa kembali ticker saham yang dimasukkan.')
    else:
        # Menampilkan informasi saham
        st.subheader('Tentang Saham')
        st.write('**Nama Perusahaan:**', stock_info['longName'])
        st.write('**Deskripsi:**', stock_info['longBusinessSummary'])
        st.write('**Sektor:**', stock_info['sector'])
        st.write('**Industri:**', stock_info['industry'])
        st.write('**Negara:**', stock_info['country'])
        st.write('**Market Cap:**', stock_info['marketCap'])

        # Menampilkan data saham
        st.subheader('Data Saham')
        st.write(stock_data)

        # Menampilkan grafik pergerakan harga saham
        st.subheader('Grafik Pergerakan Harga Saham')
        plot_stock_data(stock_data)

         # Grafik volume trading
        st.subheader('Volume Trading')
        st.line_chart(volume_data)

        # Perbandingan Saham
        st.subheader('Perbandingan Saham')
        tickers = st.text_input('Masukkan Ticker Saham untuk Perbandingan (pisahkan dengan koma)', 'BBNI.JK, BBRI.JK')
        tickers_list = [ticker.strip() for ticker in tickers.split(',')]
        comparison_data = pd.DataFrame()
        for t in tickers_list:
            comparison_data[t] = yf.download(t, start=start_date, end=end_date, interval=interval)['Close']
        st.line_chart(comparison_data)

        # Mendapatkan riwayat dividen
        st.subheader('Riwayat Dividen')
        dividend_history = get_dividend_history(ticker)
        st.write(dividend_history)

        # Menampilkan informasi tambahan
        st.subheader('Informasi Tambahan')
        st.write('Sektor:', stock_info['sector'])
        st.write('ROE', stock_info['returnOnEquity'])
        st.write('ROA', stock_info['returnOnAssets'])
        st.write('EPS', stock_info['earningsGrowth'])


if __name__ == '__main__':
    main()
