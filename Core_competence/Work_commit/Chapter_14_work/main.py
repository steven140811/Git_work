import Route_api
import preprocessing_location
import pandas as pd

# 下面这个部分是为了在命令行或者Cell中执行命令 程序可以知道参数要传到哪
import argparse 
parser = argparse.ArgumentParser()    
parser.add_argument('--site1', type=str, default='清华大学', help='site1')
parser.add_argument('--site2', type=str, default='798', help='site2')
parser.add_argument('--city', type=str, default='北京', help='city')
args = parser.parse_known_args()[0]
site1=args.site1
site2=args.site2
city=args.city

# 找最近的地铁站
def get_nearest_subway(data,longitude1,latitude1):
    # 保存当前最小距离
    distance = float('inf')
    # longitude1,latitude1 = location[0],location[1]
    nearest = None
    for i in range(data.shape[0]):
        site1 = data.iloc[i]['name']
        # iloc = index  location 使用index来进行定位（行）
        longitude = float(data.iloc[i]['longitude'])
        latitude = float(data.iloc[i]['latitude'])
        temp = (float(longitude1) - longitude) ** 2 + (float(latitude1) - latitude) ** 2
        if temp < distance:
            distance = temp
            nearest = site1
    return nearest


def compute(site1,site2,city):
    longitude1,latitude1 = preprocessing_location.get_location(site1,city)
    longitude2,latitude2 = preprocessing_location.get_location(site2,city)
    # 加载所有的地铁线路
    data = pd.read_excel('./subway.xlsx')
    # 求site1， site2最近的地铁站
    start = get_nearest_subway(data,longitude1,latitude1)
    end = get_nearest_subway(data,longitude2,latitude2)
    print('{}最近的地铁站为{}'.format(site1,start))
    print('{}最近的地铁站为{}'.format(site2,end))
    shortest_path = Route_api.compute(start,end)
    if site1 != start:
        shortest_path.insert(0,site1)
    if site2 != end:
        shortest_path.append(site2)
    print('从{} => {}的最短路径为: {}'.format(site1,site2,str(shortest_path).replace('[','').replace(']','')))
    
if __name__ == '__main__':

#     print('city:', args.city, type(args.city))
#     print('site1:', args.site1, type(args.site1))
#     print('site2:', args.site2, type(args.site2))
#     city = '北京'        
#     site1 = '清华大学'
#     site2 = '北京大学'
    compute(site1,site2,city)
    