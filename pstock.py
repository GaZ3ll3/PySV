from pandas.io.data import DataReader
import matplotlib.pyplot as plt
import datetime

google = DataReader("BAS", "google", datetime.datetime(2014, 6, 8),
    datetime.datetime(2014,6,11))

top = plt.subplot2grid((4,4), (0, 0), rowspan=3, colspan=4)
top.plot(google.index, google["Close"])
plt.title('Google Stock Price from 2007 - 2012')

bottom = plt.subplot2grid((4,4), (3,0), rowspan=1, colspan=4)
bottom.bar(google.index, google['Volume'])
#plt.title('Google Trading Volume in Millions')

plt.gcf().set_size_inches(15,8)

plt.show()
