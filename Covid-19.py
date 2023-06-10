import pandas as pd
import requests
from datetime import datetime
import time

def send_slack_message(webhook_url,message):
    payload = {'text':message}
    response = requests.post(webhook_url,json=payload)
    if response.status_code == 200:
        print("Message sent successfully !!!")
    else:
        print("Failed to send message. Error:{respose.status_code}")

def generate_monthly_summary(dataframe,month):
    top_3_states= dataframe.groupby('state')['deaths'].sum().nlargest(3)
    total_deaths = dataframe['deaths'].sum()
    summary =f"Top 3 states with the highest number of COVID-19 deaths for the month of {month}\n" 
    summary += f"Month - {month}\n\n"

    for i,(state,deaths) in enumerate(top_3_states.items()):
        death_percentage = (deaths / total_deaths) * 100
        summary += f"State #{i+1} ({state}) - {deaths} deaths, {death_percentage: .2f}% of total US deaths\n"
    summary += f"\nTotal US Deaths : {total_deaths}"
    return summary

#Read the Dataset
df = pd.read_excel('C:\\Users\\sathish\\Downloads\\covid-19-state-level-data.xlsx')

#Convert the date column to datetime format
df['date'] = pd.to_datetime(df['date'])

#Set the interval (in seconds between sending messages)
interval = 5 

#Filter data for the desired months
months = ['March','April','May','June']

#Iterate over the desired months and send the summaries 
for month in months:
    filtered_df = df[df['date'].dt.month == months.index(month)+3]
    monthly_summary = generate_monthly_summary(filtered_df,month)
    send_slack_message('https://hooks.slack.com/services/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',monthly_summary)
    time.sleep(interval)