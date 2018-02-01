from melange.messaging import ExchangeMessageConsumer, ExchangeListener, DriverManager
from melange.messaging.exchange_message_publisher import ExchangeMessagePublisher

DriverManager.instance().use_driver(driver_name='aws')

HERO = None

class Hero:
    def __init__(self):
        self.hp = 100

    @property
    def status(self):
        if self.hp <= 0:
            return 'DEAD'
        elif self.hp == 100:
            return 'ALIVE'
        elif self.hp > 100:
            return 'BEEFED'
        else:
            return 'WOUNDED'

    def damage(self, amount):
        self.hp -= amount

    def restore(self, amount):
        self.hp += amount

class HeroDamageReceptor(ExchangeListener):
    def process(self, event, **kwargs):
        HERO.damage(event['amount'])
        print('Arghhh, You\'ll pay in blood! (Remaining HP: {})'.format(HERO.hp))

    def listens_to(self):
        return ['DamageDealtToHero']


class HeroHealingReceptor(ExchangeListener):
    def process(self, event, **kwargs):
        HERO.restore(event['amount'])
        print('Wow, thanks for the healing, you saved my life! (Remaining HP: {})'.format(HERO.hp))
        if HERO.status in ['ALIVE', 'BEEFED']:
            print('Wow! I feel stronger than ever!')

    def listens_to(self):
        return ['HeroHealthRestored']


class NewHeroArrivesReceptor(ExchangeListener):
    def process(self, event, **kwargs):
        print('Finally! Reinforcements!')

    def listens_to(self):
        return ['NewHeroArrives']


consumer = ExchangeMessageConsumer('dev-hero', 'dev-superbattle')

publisher = ExchangeMessagePublisher('dev-superbattle')
publisher.publish({}, 'NewHeroArrives')

print('Here comes a new challenger!')

HERO = Hero()

consumer.subscribe(HeroDamageReceptor())
consumer.subscribe(HeroHealingReceptor())
consumer.subscribe(NewHeroArrivesReceptor())

while HERO.status != 'DEAD':
    print('I am waiting for you, evildoers!')
    consumer.consume_event()

print('Arghhhh... My time has arrived... *Ouch*, damn you, healer!')