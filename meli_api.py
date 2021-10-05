from os import link, name
import requests 
import pandas as pd
from matplotlib import pyplot as plt


CHORMECAST = 'https://api.mercadolibre.com/sites/MLA/search?q=chromecast&limit=50#json' 
APPLE_TV = 'https://api.mercadolibre.com/sites/MLA/search?q=TV Apple&limit=50#json'
AMZN = 'https://api.mercadolibre.com/sites/MLA/search?q=Amazon Fire TV&limit=50#json'
XIAOMI = 'https://api.mercadolibre.com/sites/MLA/search?q=Xiaomi%20MI%20TV&limit=50#json'
MELITEMS ='https://api.mercadolibre.com/items/'
           


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def databases(link):

    try:

        response = requests.get(link)

        if response.status_code == 200:

            database= pd.DataFrame(requests.get(link).json()['results'])
            return(database)
            #print(database.installments)

        else: 

            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:

        print(ve)


def manipulate(link):

    df= databases(link)

    avg_price= df.price.mean()
    total_stock= df.available_quantity.sum()

    df ['location'] = df.address.map(lambda x: x['city_name'])
    df ['index'] = df.index
    df_p_s= pd.DataFrame({'Id':df.id ,'Price': df.price, 'Stock': df.available_quantity})  




    return (avg_price, total_stock, df['location'], df_p_s )

def point_1():

    google_market= manipulate(CHORMECAST)[2]
    apple_market = manipulate(APPLE_TV)[2]
    xiaomi_market= manipulate(XIAOMI)[2]
    amazon_market= manipulate(AMZN)[2]



    series_brand = pd.Series(['Chromecast', 'Apple TV', 'MI TV', 'Amazon Fire'])
    series_prices= pd.Series([manipulate(CHORMECAST)[0],manipulate(APPLE_TV)[0],manipulate(XIAOMI)[0],manipulate(AMZN)[0]])
    series_stock = pd.Series([manipulate(CHORMECAST)[1],manipulate(APPLE_TV)[1],manipulate(XIAOMI)[1],manipulate(AMZN)[1]])
    #series_cities = pd.Series([manipulate(CHORMECAST)[2],manipulate(APPLE_TV)[2],manipulate(XIAOMI)[2],manipulate(AMZN)[2]])


    df_prices = pd.DataFrame({'Productos': series_brand, 'Precio Promedio': series_prices})
    df_stock  = pd.DataFrame({'Productos': series_brand, 'Stock': series_stock})
    df_market = pd.DataFrame({'Chromecast':google_market, 'Apple TV':apple_market,"Mi Tv": xiaomi_market, 'Amazon Fire':amazon_market})
    #df_market.replace({'CAPITAL FEDERAL': 'CABA', 'Capital Federal': 'CABA' , 'C.A.B.A':'CABA', 'Palermo Hollywood': 'Palermo','PALERMO HOLLYWOOD': 'Palermo' })
    #df_global= pd.concat()


    print(f'La tabla promedio de precios es \n \n {df_prices} \n \n')
    print(f'La tabla stock es \n \n {df_stock} \n \n')
    print(f'La tabla de localidades es \n \n {df_market} \n \n')

    df_market.to_csv(f'locations.csv',sep='|',index=False, encoding= 'utf-8')

def point_2(df, name):

    """#dataframes = [manipulate(CHORMECAST)[3],manipulate(APPLE_TV)[3],manipulate(XIAOMI)[3],manipulate(AMZN)[3]]

    df =  manipulate(CHORMECAST)[3]
    
    print(df)
    #for df in dataframes:   

    #for row in df.itertuples():
    #for index, row in df.iterrows():

    for index, i in enumerate(df['Id']):
           
            #print(df)
            #print(index,row)
            #print(row.Id)
            print(index)


            if index==0:
                json_get = requests.get('https://api.mercadolibre.com/items/'+i).json()
                df = pd.DataFrame(requests.get('https://api.mercadolibre.com/items/'+i).json()['sale_terms'])
                df['Id'] = json_get['id']
                df['Price'] = json_get['price']
                df['Stock'] = json_get['available_quantity']

            else:
                json_get = requests.get('https://api.mercadolibre.com/items/'+i).json()
                df_aux = pd.DataFrame(requests.get('https://api.mercadolibre.com/items/'+i).json()['sale_terms'])
                df_aux['Id'] = json_get['id']
                df_aux['Price'] = json_get['price']
                df_aux['Stock'] = json_get['available_quantity']
                    
                    
                df = pd.concat([df,df_aux],axis=0)
                print(df)"""


    """ df = pd.DataFrame(requests.get("https://api.mercadolibre.com/sites/MLA/search?q=chromecast&limit=50#json").json()['results'])
    df['amount'] = df.installments.map(lambda x: x['amount'])
    df['rate'] = df.installments.map(lambda x: x['rate'])"""

    
    for indx, i in enumerate(df['Id']):

        print(indx)

        if indx==0:
            json_get = requests.get("https://api.mercadolibre.com/items/"+i).json()
            df = pd.DataFrame(requests.get("https://api.mercadolibre.com/items/"+i).json()['sale_terms'])
            df['Id'] = json_get['id']
            df['Price'] = json_get['price']
            df['available_quantity'] = json_get['available_quantity']

        else:
            json_get = requests.get("https://api.mercadolibre.com/items/"+i).json()
            df_aux = pd.DataFrame(requests.get("https://api.mercadolibre.com/items/"+i).json()['sale_terms'])
            df['Id'] = json_get['id']
            df['Price'] = json_get['price']
            df['available_quantity'] = json_get['available_quantity']
            
            df = pd.concat([df,df_aux],axis=0)
            df.to_csv(f'{name}_process.csv',sep='|',index=False, encoding= 'utf-8')

def run():

    point_1()
    
    #Se que lo ideal aqui es utilizar un bucle


    point_2(manipulate(CHORMECAST)[3], 'chromecast')
    point_2(manipulate(APPLE_TV)[3], 'apple_tv')
    point_2(manipulate(AMZN)[3], 'amazon_fire')
    point_2(manipulate(XIAOMI)[3], 'xiaomi_mi')




if __name__=='__main__':

    run()