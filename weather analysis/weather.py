import requests, time, datetime

city_id = '707860'
type = 'hour'
start = '22/04/2016'
end = '23/04/2016'
cnt = 1
timestamp_start = int(time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y").timetuple()))
timestamp_end = int(time.mktime(datetime.datetime.strptime(end, "%d/%m/%Y").timetuple()))

APPID='cf75729ca97c6d827e62d692ffaa8f69'

url = 'http://api.openweathermap.org/data/2.5/history/city?id={id}&type=hour&start={start}&end={end}&APPID={APPID}'
url =  url.replace('{id}', city_id).replace('{start}', str(timestamp_start)).\
      replace('{end}', str(timestamp_end)).replace('{APPID}', str(APPID))
##url = 'http://api.openweathermap.org/data/2.5/history/city'
##data = {'id': city_id, 'APPID':APPID, 'end':timestamp_end, 'start':timestamp_start, 'type':type, 'cnt':1}
##resp = requests.post(url, data=data)

print url
resp = requests.get(url)
print resp.text
