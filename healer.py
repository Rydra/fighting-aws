from melange import DriverManager
from melange.messaging.exchange_message_publisher import ExchangeMessagePublisher

DriverManager.instance().use_driver(driver_name='aws')

publisher = ExchangeMessagePublisher('dev-superbattle')

publisher.publish({
    'amount': 40
}, 'HeroHealthRestored')

print('Here comes justice! I heal you!')