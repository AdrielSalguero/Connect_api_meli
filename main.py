from os import link, name
import requests 
import pandas as pd
import json
from matplotlib import pyplot as plt


urls = {'CHORMECAST':'https://api.mercadolibre.com/sites/MLA/search?q=chromecast&limit=50#json', 
            'SMARTV': 'https://api.mercadolibre.com/sites/MLA/search?q=smart-tv-tv&limit=50#json',
            'AMAZON': 'https://api.mercadolibre.com/sites/MLA/search?q=AmazonFire=TV&limit=50#json',
            'XIAOMI': 'https://api.mercadolibre.com/sites/MLA/search?q=xiaomi-tv&limit=50#json'}         



#df = database[database['title'].str.contains('GOOGLE', case=False)]
def clean(df):

    df['state'] = df['seller_address'].apply(lambda x: x['state']['name'])
    df['city'] = df['seller_address'].apply(lambda x: x['city']['name'])
    df['seller']= df['seller'].apply(lambda x:x['nickname'])
    df=df[['id','title','price','available_quantity','city','state','seller']]
    
    return df 


def transform(results,dataframe):
    rows = []
    for result in results:
        title = result.get('title')
        price = result.get('price')
        available_quantity = result.get('available_quantity')
        seller = result.get('seller',{}).get('nickname')
        city = result.get('seller_address',{}).get('city',{}).get('name')
        state = result.get('seller_address',{}).get('state',{}).get('name')
        
        rows.append([title, price, available_quantity, seller, city, state])
        
    return pd.DataFrame(rows, columns=['title', 'price', 'available_quantity', 'seller', 'city', 'state'])



dataframe = pd.DataFrame(columns =['title','price','available_quantity','seller','city','state'])                          

for clave,valor in urls.items():

    link=valor
    try:
        response = requests.get(link)
    
        if response.status_code == 200:
            # Tu código para obtener los datos
            print(link)
            data = response.json()
            results = data.get('results',[]) 
            cleaned_df= transform(results,dataframe)
            cleaned_df['Brand']= clave
            dataframe = dataframe.append(cleaned_df, ignore_index=True)
            
        else:
            raise ValueError(f'Error: {response.status_code}')
        
    except ValueError as ve:
        print(ve)
    
dataframe.to_csv('cleaned_from_get.csv')


'''
Trabaja con la funcion apply de pandas para la extraccion de los datos desde el link, pero no es lo que se pidio
dataframe = pd.DataFrame()
for clave,valor in urls.items():

    link=valor
    try:
        response = requests.get(link)
    
        if response.status_code == 200:
            # Tu código para obtener los datos
            df = pd.DataFrame(requests.get(link).json()['results'])
            cleaned_df= clean(df)
            cleaned_df['Brand']= clave
            dataframe= pd.concat([dataframe,cleaned_df])

        else:
            raise ValueError(f'Error: {response.status_code}')
        
    except ValueError as ve:
        print(ve)
    
dataframe.to_csv('cleaned.csv')'''