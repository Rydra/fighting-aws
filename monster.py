from melange import DriverManager
from melange.messaging.exchange_message_publisher import ExchangeMessagePublisher

DriverManager.instance().use_driver(driver_name='aws')

publisher = ExchangeMessagePublisher('dev-superbattle')

publisher.publish({
    'amount': 20
}, 'DamageDealtToHero')

print('Gñeeee, die you fool!')