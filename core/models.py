from django.db import models
from datetime import datetime
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class EmailConfig(models.Model):
    from_email = models.EmailField(max_length=100,default="bengomallKE@gmail.com")
    email_password = models.CharField(
        max_length=128, validators=[MinLengthValidator(8)],default="waxaaaofvxgifsyt")
    email_host = models.CharField(max_length=50, default="smtp.gmail.com")
    email_port = models.CharField(max_length=5, default=587)
    use_tls = models.BooleanField(default=True)
    fail_silently = models.BooleanField(default=True)

    # def save(self, *args, **kwargs):
    #     self.email_password = make_password(self.email_password)
    #     super(EmailConfig, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.from_email

    class Meta:
        verbose_name_plural = 'Email Configuration'

class FrontStore(models.Model):
    flash_sale_end_date = models.DateTimeField(default=datetime.now())
    slider_image=models.FileField(upload_to='store/slider',blank=True,null=True)
    slider_text = models.CharField(
        max_length=100, default="Upto 60% + Extra 10%")

    def __str__(self):
        return "Front Store Settings"

    class Meta:
        db_table = 'storefront'
        verbose_name = 'Front Store Settings'
        verbose_name_plural = 'Front Store Settings'

class Blog(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blogs',null=True)
    title = models.CharField(
        max_length=255, default="Yuletide Zen: Finding Balance in Festivity")
    featured_image = models.ImageField(upload_to='Blog/featured', null=True)
    excerpt = models.TextField(default="Dive into the season of joy and mindfulness with Yogi's Delight! Explore our guide on maintaining serenity amidst the festive bustle. From calming yoga routines to mindful gift-giving, discover how you can infuse your holidays with peace and positivity.")
    date_created=models.DateTimeField(default=datetime.now())
    published=models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blog'
        verbose_name = 'Blog'
        verbose_name_plural = 'Blog'

class Post(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='posts')
    title=models.CharField(max_length=255)
    content=models.TextField(default='Yogis official store')
    image=models.ImageField(upload_to='Blog/posts')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blog_posts'
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    comment=models.TextField()

    def __str__(self):
        return self.user.email

    class Meta:
        db_table = 'post_comments'
        verbose_name = 'Post Comment'
        verbose_name_plural = 'Post Comments'
