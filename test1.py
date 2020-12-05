# 提取城市的POI点信息并将其保存至CSV
import csv
import string
import urllib.request
import json
from urllib.parse import quote

# left_bottom = [120.89,31.83];  # 设置区域左下角坐标（百度坐标系）
left_bottom = [114.775983, 34.192911]
# right_top = [121.40,32.47]; # 设置区域右上角坐标（百度坐标系）
right_top = [122.852396, 38.318636]
part_n = 10  # 设置区域网格（10*10）
url0 = 'http://api.map.baidu.com/place/v2/search?'
x_item = (right_top[0]-left_bottom[0])/part_n  #经度变化单位长度
y_item = (right_top[1]-left_bottom[1])/part_n  #纬度变化单位长度
ak = 'Glg31GCbU4tHj6EF46GgeHBUKRiTTfnv' #百度地图api信令
n = 0 # 切片计数器

datacsv=open("fuwu10.csv", "a+", encoding="utf-8")
csvwriter = csv.writer(datacsv, dialect=("excel"))
# keywords = ['百货商场', '超市', '便利店', '商铺', '集市', '通讯营业厅', '邮局', '物流公司', '公用事业', '公园', '风景区', '动物园', '植物园', '游乐园', '文物古迹',
#             '度假村', '农家院', '休闲广场', '高等院校', '中学', '小学', '幼儿园', '特殊教育学校', '综合医院', '专科医院', '诊所', '药店', '飞机场', '火车站',
#             '长途汽车站', '公交车站', '公交线路', '港口', '服务区', '收费站', '银行', '', '信用社', '投资理财', '中央机构', '各级政府', '行政单位', '政治教育机构',
#             '福利机构', '高速公路出口', '高速公路入口', '机场出口', '机场入口', '车站出口', '车站入口', '岛屿', '山峰', '水系']
keywords = ['服务区']

for keyword in keywords:
    urlx = url0+'query='+keyword

    for i in range(part_n):
        for j in range(part_n):
            left_bottom_part = [left_bottom[0]+i*x_item, left_bottom[1]+j*y_item]  # 切片的左下角坐标
            right_top_part = [left_bottom_part[0]+x_item, left_bottom_part[1]+y_item]  # 切片的右上角坐标
            for k in range(20):
                # url = url0 + 'query=' + query + '&page_size=20&page_num=' + str(k) + '&scope=1&bounds=' + str(left_bottom_part[1]) + ',' + str(left_bottom_part[0]) + ','+str(right_top_part[1]) + ',' + str(right_top_part[0]) + '&output=json&ak=' + ak;
                url = urlx + '&page_size=20&page_num=' + str(k) + '&scope=1&bounds=' + str(left_bottom_part[1]) + ',' \
                      + str(left_bottom_part[0]) + ','+ str(right_top_part[1]) + ',' + str(right_top_part[0]) \
                      + '&output=json&ak=' + ak
                s=quote(url, safe=string.printable)
                data = urllib.request.urlopen(s)
                hjson = json.loads(data.read().decode('utf-8'))
                if hjson['message'] == 'ok':
                    results = hjson['results']
                    for m in range(len(results)):  # 提取返回的结果
                        csvwriter.writerow(list(results[m].values()))
            n += 1
            print('第', str(n), '个切片入库成功')
    csvwriter.writerow('\r\n')
