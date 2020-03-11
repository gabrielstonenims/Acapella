from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from upload_validator import FileTypeValidator
from django.core.exceptions import ValidationError


MUSIC_GENRES = (
    ("Hip hop music","Hip hop music"),
    ("Pop music","Pop music"),
    ("Rock","Rock"),
    ("Jazz","Jazz"),
    ("Blues","Blues"),
    ("Country music","Country music"),
    ("Rhythm and blues","Rhythm and blues"),
    ("Classical music","Classical music"),
    ("Soul music","Soul music"),
    ("Gospel music","Gospel music"),
    ("Rapper","Rapper"),
    ("Adadam","Adadam"),
    ("Hip life","Hip life"),
    ("Gyama","Gyama"),
    ("Other","Other")
)

def validate_image_size(value):
    filesize= value.size
    
    if filesize > 4096:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value

def validate_video_file_size(value):
    filesize= value.size
    
    if filesize > 15360:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value

class Post_Audio(models.Model):
    artist = models.ForeignKey(User,on_delete=models.CASCADE)
    track_title = models.CharField(max_length=100)
    genre = models.CharField(choices = MUSIC_GENRES,max_length=40)
    track_poster = models.ImageField(upload_to="track_posters")
    track = models.FileField(upload_to="tracks", validators=[validate_image_size])
    like = models.ManyToManyField(User,related_name="likes",blank=True)
    date_posted = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.artist.username} posted {self.track_title}"

    def get_absolute_url(self):
        return reverse("post_audio_detail",args={self.pk })


class Post_Videos(models.Model):
    artist = models.ForeignKey(User,on_delete=models.CASCADE)
    vid_title = models.CharField(max_length=100)
    genre = models.CharField(choices = MUSIC_GENRES,max_length=40)
    vid_poster = models.ImageField(upload_to="vid_posters")
    vid = models.FileField(upload_to="tracks", validators=[validate_video_file_size])
    like = models.ManyToManyField(User,related_name="likes",blank=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.artist.username} posted {self.vid_title}"

    def get_absolute_video_url(self):
        return reverse("post_video_detail",args={self.pk })


class Programme(models.Model):
    artists = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    poster = models.ImageField(upload_to="programme_posters",validators=[validate_image_size])
    date = models.DateField(default=timezone.now)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.artists.username} scheduled an event"

    def get_absolute_programme_url(self):
        return reverse("programme_detail",args={self.pk })