import requests
import pprint
import gmplot
import webbrowser


pp = pprint.PrettyPrinter(indent=2)


def valid_ip(ip):
    return ip.count('.') == 3 and  all(0<=int(num)<256 for num in ip.rstrip().split('.'))


def user_finder(page_language, page_name):

    url = "https://" + page_language + ".wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvlimit=500&titles=" + page_name + "&rvprop=user"
    request = requests.get(url)
    obj = request.json()
    lst = []
    for page_id in list(obj['query']['pages'].values()):
        users = page_id['revisions']
        for user in users:
            if valid_ip(user['user']):
                lst.append(user['user'])
    titles = []
    latitudes = []
    longitudes = []
    for ip in lst:
        url = "http://api.ipstack.com/" + ip + "?access_key=27f1532216d2f34e7a86c430cbf2d899"
        request = requests.get(url)
        obj = request.json()
        print(obj['country_name'])
        titles.append(obj['ip'])
        latitudes.append(obj['latitude'])
        longitudes.append(obj['longitude'])

    return titles, latitudes, longitudes


def map_drawer(titles, latitudes, longitudes):
    gmap = gmplot.GoogleMapPlotter(0, 0, 1)
    gmap.apikey = 'AIzaSyDQR82Mz9Bol-NtCltQ4SCKATneJV26CjQ'
    gmap.scatter(
        lats=latitudes,
        lngs=longitudes,
        s=10,
        color='red',
        title=titles
    )
    gmap.draw('gmplot.html')
    print("Выполнение завершено, карта доступна из файла gmplot.html")


def heatmap_drawer(titles, latitudes, longitudes):
    gmap = gmplot.GoogleMapPlotter(0, 0, 1)
    gmap.apikey = 'AIzaSyDQR82Mz9Bol-NtCltQ4SCKATneJV26CjQ'
    gmap.heatmap(
        lats=latitudes,
        lngs=longitudes,
        radius=50,
        # weights=[5, 1, 1, 1, 3, 1],
        gradient=[(0, 0, 255, 0), (0, 255, 0, 0.9), (255, 0, 0, 1)]
    )

    gmap.draw('heatmap.html')


print('Пожалуйста, выберите версию википедии:\n(1) Англоязычная\n(2) Русскоязычная')
while True:
    try:
        number1 = int(input('Ваш выбор: '))
        if number1 < 1 or number1 > 3:
            raise ValueError
        break
    except ValueError:
        print("Выберите 1 или 2.")
page_language = "en"
if number1 == 1: page_language = "en"
elif number1 == 2: page_language = "ru"

print('Пожалуйста, введите название статьи википедии, для которой необходимо построить карту')
page_name = str(input())
titles, latitudes, longitudes = user_finder(page_language, page_name)
map_drawer(titles, latitudes, longitudes)
heatmap_drawer(titles, latitudes, longitudes)






