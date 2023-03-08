import exchange_calendars as xcals
import datetime
import json
import pytz
import boto3

utc=pytz.UTC

def get_closest_session(calendar):
    today = datetime.date.today()
    date = today

    if not calendar.is_session(today):
        date =  calendar.previous_close(today).to_pydatetime().date()
    elif calendar.schedule.loc[str(today)].open.to_pydatetime() > datetime.datetime.now().replace(tzinfo=utc):
        date =  calendar.previous_close(today).to_pydatetime().date()
    
    return date

def handler(event, context):
    xnys = xcals.get_calendar("XNYS")
    xkrx = xcals.get_calendar("XKRX")

    xnyx_session = get_closest_session(xnys)
    xkrx_session = get_closest_session(xkrx)

    exchange_date = {}
    for ex in ['NYSE', 'NASDAQ', 'S&P500', 'AMEX']:
        exchange_date[ex] = str(xnyx_session)
    for ex in ['KOSPI', 'KONEX', 'KOSDAQ GLOBAL', 'KOSDAQ']:
        exchange_date[ex] = str(xkrx_session)

    lambda_client = boto3.client('lambda')
    function_names = ["get_live_price"]

    responses = []
    for function_name in function_names:
        response = lambda_client.update_function_configuration(
            FunctionName=function_name,
            Environment={'Variables': {exchange_date: json.dumps(exchange_date)}}
        )
        responses.append(response)


    return {
    'statusCode': 200,
    'headers' : {
        'Content-Type':'application/json'
    },
    'body': json.dumps(responses)
    }

