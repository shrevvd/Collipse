from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True, blank=True
    )
    
    nickname = models.CharField(
        max_length=50,
        blank=True
    )
    
    bio = models.TextField(
        max_length=500,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s profile"
    
class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_of')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'friend']

    def __str__(self):
        return f"{self.user.username} -> {self.friend.username}"
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.text[:30]}"