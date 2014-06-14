import sys, os
from PySide.QtCore import *
from PySide.QtGui import *

from pandas.io.data import DataReader
import datetime
import matplotlib
matplotlib.rcParams['backend.qt4'] = 'PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

from matplotlib.figure import Figure

import operator
import matplotlib.dates as mdates

from matplotlib.dates import  DateFormatter, WeekdayLocator, HourLocator, \
     DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo, candlestick,\
     plot_day_summary, candlestick2, plot_day_summary2

class StockView(QMainWindow):
    """docstring for StockView"""
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Pandas data processing with matplotlib visualization')
        self.setGeometry(0, 0, 1500, 800)

        # set menu
        self.create_StockView_Menu()

        # set canvas 
        self.create_StockView_MainFrame()

        # set status bar
        self.create_StockView_StatusBar()

        # set tool bar
        self.create_StockView_ToolBar()





    def save_StockView_Data(self):
        pass

    def save_StockView_Plot(self):
        pass


    def load_StockView_Watchlist(self):
        pass

    def calc_StockView_CCI(self):
        pass



    def time_StockView_setup(self):
        self.start_date = datetime.datetime(2014,5,1)
        self.end_date   = datetime.datetime(2014,6,12)

    def data_StockView_import(self):
        self.data = DataReader("GOOGL","google",self.start_date,self.end_date)

    # signal 

    def on_StockView_HoverOver(self):
        pass

    def on_StockView_ClickOn(self):
        pass

    def on_StockView_Plot(self):
        self.top_axes = self.figure.add_subplot(2,1,1)
        # self.top_axes.subplot2grid((4,4), (0,0), rowspan = 3, colspan = 4)
        self.top_axes.plot(
            self.data.index, self.data["High"],'y',
            # self.data.index, self.data["Close"],'r',
            # self.data.index, self.data["Open"],'g',
            # self.data.index, self.data["Low"],'b'
            )
        # self.top_axes.set_ylabel('Price', color='r')
        self.bottom_axes = self.top_axes.twinx()
        # self.bottom_axes = self.figure.add_subplot(2,1,1)
        # self.bottom_axes.subplot2grid((4,4), (3,0), rowspan = 1, colspan = 4)
        self.bottom_axes.bar(self.data.index, self.data["Volume"],
            alpha=0.05,
            color='k', label='Volume')
        self.bottom_axes.get_yaxis().set_visible(False)
        self.x_axes = self.top_axes.get_xaxis() # get the x-axis
        
        self.autoformat = self.x_axes.get_major_formatter() # the the auto-formatter

        self.autoformat.scaled[1./24] = '%H:%M'  # set the < 1d scale to H:M
        self.autoformat.scaled[1.0] = '%m-%d' # set the > 1d < 1m scale to Y-m-d
        self.autoformat.scaled[30.] = '%Y-%m' # set the > 1m < 1Y scale to Y-m
        self.autoformat.scaled[365.] = '%Y' # set the > 1y scale to Y

        self.top_axes.grid(True)

        self.top_axes.get_xaxis().set_visible(False)


        self.top_axes.autoscale_view()


        self.candle_axes = self.figure.add_subplot(2,1,2)

        self.candle_axes.get_xaxis().set_visible(False)

        candlestick2(self.candle_axes, self.data["Open"],self.data["Close"], 
            self.data["High"], self.data["Low"], width=0.6, colorup='g', colordown='r')


        plot_day_summary2(self.candle_axes, self.data["Open"],self.data["Close"], 
            self.data["High"], self.data["Low"])

        self.candle_axes.locator_params(tight=True)

        print self.data






        self.canvas.draw()




    def create_StockView_Action(self, text, slot=None, 
        shortcut=None,icon=None, tip=None,
        checkable=False,signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action
        

    def create_StockView_Menu(self):
        self.file_Menu = self.menuBar().addMenu("&File")
        load_Plot_Action = self.create_StockView_Action("&Save Figure",
            shortcut="Ctrl+S", slot=self.save_StockView_Plot, 
            tip="Save the plot")
        load_CSV_Action  = self.create_StockView_Action("&Save CSV",
            shortcut="Ctrl+D",slot=self.save_StockView_Data,
            tip="Save the data")
        quit_Action = self.create_StockView_Action("&Quit",
            shortcut="Ctrl+Q",slot=self.close,
            tip="Quit StockView")

        self.edit_Menu = self.menuBar().addMenu("&Edit")
        edit_Watchlist_Action = self.create_StockView_Action("&Edit Watchlist",
            shortcut="Ctrl+E",slot=self.load_StockView_Watchlist,
            tip="Edit Watchlist")

        self.calc_Menu = self.menuBar().addMenu("&Analysis")
        calc_CCI_Action = self.create_StockView_Action("&CCI",
            shortcut="Ctrl+W",slot=self.calc_StockView_CCI,
            tip="Calculate CCI")

        self.add_StockView_Action(self.file_Menu,
            (load_Plot_Action,None,load_CSV_Action,None,quit_Action))

        self.add_StockView_Action(self.edit_Menu,
            (edit_Watchlist_Action,))

        self.add_StockView_Action(self.calc_Menu,
            (calc_CCI_Action,))





    def create_StockView_MainFrame(self):
        # new widget
        self.main_Frame = QWidget()
        # Figure setup
        self.create_StockView_Canvas()
        # set parent
        self.canvas.setParent(self.main_Frame)

        # setup canvas data range
        self.time_StockView_setup()
        # import data from google or yahoo finance
        self.data_StockView_import()
        # plot data onto screen, need to change into callback
        self.on_StockView_Plot()


        # turn data into tableview
        self.create_StockView_TableView(data_list,header)
        # need a callback to refresh table

        hbox = QHBoxLayout()
        hbox.addWidget(self.table_view)
        hbox.addWidget(self.canvas)



        self.main_Frame.setLayout(hbox)

        self.setCentralWidget(self.main_Frame) 

    def create_StockView_StatusBar(self):
        pass

    def create_StockView_ToolBar(self):
        pass

    def create_StockView_Canvas(self):
        self.dpi = 85
        self.figure = Figure((10.0,6.0), dpi=self.dpi,
            facecolor=(1,1,1), edgecolor=(0,0,0))

        self.canvas = FigureCanvas(self.figure)

    def create_StockView_TableView(self, data_list, header):
        table_model = StockViewTableModel(self.main_Frame, data_list, header)
        self.table_view = QTableView()
        self.table_view.setModel(table_model)
        # set font
        font = QFont("Courier New", 14)
        self.table_view.setFont(font)
        # set column width to fit contents (set font first!)
        self.table_view.resizeColumnsToContents()
        # enable sorting
        self.table_view.setSortingEnabled(True)

    def create_StockView_Watchlist(self):
        pass

    def create_StockView_Database(self):
        pass


    def add_StockView_Action(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)


class StockViewTableModel(QAbstractTableModel):
    def __init__(self, parent, datalist, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.datalist = datalist
        self.header = header
    def rowCount(self, parent):
        return len(self.datalist)
    def columnCount(self, parent):
        return len(self.datalist[0])
    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.datalist[index.row()][index.column()]
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None
    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.datalist = sorted(self.datalist,
            key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.datalist.reverse()
        self.emit(SIGNAL("layoutChanged()"))
# the solvent data ...
header = ['Solvent Name', ' BP (deg C)', ' MP (deg C)', ' Density (g/ml)']
# use numbers for numeric data to sort properly
data_list = [
('ACETIC ACID', 117.9, 16.7, 1.049),
('ACETIC ANHYDRIDE', 140.1, -73.1, 1.087),
('ACETONE', 56.3, -94.7, 0.791),
('ACETONITRILE', 81.6, -43.8, 0.786),
('ANISOLE', 154.2, -37.0, 0.995),
('BENZYL ALCOHOL', 205.4, -15.3, 1.045),
('BENZYL BENZOATE', 323.5, 19.4, 1.112),
('BUTYL ALCOHOL NORMAL', 117.7, -88.6, 0.81),
('BUTYL ALCOHOL SEC', 99.6, -114.7, 0.805),
('BUTYL ALCOHOL TERTIARY', 82.2, 25.5, 0.786),
('CHLOROBENZENE', 131.7, -45.6, 1.111),
('CYCLOHEXANE', 80.7, 6.6, 0.779),
('CYCLOHEXANOL', 161.1, 25.1, 0.971),
('CYCLOHEXANONE', 155.2, -47.0, 0.947),
('DICHLOROETHANE 1 2', 83.5, -35.7, 1.246),
('DICHLOROMETHANE', 39.8, -95.1, 1.325),
('DIETHYL ETHER', 34.5, -116.2, 0.715),
('DIMETHYLACETAMIDE', 166.1, -20.0, 0.937),
('DIMETHYLFORMAMIDE', 153.3, -60.4, 0.944),
('DIMETHYLSULFOXIDE', 189.4, 18.5, 1.102),
('DIOXANE 1 4', 101.3, 11.8, 1.034),
('DIPHENYL ETHER', 258.3, 26.9, 1.066),
('ETHYL ACETATE', 77.1, -83.9, 0.902),
('ETHYL ALCOHOL', 78.3, -114.1, 0.789),
('ETHYL DIGLYME', 188.2, -45.0, 0.906),
('ETHYLENE CARBONATE', 248.3, 36.4, 1.321),
('ETHYLENE GLYCOL', 197.3, -13.2, 1.114),
('FORMIC ACID', 100.6, 8.3, 1.22),
('HEPTANE', 98.4, -90.6, 0.684),
('HEXAMETHYL PHOSPHORAMIDE', 233.2, 7.2, 1.027),
('HEXANE', 68.7, -95.3, 0.659),
('ISO OCTANE', 99.2, -107.4, 0.692),
('ISOPROPYL ACETATE', 88.6, -73.4, 0.872),
('ISOPROPYL ALCOHOL', 82.3, -88.0, 0.785),
('METHYL ALCOHOL', 64.7, -97.7, 0.791),
('METHYL ETHYLKETONE', 79.6, -86.7, 0.805),
('METHYL ISOBUTYL KETONE', 116.5, -84.0, 0.798),
('METHYL T-BUTYL ETHER', 55.5, -10.0, 0.74),
('METHYLPYRROLIDINONE N', 203.2, -23.5, 1.027),
('MORPHOLINE', 128.9, -3.1, 1.0),
('NITROBENZENE', 210.8, 5.7, 1.208),
('NITROMETHANE', 101.2, -28.5, 1.131),
('PENTANE', 36.1, ' -129.7', 0.626),
('PHENOL', 181.8, 40.9, 1.066),
('PROPANENITRILE', 97.1, -92.8, 0.782),
('PROPIONIC ACID', 141.1, -20.7, 0.993),
('PROPIONITRILE', 97.4, -92.8, 0.782),
('PROPYLENE GLYCOL', 187.6, -60.1, 1.04),
('PYRIDINE', 115.4, -41.6, 0.978),
('SULFOLANE', 287.3, 28.5, 1.262),
('TETRAHYDROFURAN', 66.2, -108.5, 0.887),
('TOLUENE', 110.6, -94.9, 0.867),
('TRIETHYL PHOSPHATE', 215.4, -56.4, 1.072),
('TRIETHYLAMINE', 89.5, -114.7, 0.726),
('TRIFLUOROACETIC ACID', 71.8, -15.3, 1.489),
('WATER', 100.0, 0.0, 1.0),
('XYLENES', 139.1, -47.8, 0.86)
]        

def main():
    try:
        app = QApplication(sys.argv)
    except RuntimeError:
        app = QApplication.instance()
    view = StockView()
    view.show()
    app.exec_()


if __name__ == "__main__":
    main()

        