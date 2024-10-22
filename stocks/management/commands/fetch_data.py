import requests
from django.core.management.base import BaseCommand
from stocks.models import StockData
from django.utils import timezone
from datetime import datetime, timedelta
from decouple import config

# FETCH DAILY STOCK DATA FROM ALPHA VANTAGE FOR MULTIPLE STOCKS

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        # LIST OF STOCKS
        symbols = ['AAPL', 'MSFT', 'GOOGL']
        api_key = config('ALPHA_VANTAGE_API_KEY') 

        # 2 YEARS AGO FROM TODAY
        cutoff_date = datetime.now() - timedelta(days=730) 
        cutoff_date_str = cutoff_date.strftime('%Y-%m-%d')

        for symbol in symbols:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={api_key}'
            response = requests.get(url)
            data = response.json()

            if 'Time Series (Daily)' in data:
                for date, metrics in data['Time Series (Daily)'].items():
                    if date < cutoff_date_str:
                        continue
                    stock_data = StockData(
                        symbol=symbol,
                        date=date,
                        open_price=float(metrics['1. open']),
                        high_price=float(metrics['2. high']),
                        low_price=float(metrics['3. low']),
                        close_price=float(metrics['4. close']),
                        volume=int(metrics['5. volume']),
                    )
                    stock_data.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully fetched and stored stock data for {symbol}.'))
            else:
                self.stdout.write(self.style.ERROR(f'Error fetching stock data for {symbol}: {data}'))
