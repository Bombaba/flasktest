import feedparser
import datetime
import json
import os
import requests
import flask as fl

port = int(os.getenv('PORT', 8000))

DEFAULTS = {
    'publication': 'BBC',
    'city': 'London,UK',
    'currency_from': 'GBP',
    'currency_to': 'USD',
}

app = fl.Flask(__name__)

RSS_FEEDS = {
    'BBC': "http://feeds.bbci.co.uk/news/rss.xml",
    'CNN': "http://rss.cnn.com/rss/edition.rss",
    'FOX': "http://feeds.foxnews.com/foxnews/latest",
    'IOL': "http://www.iol.co.za/cmlink/1.640"
}

def get_news(query):
    if not query or query.upper() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.upper()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return {'publication': publication, 'entries': feed['entries']}

def get_weather(query):
    payload = {
        'appid': '0c743ad276fa15e22ce93c6899364130',
        'q': query or DEFAULTS['city'],
        'units': 'metric',
    }
    api_url = "http://api.openweathermap.org/data/2.5/weather"
    res = requests.get(api_url, params=payload)
    weather = None
    if res.status_code == 200:
        data = json.loads(res.text)
        weather = {
            'description': data['weather'][0]['description'],
            'temperature': data['main']['temp'],
            'city': f"{data['name']}, {data['sys']['country']}",
        }
    return weather

def get_currency(frm, to):
    payload = {
        'app_id': '8e95d6f316594963b1f11505e5fe0dd5',
    }
    api_url = "https://openexchangerates.org/api/latest.json"
    res = requests.get(api_url, params=payload)
    if res.status_code == 200:
        if not frm:
            frm = DEFAULTS['currency_from']
        if not to:
            to = DEFAULTS['currency_to']
        frm = frm.upper()
        to = to.upper()
        rates = json.loads(res.text)['rates']
        from_rate = rates.get(frm) or rates[DEFAULTS['currency_from']]
        to_rate = rates.get(to) or rates[DEFAULTS['currency_to']]
        return {
            'all': rates.keys(),
            'from': frm,
            'to': to,
            'rate': to_rate / from_rate,
        }
    else:
        return {'all': "", 'from': "", 'to': "", 'rate': 0}

def get_value_with_fallback(key):
    return fl.request.args.get(key) or fl.request.cookies.get(key)

@app.route("/")
def home():
    articles = get_news(get_value_with_fallback('publication'))
    weather = get_weather(get_value_with_fallback('city'))
    currency = get_currency(
        get_value_with_fallback('currency_from'),
        get_value_with_fallback('currency_to')
    )
    response = fl.make_response(
        fl.render_template(
            "home.html", articles=articles,
            weather=weather, currency=currency,
        )
    )
    expires = datetime.datetime.now() + datetime.timedelta(days=7)
    response.set_cookie("publication", articles['publication'],
                        expires=expires)
    response.set_cookie("city", weather['city'],
                        expires=expires)
    response.set_cookie("currency_from", currency['from'],
                        expires=expires)
    response.set_cookie("currency_to", currency['to'],
                        expires=expires)
    return  response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)