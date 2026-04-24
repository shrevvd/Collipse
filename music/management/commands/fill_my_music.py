from django.core.management.base import BaseCommand
from music.models import Genre, Artist, Album, Track
from datetime import date

class Command(BaseCommand):

    def handle(self, *args, **options):
        # Жанры
        alt_rnb, _ = Genre.objects.get_or_create(name='Alternative R&B')
        indie_rock, _ = Genre.objects.get_or_create(name='Indie Rock')
        indie_pop, _ = Genre.objects.get_or_create(name='Indie Pop')
        synth_pop, _ = Genre.objects.get_or_create(name='Synth Pop')
        jpop, _ = Genre.objects.get_or_create(name='J-Pop')
        jrock, _ = Genre.objects.get_or_create(name='J-Rock')
        self.stdout.write('Жанры созданы')

        # Исполнители
        malcolm, _ = Artist.objects.get_or_create(name='Malcolm Todd')
        whity, _ = Artist.objects.get_or_create(name='Whitey')
        sheena, _ = Artist.objects.get_or_create(name='Sheena Ringo')
        chloe, _ = Artist.objects.get_or_create(name='Sir Chloe')
        lemon, _ = Artist.objects.get_or_create(name='Lemon Demon')
        self.stdout.write('Исполнители созданы')

        # Альбомы
        sweet_boy, _ = Album.objects.get_or_create(
            title='Sweet Boy',
            artist=malcolm,
            release_date=date(2024, 4, 5)
        )
        hot_ny_album, _ = Album.objects.get_or_create(
            title='Hot in NY',
            artist=malcolm,
            release_date=date(2023, 8, 25)
        )
        dinosaurchestra, _ = Album.objects.get_or_create(
            title='Dinosaurchestra',
            artist=lemon,
            release_date=date(2006, 7, 20)
        )
        party_favors, _ = Album.objects.get_or_create(
            title='Party Favors',
            artist=chloe,
            release_date=date(2020, 10, 23)
        )
        self.stdout.write('Альбомы созданы')

        # Треки
        # Malcolm Todd
        t1, _ = Track.objects.get_or_create(title='Earrings', artist=malcolm, album=sweet_boy)
        t1.genre.add(alt_rnb)
        t1.save()

        t2, _ = Track.objects.get_or_create(title='Hot in NY', artist=malcolm, album=hot_ny_album)
        t2.genre.add(alt_rnb)
        t2.save()

        # Sheena Ringo 
        t3, _ = Track.objects.get_or_create(title='Gate of Living', artist=sheena)
        t3.genre.add(jrock)
        t3.save()

        # Sir Chloe
        t4, _ = Track.objects.get_or_create(title='Michelle', artist=chloe)
        t4.genre.add(indie_rock)
        t4.save()

        t5, _ = Track.objects.get_or_create(title='Too Close', artist=chloe, album=party_favors)
        t5.genre.add(indie_rock)
        t5.save()

        # Lemon Demon
        t6, _ = Track.objects.get_or_create(title='Knife Fight', artist=lemon)
        t6.genre.add(indie_rock)
        t6.save()

        t7, _ = Track.objects.get_or_create(title='Bill Watterson', artist=lemon)
        t7.genre.add(indie_rock)
        t7.save()

        t8, _ = Track.objects.get_or_create(title='The Ultimate Showdown of Ultimate Destiny', artist=lemon, album=dinosaurchestra)
        t8.genre.add(indie_rock)
        t8.save()

        # Whitey
        t9, _ = Track.objects.get_or_create(title='Brief and Bright', artist=whity)
        t9.genre.add(indie_rock)
        t9.save()

        self.stdout.write(self.style.SUCCESS('Треки загружены'))