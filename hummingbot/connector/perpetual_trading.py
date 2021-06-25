from decimal import Decimal
from typing import Dict, List
from hummingbot.core.event.events import PositionMode, FundingInfo, PositionSide
from hummingbot.connector.derivative.position import Position


NaN = float("nan")
s_decimal_NaN = Decimal("nan")
s_decimal_0 = Decimal(0)


class PerpetualTrading:
    """
    A base class (interface) that defines what perpetual trading is for Hummingbot.
    """

    def __init__(self):
        self._account_positions: Dict[str, Position] = {}
        self._position_mode: PositionMode = PositionMode.ONEWAY
        self._leverages: Dict[str, int] = {}
        self._funding_info: Dict[str, FundingInfo] = {}
        self._funding_payment_span: List[int] = [0, 0]

    @property
    def account_positions(self) -> Dict[str, Position]:
        """
        Returns a dictionary of current active open positions
        """
        return self._account_positions

    def position_key(self, trading_pair: str, side: PositionSide = None) -> str:
        """
        Returns a key to a position in account_positions. On OneWay position mode this is the trading pair.
        On Hedge position mode this is a combination of trading pair and position side
        :param trading_pair: The market trading pair
        :param side: The position side (long or short)
        :return: A key to the position in account_positions dictionary
        """
        if self._position_mode == PositionMode.ONEWAY:
            return trading_pair
        elif self._position_mode == PositionMode.HEDGE:
            return f"{trading_pair}{side.name}"

    @property
    def funding_payment_span(self) -> List[int]:
        """
        Time span(in seconds) before and after funding period when exchanges consider active positions eligible for
        funding payment.
        :return: a list of seconds (before and after)
        """
        return self._funding_payment_span

    @property
    def position_mode(self) -> PositionMode:
        return self._position_mode

    @position_mode.setter
    def position_mode(self, value: PositionMode):
        """
        Sets position mode for perpetual trading, a child class might need to override this to set position mode on
        the exchange
        :param value: the position mode
        """
        self._position_mode = value

    def get_leverage(self, trading_pair: str) -> int:
        """
        Gets leverage level of a particular market
        :param trading_pair: the market trading pair
        :return: leverage level
        """
        return self._leverages[trading_pair]

    def set_leverage(self, trading_pair: str, leverage: int = 1):
        """
        Sets leverage level, e.g. 2x, 10x, etc..
        A child class may need to override this to set leverage level on the exchange
        :param trading_pair: the market trading pair
        :param leverage: leverage to be used
        """
        self._leverages[trading_pair] = leverage

    def supported_position_modes(self) -> List[PositionMode]:
        """
        Returns a list of position modes supported by the connector
        """
        raise NotImplementedError

    def get_funding_info(self, trading_pair: str) -> FundingInfo:
        """
        Returns funding information
        :param trading_pair: the market trading pair
        :return: funding info
        """
        return self._funding_info[trading_pair]
