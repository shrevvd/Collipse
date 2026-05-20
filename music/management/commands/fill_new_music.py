from django.core.management.base import BaseCommand
from music.models import Genre, Artist, Album, Track
from datetime import date

class Command(BaseCommand):
    help = 'Add new tracks'

    def handle(self, *args, **options):
        # Жанры
        jpop, _ = Genre.objects.get_or_create(name='J-Pop')
        jrock, _ = Genre.objects.get_or_create(name='J-Rock')
        electro_punk, _ = Genre.objects.get_or_create(name='Electro-Punk')
        vocaloid, _ = Genre.objects.get_or_create(name='Vocaloid')
        indie_pop, _ = Genre.objects.get_or_create(name='Indie Pop')
        pop, _ = Genre.objects.get_or_create(name='Pop')
        alt_rock, _ = Genre.objects.get_or_create(name='Alternative Rock')
        self.stdout.write('Жанры готовы')

        # Исполнители
        sheena, _ = Artist.objects.get_or_create(name='Sheena Ringo')
        msi, _ = Artist.objects.get_or_create(name='Mindless Self Indulgence')
        egoist_artist, _ = Artist.objects.get_or_create(name='Egoist')
        ghost, _ = Artist.objects.get_or_create(name='GHOST')
        halle, _ = Artist.objects.get_or_create(name='Halle Uchida')
        syudou_artist, _ = Artist.objects.get_or_create(name='syudou')
        meiko_artist, _ = Artist.objects.get_or_create(name='MEIKO')
        mikito, _ = Artist.objects.get_or_create(name='MikitoP feat. Hatsune Miku')
        menitrust, _ = Artist.objects.get_or_create(name='Men I Trust')
        gaga, _ = Artist.objects.get_or_create(name='Lady Gaga')
        gross, _ = Artist.objects.get_or_create(name='Grossstadtgeflüster')
        tally, _ = Artist.objects.get_or_create(name='Tally Hall')
        self.stdout.write('Исполнители готовы')

        # Альбомы
        single_sheena, _ = Album.objects.get_or_create(title='La velada legendaria - Single', artist=sheena, release_date=date(2025, 6, 25))
        if_album, _ = Album.objects.get_or_create(title='If', artist=msi, release_date=date(2008, 4, 28))
        meat_single, _ = Album.objects.get_or_create(title='We Are Made of Meat - Single', artist=halle, release_date=date(2026, 2, 9))
        sonobashi, _ = Album.objects.get_or_create(title='Sonobashinogi EP', artist=syudou_artist, release_date=date(2020, 4, 20))
        hope_album, _ = Album.objects.get_or_create(title='I Hope to Be Around', artist=menitrust, release_date=date(2017, 11, 10))
        mayhem, _ = Album.objects.get_or_create(title='Mayhem', artist=gaga, release_date=date(2025, 3, 7))
        self.stdout.write('Альбомы готовы')

        # Треки
        t1, _ = Track.objects.get_or_create(title='La velada legendaria', artist=sheena, album=single_sheena)
        t1.genre.add(jrock)

        t2, _ = Track.objects.get_or_create(title='Pay For It', artist=msi, album=if_album)
        t2.genre.add(electro_punk)

        t3, _ = Track.objects.get_or_create(title='Egoist', artist=egoist_artist)
        t3.genre.add(jpop)

        t4, _ = Track.objects.get_or_create(title="Honey I'm Home", artist=ghost)
        t4.genre.add(vocaloid)

        t5, _ = Track.objects.get_or_create(title='we made of meat', artist=halle, album=meat_single)
        t5.genre.add(indie_pop)

        t6, _ = Track.objects.get_or_create(title='bitter choko decoration', artist=syudou_artist, album=sonobashi)
        t6.genre.add(jpop)

        t7, _ = Track.objects.get_or_create(title='on the rocks', artist=meiko_artist)
        t7.genre.add(vocaloid)

        t8, _ = Track.objects.get_or_create(title='Roki', artist=mikito)
        t8.genre.add(vocaloid)

        t9, _ = Track.objects.get_or_create(title='I Hope to Be Around', artist=menitrust, album=hope_album)
        t9.genre.add(indie_pop)

        t10, _ = Track.objects.get_or_create(title='Garden of Eden', artist=gaga, album=mayhem)
        t10.genre.add(pop)

        t11, _ = Track.objects.get_or_create(title='Für dich', artist=gross)
        t11.genre.add(alt_rock)

        t12, _ = Track.objects.get_or_create(title='Fate of the Star', artist=tally)
        t12.genre.add(alt_rock)

        self.stdout.write(self.style.SUCCESS('✅ 12 треков добавлены!'))