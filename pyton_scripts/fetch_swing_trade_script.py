import requests
import os
from datetime import datetime

def fetch_swing_trades():
    """
    Fetch swing trading opportunities from ChartInk screener
    Returns a list of stocks matching the swing trading criteria
    """
    
    # Note: These tokens will expire and need to be refreshed periodically
    # Consider moving to environment variables for production
    cookies = {
        'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d': 'eyJpdiI6ImFML1J3QUJZZ2tQT0hLNDFvRE10WXc9PSIsInZhbHVlIjoiZi9NVzFMR0Y3eGVseDNrR1Vib3RSTkhNZExwSTgwNkx2QnJ4WWs2bDZBUmVxOFBPZWhwQkl2RERsc01TTFUramF1c0YzcUd1U0MwZmhQOUFDQ2hQajVlQVpDRzBlanZTMnVIZEd2cVJVQVZVTTV1Y2M2aWp5QVNORUdiMGJ0M2k5MmFqN0RWaFhyOVdRajJVL21hQUVoRGJEblBrQVI0cjBzUHBiT2o5akhnSnJmWm91d2IwYWx3Tlc0d3hFajUybktMaGEvN3o5cmhmTnFFVkFHTUxCK3puVVQ4LzRidWhGTHVJTmRaMWNGbz0iLCJtYWMiOiJhZWZjZWRmNjYxNTFkZDJjZTBjZDljZWU5NmE2NzVlM2UxMjJiY2U4Y2Y1NjNhMjE1ODEwNjgxMzc5ZGFlN2IxIiwidGFnIjoiIn0%3D',
        '_au_1d': 'AU1D-0100-001737407818-PCV4Z5DT-8C3L',
        'XSRF-TOKEN': 'eyJpdiI6IlppTm1tVWtKWk9NZUVvWnFEZDA4ZVE9PSIsInZhbHVlIjoiY3YrUk1WeFllZ2xLaDRTYTQ1MTNjUmpJRThnM2xJTDdrQnp2YlVVTEdqSkgxL2N1WUUyNEhCa2x0TURRVGN4MW03V0h4UDRlTEcxa3FKZ0p3YXVuWlU4RFU3dDVtNHN2S0JhZXBYUHc3dDA1ZGlJZE5SOE92YlN3dnBSSmtrblciLCJtYWMiOiIzNWI5ZThhMzdjYjYwZTFjMzI1ZjliMmQwZjkxMjdiOGZkNzliNzFjYTgwM2I2NjNiNmNkZGE1YjYzOTgxZmIzIiwidGFnIjoiIn0%3D',
        'ci_session': 'eyJpdiI6IllaOEdzcDRvaS9Cd3RUT2FpZHZIOUE9PSIsInZhbHVlIjoickNUREtjLzFGNk5ldTFqTm9LTXQrRHhSK1NVS2dpN0VMQkcxTkpyYld6TmFUZkthQnlJWE1GM0o0eUdkL0J2L3R1NnZCV3FnYi9PZ0dIVmZuakEweGtMYXpZQWNzQ2xKTGx1aUd2OHk3WHBYdVdmajBLQ0VoUHgya0IrakpYdUciLCJtYWMiOiI0NTNjYmFhOTUxNWVjYzQ4NDM2YWI4NGY3MmYwYWIzN2I0MWU0NDdlYTgyYjhiZWJlMTdiYmU1MjdkY2JhOTMyIiwidGFnIjoiIn0%3D',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://chartink.com',
        'priority': 'u=1, i',
        'referer': 'https://chartink.com/screener/swing-pullback-weekly-2',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrf-token': 'eyJpdiI6IlppTm1tVWtKWk9NZUVvWnFEZDA4ZVE9PSIsInZhbHVlIjoiY3YrUk1WeFllZ2xLaDRTYTQ1MTNjUmpJRThnM2xJTDdrQnp2YlVVTEdqSkgxL2N1WUUyNEhCa2x0TURRVGN4MW03V0h4UDRlTEcxa3FKZ0p3YXVuWlU4RFU3dDVtNHN2S0JhZXBYUHc3dDA1ZGlJZE5SOE92YlN3dnBSSmtrblciLCJtYWMiOiIzNWI5ZThhMzdjYjYwZTFjMzI1ZjliMmQwZjkxMjdiOGZkNzliNzFjYTgwM2I2NjNiNmNkZGE1YjYzOTgxZmIzIiwidGFnIjoiIn0=',
    }

    json_data = {
        'scan_clause': '( {cash} ( ( {cash} ( ( {cash} ( weekly macd line( 21 , 3 , 9 ) >= weekly macd signal( 21 , 3 , 9 ) and weekly ha-close  > weekly "wma( ( ( 2 * wma( (weekly ha-close ), 15) ) - wma((weekly ha-close ), 30) ), 5)" and 1 week ago  ha-close  <= 1 week ago  "wma( ( ( 2 * wma( (weekly ha-close ), 15) ) - wma((weekly ha-close ), 30) ), 5)" and 1 week ago ha-close  < weekly "wma( ( ( 2 * wma( (1 week ago min( 12 , weekly ha-close  )), 15) ) - wma((1 week ago min( 12 , weekly ha-close  )), 30) ), 5)" ) ) or( {cash} ( weekly ha-close  >= weekly "wma( ( ( 2 * wma( (weekly ha-close ), 22) ) - wma((weekly ha-close ), 44) ), 6)" and 1 week ago ha-close  < weekly "wma( ( ( 2 * wma( (1 week ago min( 12 , weekly ha-close  )), 15) ) - wma((1 week ago min( 12 , weekly ha-close  )), 30) ), 5)" and weekly macd line( 11 , 3 , 9 ) > weekly macd signal( 11 , 3 , 9 ) and 1 week ago  macd line( 11 , 3 , 9 ) <= 1 week ago  macd signal( 11 , 3 , 9 ) and 1 week ago max( 7 , 1 week ago macd histogram( 21 , 3 , 9 ) ) < 0 ) ) ) ) and weekly wma( weekly rsi( 9 ) , 11 ) < weekly rsi( 9 ) and daily close > 50 and 1 day ago volume > 50000 and market cap > 1000 and weekly macd histogram( 21 , 3 , 9 ) > 0 and weekly ha-close  > weekly ha-open  and daily close > daily open and weekly min( 10 , weekly macd histogram( 21 , 3 , 9 ) ) < -20 and weekly volume > weekly sma( weekly close , 7 ) ) ) ',
        'debug_clause': 'groupcount( 1 where         weekly macd line( 21 , 3 , 9 ) >= weekly macd signal( 21 , 3 , 9 )),groupcount( 1 where         weekly ha-close  > weekly "wma( ( ( 2 * wma( (weekly ha-close ), 15) ) - wma((weekly ha-close ), 30) ), 5)" and 1 week ago  ha-close  <= 1 week ago  "wma( ( ( 2 * wma( (weekly ha-close ), 15) ) - wma((weekly ha-close ), 30) ), 5)"),groupcount( 1 where         1 week ago ha-close  < weekly "wma( ( ( 2 * wma( (1 week ago min( 12 , weekly ha-close  )), 15) ) - wma((1 week ago min( 12 , weekly ha-close  )), 30) ), 5)"),groupcount( 1 where         weekly ha-close  >= weekly "wma( ( ( 2 * wma( (weekly ha-close ), 22) ) - wma((weekly ha-close ), 44) ), 6)"),groupcount( 1 where         1 week ago ha-close  < weekly "wma( ( ( 2 * wma( (1 week ago min( 12 , weekly ha-close  )), 15) ) - wma((1 week ago min( 12 , weekly ha-close  )), 30) ), 5)"),groupcount( 1 where         weekly macd line( 11 , 3 , 9 ) > weekly macd signal( 11 , 3 , 9 ) and 1 week ago  macd line( 11 , 3 , 9 ) <= 1 week ago  macd signal( 11 , 3 , 9 )),groupcount( 1 where         1 week ago max( 7 , 1 week ago macd histogram( 21 , 3 , 9 ) ) < 0),groupcount( 1 where weekly wma( weekly rsi( 9 ) , 11 ) < weekly rsi( 9 )),groupcount( 1 where daily close > 50),groupcount( 1 where 1 day ago volume > 50000),groupcount( 1 where market cap > 1000),groupcount( 1 where weekly macd histogram( 21 , 3 , 9 ) > 0),groupcount( 1 where weekly ha-close  > weekly ha-open ),groupcount( 1 where daily close > daily open),groupcount( 1 where weekly min( 10 , weekly macd histogram( 21 , 3 , 9 ) ) < -20),groupcount( 1 where weekly volume > weekly sma( weekly close , 7 ))',
    }

    try:
        response = requests.post('https://chartink.com/screener/process', 
                               cookies=cookies, headers=headers, json=json_data, timeout=30)
        response.raise_for_status()
        
        response_data = response.json()
        
        if 'data' in response_data:
            # Format the data for better consumption
            formatted_stocks = []
            for stock in response_data['data']:
                formatted_stocks.append({
                    'symbol': stock.get('nsecode', ''),
                    'name': stock.get('name', ''),
                    'close_price': stock.get('close', 0),
                    'volume': stock.get('volume', 0),
                    'market_cap': stock.get('market_cap', 0),
                    'sector': stock.get('sector', ''),
                    'screened_at': datetime.now().isoformat()
                })
            
            return formatted_stocks
        else:
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching swing trades: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

if __name__ == "__main__":
    # Test the function when run directly
    stocks = fetch_swing_trades()
    print(f"Found {len(stocks)} swing trading opportunities:")
    for i, stock in enumerate(stocks, 1):
        print(f"{i}. {stock['symbol']} - {stock['name']} - ₹{stock['close_price']}")