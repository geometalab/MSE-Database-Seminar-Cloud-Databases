import urllib.request
import threading

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
prefix = 'https://s3.amazonaws.com/nyc-tlc/trip+data/'
body = '_tripdata_2015-'
suffix = '.csv'
taxi_types = ['yellow', 'green']


def download_file(file_name):
    url = prefix + file_name
    print(url)
    urllib.request.urlretrieve(url, file_name)


file_names = []

for month in months:
    for taxi_type in taxi_types:
        file_names.append(taxi_type + body + month + suffix)

threads = [threading.Thread(target=download_file, args=(file_name,)) for file_name in file_names]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
