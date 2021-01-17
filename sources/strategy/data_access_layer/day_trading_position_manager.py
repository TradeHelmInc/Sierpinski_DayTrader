import pyodbc
from sources.framework.business_entities.securities.security import *
from sources.strategy.strategies.day_trader.business_entities.day_trading_position import *


_CS_SEC_TYPE = "CS"

_id=0
_symbol=1
_shares_quantity=2
_active=3
_exchange=4
_security_type=5
_routing=6
_open=7
_long_signal=8
_short_signal=9
_signal_type=10
_signal_desc=11

class DayTradingPositionManager():

    #region Constructors

    def __init__(self, connectionString):
        self.ConnParams = {}

        self.i = 0
        self.connection = pyodbc.connect(connectionString)

    #endregion

    #region Private Methods

    def GetSecurityTypeFromStrSecType(self,strSecType):

        if strSecType==_CS_SEC_TYPE:
            return SecurityType.CS
        else:
            raise Exception("Unknown security type {0}".format(strSecType))

    def GetStrSecurityTypeFromSecType(self, secType):

        if secType ==  SecurityType.CS:
            return _CS_SEC_TYPE
        else:
            raise Exception("Unknown security type {0}".format(secType))

    def BuildSecurity(self,row):
        return Security(Symbol=row[_symbol],
                        Exchange=row[_exchange],
                        SecType=self.GetSecurityTypeFromStrSecType(row[_security_type])
                       )

    def BuildDayTradingPosition(self, row,security):
        return DayTradingPosition(
            id=int(row[_id]),
            security=security,
            shares=int(row[_shares_quantity]),
            active=bool(row[_active]),
            open=bool(row[_open]),
            routing=bool(row[_routing]),
        )

    #endregion

    #region Public Methods

    def PersistDayTradingPosition(self, dayTradingPosition):

        with self.connection.cursor() as cursor:
            params = (dayTradingPosition.Id, dayTradingPosition.Security.Symbol,
                      self.GetStrSecurityTypeFromSecType(dayTradingPosition.Security.SecurityType),
                      dayTradingPosition.Security.Exchange,
                      int(dayTradingPosition.SharesQuantity),
                      bool(dayTradingPosition.Active),
                      bool(dayTradingPosition.Routing),
                      bool(dayTradingPosition.Open))

            cursor.execute("{CALL PersistDayTradingPosition (?,?,?,?,?,?,?,?)}", params)
            self.connection.commit()

    def GetDayTradingPositions(self):
        datTradingPositions=[]
        with self.connection.cursor() as cursor:
            params = (True,None)
            cursor.execute("{CALL GetDayTradingPositions (?,?)}", params)

            for row in cursor:
                sec = self.BuildSecurity(row)
                dayTradingPos = self.BuildDayTradingPosition(row,sec)
                datTradingPositions.append(dayTradingPos)

        return datTradingPositions

    def GetDayTradingPosition(self,symbol):

        dayTradingPos = None

        with self.connection.cursor() as cursor:
            params = (True,symbol)
            cursor.execute("{CALL GetDayTradingPositions (?,?)}", params)

            for row in cursor:
                sec = self.BuildSecurity(row)
                dayTradingPos = self.BuildDayTradingPosition(row,sec)


        return dayTradingPos

    #endregion


