import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_page_content(request_url):
    #得到页面内容
    header={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(request_url,headers=header,timeout=10)
    content = html.text
    # print(content)
    # 通过content创建BS对象
    # html.parser是bs自带的html解析器
    soup = BeautifulSoup(content,'html.parser',from_encoding='utf-8')
    return soup

def content_analysis():
    request_url = 'https://ditie.mapbar.com/beijing_line/'
    soup = get_page_content(request_url)

    # 解析内容
    subways = soup.find_all('div',class_='station')
    df = pd.DataFrame(columns=['name','site'])
    for subway in subways:
        # 得到线路名称
        route_name = subway.find('strong',class_='bolder').text
        # print('routename = ',route_name)
        # 找到该线路中每一站的名称
        routes = subway.find('ul')
        routes = routes.find_all('a')
        for route in routes:
            # name 地铁站名 site 线路名
            temp = {'name':route.text,'site':route_name}
            # print('route = ',route.text)
            df = df.append(temp,ignore_index=True)

    # print(df)        
    df['city'] = '北京'
    df.to_excel('./subway.xlsx',index=False)

# 获取经度longitude 纬度latitude
def get_location(keyword,city):
    header={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    request_url = 'http://restapi.amap.com/v3/place/text?key=f839aebd38cd68cc4802c99b45298674&keywords=' + keyword + '&types=&city=' + city + '&children=1&offset=1&page=1&extensions=all'
    data = requests.get(request_url,headers=header)
    data.encoding = 'utf-8'
    data = data.text
    # print(data)
    # "location":"116.337581,39.993138"
    # .*具有贪婪的性质，首先匹配到不能匹配为止
    # 。*？ 则相反，一个匹配以后，就可以继续后面的匹配
    pattern = 'location":"(.*?),(.*?)"'
    # 获取经纬度
    '''
        IndexError                                Traceback (most recent call last)
    <ipython-input-9-dee0fef02142> in <module>
         22 df['longitude'],df['latitude'] = None, None
         23 for index,row in df.iterrows():
    ---> 24     longitude,latitude = get_location(row['name'],row['city'])
         25     df.iloc[index]['longitude'] = longitude
         26     df.iloc[index]['latitude'] = latitude

    <ipython-input-9-dee0fef02142> in get_location(keyword, city)
         15     # 获取经纬度
         16     result = re.findall(pattern,data)
    ---> 17     return result[0][0],result[0][1]
         18 
         19 get_location('五道口站','北京')

    IndexError: list index out of range
    
    此错误是由于高德地图API中没有"石门站" 而是"石门"
    所以下面要加try except
    '''
    result = re.findall(pattern,data)
    try:
        return result[0][0],result[0][1]
    except:
        return get_location(keyword.replace('站',''),city)   

def work():
    
    df = pd.read_excel('./subway.xlsx')
    df['longitude'],df['latitude'] = None, None
    for index,row in df.iterrows():
        longitude,latitude = get_location(row['name'],row['city'])
        df.iloc[index]['longitude'] = longitude
        df.iloc[index]['latitude'] = latitude
        # print(longitude,latitude)

    get_location('五道口站','北京')
    df.to_excel('./subway.xlsx',index=False)   