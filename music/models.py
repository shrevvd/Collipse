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
    
    # photo = models.ImageField(upload_to='artists/', null=True, blank=True)
    # 
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Album(models.Model):
    title = models.CharField(  # Лучше назвать title для единообразия
        max_length=200
    )
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,  # Если удаляем артиста, удаляем и альбомы
        related_name='albums'
    )
    cover = models.ImageField(  # Обложка альбома
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
    title = models.CharField(  # Исправил опечатку Charfield -> CharField
        max_length=150
    )
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name='tracks'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tracks'
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,  # Трек может быть синглом без альбома
        related_name='tracks'
    )
    cover = models.ImageField(  # Обложка трека (если сингл или своя обложка)
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
    # Можно добавить длительность позже
    # duration = models.PositiveIntegerField(help_text='Длительность в секундах', null=True, blank=True)
    
    def __str__(self):
        return f"{self.artist.name} - {self.title}"
    
    class Meta:
        ordering = ['-uploaded_at']