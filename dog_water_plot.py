import paramiko
from datetime import datetime
import matplotlib.pyplot as plt
import numpy

dates = []
converted_dates = []
times = []
# values = []
str = ""
str2 = ""
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.1.189', username='pi', password='raiderkozmo')
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('cat Dog_Water_Data.csv')
for line in ssh_stdout:
    dt = line.split(',', 1)[0]
    val = line.split(',', 1)[1]
    val = val.rsplit()
    dt = str2.join(dt)
    dates.append(dt)
    val = str.join(val)
    times.append(float(val))
    # values.append(line)

for d in dates:
    converted_dates.append(datetime.strptime(d, '%m-%d-%Y'))
arr1 = numpy.asarray(converted_dates)
arr2 = numpy.asarray(times)

# plt.scatter(converted_dates, times)
# plt.plot(converted_dates, times)
# plt.grid(b=True, which='major')
# bottom, top = plt.ylim()
# plt.ylim(bottom=0, top=top + .5)
#
# z = numpy.polyfit(dates, times, 1)
# p = numpy.poly1d(z)
# pylab.plot(x,p(x),"r--")
# plt.show()

plt.bar(dates, times)
plt.show()