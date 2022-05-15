from PySide2 import QtWidgets
import currency_converter

class App(QtWidgets.QWidget):
    def __init__ (self):
        super().__init__()
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("Currency converter")
        self.setup_ui()
        self.set_default_values()
        self.setup_css()
        self.setup_connections()
        self.resize(500, 55)

    def setup_ui(self):
        self.layout = QtWidgets.QHBoxLayout(self)  # type: ignore
        self.cbb_currencyFrom = QtWidgets.QComboBox()
        self.spn_montant = QtWidgets.QSpinBox()
        self.cbb_currencyTo = QtWidgets.QComboBox()
        self.spn_montantConverti = QtWidgets.QSpinBox()
        self.btn_inverser = QtWidgets.QPushButton("Reverse currencies")

        self.layout.addWidget(self.cbb_currencyFrom)
        self.layout.addWidget(self.spn_montant)
        self.layout.addWidget(self.cbb_currencyTo)
        self.layout.addWidget(self.spn_montantConverti)
        self.layout.addWidget(self.btn_inverser)

    def set_default_values(self):
        self.cbb_currencyFrom.addItems(sorted(list(self.c.currencies)))  # type: ignore
        self.cbb_currencyTo.addItems(sorted(list(self.c.currencies)))  # type: ignore
        self.cbb_currencyFrom.setCurrentText("CHF")
        self.cbb_currencyTo.setCurrentText("CHF")

        self.spn_montant.setRange(1, 1000000000)
        self.spn_montantConverti.setRange(1, 1000000000)

        self.spn_montant.setValue(100)
        self.spn_montantConverti.setValue(100)
    
    def setup_connections(self):
        self.cbb_currencyFrom.activated.connect(self.compute)  # type: ignore
        self.cbb_currencyTo.activated.connect(self.compute)  # type: ignore
        self.spn_montant.valueChanged.connect(self.compute)  # type: ignore
        self.btn_inverser.clicked.connect(self.reverser_currency)  # type: ignore

    def setup_css(self):
        self.btn_inverser.setStyleSheet("background-color: rgb(66, 73, 73);")  # type: ignore
        self.setStyleSheet("""
        background-color: rgb(98, 101, 103);
        color: rgb(240, 240, 240);
        """)

        


    def compute(self):
        montant = self.spn_montant.value()
        currency_from = self.cbb_currencyFrom.currentText()
        currency_to = self.cbb_currencyTo.currentText()

        try:
            resultat = self.c.convert(montant, currency_from, currency_to)
        except currency_converter.currency_converter.RateNotFoundError:
            print("The conversion did not work")
        else:
            self.spn_montantConverti.setValue(resultat)

    def reverser_currency(self):
        currency_from = self.cbb_currencyFrom.currentText()
        currency_to = self.cbb_currencyTo.currentText()
        self.cbb_currencyFrom.setCurrentText(currency_to)
        self.cbb_currencyTo.setCurrentText(currency_from)
        self.compute()

appli = QtWidgets.QApplication([])
win = App()
win.show()
appli.exec_()