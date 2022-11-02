from django.dispatch import Signal, receiver
from django.db.models.signals import post_save

ping_signal = Signal()


class SignalDemo(object):

    def ping(self):
        print('PING')
        ping_signal.send(sender=self.__class__, PING=True)


@receiver(signal=ping_signal)
def pong(**kwargs):
    if kwargs['PING']:
        print('PONG')


def get():
    pass



demo = SignalDemo()
demo.ping()
