import pandas
import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import smtplib

# your api here
API_KEY = "your api key"

API_Nomics = "your api here"


def getCryptoRates(currencyName='INR', assets='BTC,ETH,XRP'):
    url = 'https://api.nomics.com/v1/currencies/ticker'

    payload = {'key': API_Nomics, 'convert': currencyName, 'ids': assets, 'interval': '1d'}

    response = requests.get(url, params=payload)
    data = response.json()

    crypto, price, time = [], [], []

    for asset in data:
        crypto.append(asset['currency'])
        price.append(asset['price'])
        time.append(asset['price_timestamp'])

    raw_data = {
        'assets': crypto,
        'rates': price,
        'timestamp': time
    }

    df_cryptoRates = pd.DataFrame(raw_data)
    return df_cryptoRates


def setAlert(dataframe, asset, alert_price):
    user_email_func = input('Enter email where you want to be prompted:')
    cryptoValue = float(dataframe[dataframe['assets'] == asset]['rates'].item())

    price_info = f'{asset} : {cryptoValue}, Target: {alert_price}'

    if cryptoValue >= alert_price:
        print(price_info + '<< Target value reached')

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        print(user_email_func)
        server.login('your mail id', 'password for windows app here')

        subject_mail = f'Target value of {asset} has been achieved'

        body_mail = price_info
        msg = f"Subject: {subject_mail}\n\n{body_mail}"

        server.sendmail('your mail id', user_email_func, msg)

        print('Hey the email has been sent')

        server.quit()

    else:
        print(price_info)


def supportedCurrencies():
    url = f'https://api.coingecko.com/api/v3/coins'
    responseCrypto = requests.get(url)
    data = responseCrypto.json()

    cryptoNames = []

    for assets in data:
        cryptoNames.append(assets['id'])

    return cryptoNames


def cryptoChart(cryptoList, coinName_chart='bitcoin', currencyToCheck='inr', daysToTrack='30', interval='daily'):
    if coinName_chart in cryptoList:
        url = f'https://api.coingecko.com/api/v3/coins/{coinName_chart}/market_chart'
        payload = {'vs_currency': currencyToCheck, 'days': daysToTrack, 'interval': interval}
        resource = requests.get(url, payload)
        data = resource.json()

        timeStampList, priceList = [], []

        for price in data['prices']:
            timeStampList.append(datetime.datetime.fromtimestamp(price[0] / 1000))
            priceList.append(price[1])

        raw_data_map = {
            'timestamp': timeStampList,
            'price': priceList
        }

        df_chart = pandas.DataFrame(raw_data_map)
        return df_chart
    else:
        print('The crypto you entered is not supported check out our supported crypto list:')
        print(cryptoList)


def getYearlyrates(amount, currency, converted_currency, days):
    today_date = datetime.datetime.now()
    # Api takes only days so converting into days
    date_yearAgo = (today_date - datetime.timedelta(days=1 * days))

    url = f'https://api.exchangerate.host/timeseries'
    payload = {'base': currency, 'amount': amount, 'start_date': date_yearAgo.date(), 'end_date': today_date.date()}

    response_currency = requests.get(url, params=payload)
    data = response_currency.json()
    currency_hist = {}
    rates_history = []

    for item in data['rates']:
        current_date = item
        currency_rate = data['rates'][item][converted_currency]

        currency_hist[current_date] = [currency_rate]
        rates_history.append(currency_rate)

    pd_data = pd.DataFrame(currency_hist).transpose()
    pd_data.columns = ['Rate']
    pd.set_option('display.max_rows', None)
    print(pd_data)

    plt.plot(rates_history)
    plt.ylabel(f'{amount} {currency} to {converted_currency}')
    plt.xlabel('Days')
    plt.title(f'Current exchange rate for {amount} {currency} to {converted_currency} is {rates_history[-1]}')
    plt.show()


def get_crypto_data(currencyFun="USD", crypto="BTC", invert='true'):
    url = f'https://rest.coinapi.io/v1/exchangerate/{currencyFun}?invert={invert}'
    headers = {'X-CoinAPI-Key': API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()

    assets_names, assets_rates = [], []

    for asset in data['rates']:
        asset_id = asset['asset_id_quote']
        rate = asset['rate']

        assets_names.append(asset_id)
        assets_rates.append(rate)

    raw_data = {
        'assets': assets_names,
        'rates': assets_rates
    }
    df_coin = pd.DataFrame(raw_data)
    pd.set_option('display.max_rows', None)

    value = df_coin.loc[df_coin.assets == crypto, 'rates'].tolist()[0]
    print(df_coin)
    return value


# Execution starts here

want_to_continue = 1
while want_to_continue == 1:
    whatToDO = int(
        input('\nPlease Enter digit for what you want to do: \n 1->Currency Conversions \n 2->Crypto Price track \n '
              '3->Exit'))
    if whatToDO == 1:
        graphChahiye = int(
            input('Please enter what you want to do with currencies: \n 1-> Check for conversions \n 2->Track its '
                  'changes '))
        if graphChahiye == 1:

            CurrencyFrom = input('Enter the abbr of the currency to be converted:')
            CurrencyTo = input('Enter the abbr of currency to be checked:')
            money = input('Enter the amount to be converted:')
            getYearlyrates(money, CurrencyFrom, CurrencyTo, 1)

        elif graphChahiye == 2:

            CurrencyFrom = input('Enter the abbr of the currency to be converted:')
            CurrencyTo = input('Enter the abbr of currency to be checked:')
            daysTocheck = int(input('Enter the days to be checked(Max 1year):'))
            getYearlyrates(1, CurrencyFrom, CurrencyTo, daysTocheck)

        else:

            print("\nEnter a valid response")

    elif whatToDO == 2:

        invert_checker = int(input(
            'Enter What has to be done \n1-> Crypto -> Currency \n2-> Currency -> Crypto \n3-> Track Crypto changes '
            '\n4-> Set alerts'))

        if invert_checker == 1:
            Crypto = input('Enter the crypto currency abbreviation:')
            currency_entered = input('Enter the currency abbreviation:')

            valueToPrint = get_crypto_data(currency_entered, Crypto)
            print(f'\n The current price of 1 {Crypto} is {valueToPrint} in {currency_entered}')

        elif invert_checker == 2:
            Crypto = input('Enter the crypto currency abbreviation:')
            currency_entered = input('Enter the currency abbreviation:')

            valueToPrint = get_crypto_data(currency_entered, Crypto, 'false')
            print(f'\n The current price of 1 {currency_entered} is {valueToPrint} in {Crypto}')

        elif invert_checker == 3:

            cryptoOptionsAvailable = supportedCurrencies()
            print('here are the list of currencies that you can track:', cryptoOptionsAvailable)
            Crypto = input('Enter the crypto currency (type them same as shown above):')
            currency_entered = input('Enter the currency abbreviation (in small):')
            daysTocheck = input('Enter the days to be checked (enter max for all data):')
            printThisPlease = cryptoChart(cryptoOptionsAvailable, Crypto, currency_entered, daysTocheck)
            print(printThisPlease)
            printThisPlease.plot(y='price', x='timestamp')
            plt.ylabel(f'{Crypto} to {currency_entered}')
            plt.xlabel('Days')
            plt.title(f'exchange graph for {Crypto} to {currency_entered}')
            plt.show()

        elif invert_checker == 4:
            coinName = input('Enter the crypto abbreviation you want to set alert for:')
            currencyNameEntered = input('Enter the currency abbreviation you  want to check:')
            alertPrice = float(input('Enter the price above which you want to be alerted:'))
            df = getCryptoRates(currencyNameEntered, assets=coinName)
            setAlert(df, coinName, alertPrice)

        else:
            print('\nEnter a valid response')

    elif whatToDO == 3:
        break
    else:
        print("\nEnter a valid response")
