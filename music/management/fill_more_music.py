# music/management/commands/fill_more_music.py
from django.core.management.base import BaseCommand
from music.models import Genre, Artist, Album, Track

class Command(BaseCommand):
    help = 'Add more tracks to the database'

    def handle(self, *args, **options):
        # Genres
        alt_rock, _ = Genre.objects.get_or_create(name='Alternative Rock')
        indie_pop, _ = Genre.objects.get_or_create(name='Indie Pop')
        indie_rock, _ = Genre.objects.get_or_create(name='Indie Rock')
        pop, _ = Genre.objects.get_or_create(name='Pop')
        hiphop, _ = Genre.objects.get_or_create(name='Hip-Hop')
        soul, _ = Genre.objects.get_or_create(name='Soul')
        glam_rock, _ = Genre.objects.get_or_create(name='Glam Rock')
        self.stdout.write('Genres ready')

        # Artists
        orion, _ = Artist.objects.get_or_create(name='The Orion Experience')
        kt, _ = Artist.objects.get_or_create(name='KT Tunstall')
        mother, _ = Artist.objects.get_or_create(name='Mother Mother')
        tally, _ = Artist.objects.get_or_create(name='Tally Hall')
        will, _ = Artist.objects.get_or_create(name='Will Wood')
        drapht, _ = Artist.objects.get_or_create(name='Drapht')
        rex, _ = Artist.objects.get_or_create(name='Rex Orange County')
        scissor, _ = Artist.objects.get_or_create(name='Scissor Sisters')
        self.stdout.write('Artists ready')

        # Tracks
        t1, _ = Track.objects.get_or_create(title='The Cult of Dionysus', artist=orion)
        t1.genre.add(alt_rock, indie_pop)

        t2, _ = Track.objects.get_or_create(title='Suddenly I See', artist=kt)
        t2.genre.add(pop, indie_pop)

        t3, _ = Track.objects.get_or_create(title='Bit By Bit', artist=mother)
        t3.genre.add(indie_rock)

        t4, _ = Track.objects.get_or_create(title='&', artist=tally)
        t4.genre.add(indie_pop)

        t5, _ = Track.objects.get_or_create(title='Memento Mori: the most important thing in the world', artist=will)
        t5.genre.add(alt_rock)

        t6, _ = Track.objects.get_or_create(title='Model Plane', artist=drapht)
        t6.genre.add(hiphop)

        t7, _ = Track.objects.get_or_create(title='Never Enough', artist=rex)
        t7.genre.add(indie_pop, soul)

        t8, _ = Track.objects.get_or_create(title='Intermission', artist=scissor)
        t8.genre.add(glam_rock, pop)

        self.stdout.write(self.style.SUCCESS('✅ 8 tracks added!'))