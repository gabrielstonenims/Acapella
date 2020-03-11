from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=150, blank=True, default='Just a music lover')
    profile_pic = models.ImageField(blank=True, default='default.jpg', upload_to='profile_pics')
    cover_pic = models.ImageField(blank=True, default='coverdefault.jpg', upload_to='cover_photos')
    following = models.ManyToManyField(User, blank=True, related_name='is_following')
    my_followers = models.ManyToManyField(User, blank=True, related_name='my_profile_followers')
    your_facebook = models.CharField(max_length=450, blank=True)
    your_instagram = models.CharField(max_length=450, blank=True)
    your_twitter = models.CharField(max_length=450, blank=True)
    your_youtube = models.CharField(max_length=450, blank=True)

    def __str__(self):
        return f"{self.user.username}"


class Group_Members(models.Model):
    group = models.ForeignKey(Profile,on_delete=models.CASCADE)
    name = models.CharField(max_length=90)
    part = models.CharField(max_length=30,help_text="The voice part this singer sings in your group.")
    image = models.ImageField(upload_to="group_images")
    your_facebook = models.CharField(max_length=450, blank=True)
    your_instagram = models.CharField(max_length=450, blank=True)
    your_twitter = models.CharField(max_length=450, blank=True)
    your_youtube = models.CharField(max_length=450, blank=True)

    def __str__(self):
        return f"{self.group.user.username} add a new member.{self.name}"
