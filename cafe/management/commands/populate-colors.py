from django.core.management.base import (BaseCommand,
                                        CommandError)
from cafe.models import Color

colors = ['pink', 'orange', 'green', 'red', 'white',
            'yellow', 'blue', 'gold', ]

class Command(BaseCommand):
    help = 'Populates few colors into the database'

    def handle(self, *args, **options):
        for color in colors:
            Color(name=color, selected=True).save()
        self.stdout.write(self.style.SUCCESS( 'Colors Successfully populated' ))
        