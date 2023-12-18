from django.db import models
from datetime import datetime
from django.core.validators import MinLengthValidator

# Create your models here.

class EmailConfig(models.Model):
    from_email = models.EmailField(max_length=100)
    email_password = models.CharField(
        max_length=128, validators=[MinLengthValidator(8)])
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
    title=models.CharField(max_length=255)
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
    image=models.ImageField(upload_to='Blog')
    date_created=models.DateTimeField(default=datetime.now())
    published=models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blog_posts'
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
