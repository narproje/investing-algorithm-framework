from investing_algorithm_framework.core.data_providers import \
    AbstractDataProvider
from investing_algorithm_framework.core.strategies import Strategy


class MyStrategy(Strategy):
    on_tick_method_called = False
    on_quote_method_called = False
    on_order_book_method_called = False

    def on_tick(self, data):
        MyStrategy.on_tick_method_called = True

    def on_quote(self, data):
        MyStrategy.on_quote_method_called = True

    def on_order_book(self, data):
        MyStrategy.on_order_book_method_called = True


class MyStrategyTwo(Strategy):

    def on_tick(self, data):
        pass


class DataProvider(AbstractDataProvider):
    registered_strategies = [MyStrategy()]

    def extract_quote(self, data):
        return data

    def extract_order_book(self, data):
        return data

    def extract_tick(self, data):
        return data

    def get_data(self):
        return 'tick data'


class DataProviderTwo(AbstractDataProvider):

    def extract_quote(self, data):
        return data

    def extract_order_book(self, data):
        return data

    def extract_tick(self, data):
        return data

    def get_data(self):
        return 'tick data'


def test() -> None:
    data_provider = DataProvider()
    data_provider.provide_data()

    assert MyStrategy.on_tick_method_called
    assert MyStrategy.on_quote_method_called
    assert MyStrategy.on_order_book_method_called


def test_registration() -> None:
    data_provider = DataProviderTwo()
    data_provider.register_strategy(MyStrategy())

    assert len(data_provider.registered_strategies) == 1

    data_provider.register_strategy(MyStrategyTwo())

    assert len(data_provider.registered_strategies) == 2





