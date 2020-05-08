import speedtest
import temp

threads = None
# If you want to use a single threaded test
# threads = 1

s = speedtest.Speedtest()
s.get_best_server()
s.download(threads=threads)
s.upload(threads=threads)
s.results.share()

results_dict = s.results.dict()
print('Down: {}'.format(results_dict['download']/1000000))
print('Up: {}'.format(results_dict['upload']/1000000))
print('Ping: {}'.format(results_dict['ping']))


def get_file_location(filename):
    temp_dir = temp.tempdir()
    temp_dir = temp_dir.rsplit('\\', 1)[0]
    file_path = temp_dir + "/" + filename

    return file_path


file = open(get_file_location("speeddata.txt"), 'a+')
file.write(str(round((results_dict['download']) / 1000000, 2)) + ',' + str(round((results_dict['upload']) / 1000000, 2)) + ',' + str(round((results_dict['ping']), 2)) + ',' + str(results_dict['bytes_sent']) + ',' + str(results_dict['bytes_received']) + '\n')
file.close()
