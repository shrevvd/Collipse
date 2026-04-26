from django.contrib.auth.models import User
from django.db import models

class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Artist(models.Model):
    name = models.CharField(
        max_length=200
    )
    
    photo = models.ImageField(upload_to='artists/', null=True, blank=True)
        
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Album(models.Model):
    title = models.CharField(
        max_length=200
    )
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name='albums'
    )
    cover = models.ImageField(
        upload_to='albums/',
        null=True,
        blank=True
    )
    release_date = models.DateField(
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f"{self.artist.name} - {self.title}"
    
    class Meta:
        ordering = ['-release_date', 'title']

class Track(models.Model):
    title = models.CharField(
        max_length=150
    )
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name='tracks'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='tracks',
        blank=True
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tracks'
    )
    cover = models.ImageField(
        upload_to='tracks/covers/',
        null=True,
        blank=True
    )
    audio_file = models.FileField(
        upload_to='tracks/audio/'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )
    
    duration = models.PositiveIntegerField(
        help_text='Длительность в секундах',
        null=True, blank=True
    )
    
    def __str__(self):
        return f"{self.artist.name} - {self.title}"
    
    class Meta:
        ordering = ['-uploaded_at']




class UserGenreScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'genre']

    def __str__(self):
        return f"{self.user.username} - {self.genre.name}: {self.score}"


class AbstractLike(models.Model):
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    
    track = models.ForeignKey(
        Track,
        on_delete=models.CASCADE
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        abstract = True  #таблица в бд не создаётся

    def __str__(self):
        return f"{self.user.username} - {self.track.title}"


class Like(AbstractLike):
    #лайк трека
    pass


class Dislike(AbstractLike):
    #дизлайк трека
    pass