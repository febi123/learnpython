from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# This code is triggered whenever a new user has been created and saved to the database

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



# from pygments.lexers import get_lexer_by_name
# from pygments.formatters.html import HtmlFormatter
# from pygments import highlight

# Create your models here.

class Predictlog(models.Model):
    name = models.CharField(max_length=250)
    suku = models.CharField(max_length=250, blank=True, null=True)
    prob_men = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    prob_women = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    feedback = models.CharField(max_length=1, blank=True, null=True)
    feedback_reason = models.CharField(max_length=500, blank=True, null=True)
    api_consumer = models.CharField(max_length=1000, blank=True, null=True)
    client_ip = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey('auth.User', related_name='predictlog', null=True, on_delete=models.CASCADE)
    highlight = models.TextField(null=True)

    # class Meta:s
    #     ordering = ('created',)

# def save(self, *args, **kwargs):
#     """
#     Use the `pygments` library to create a highlighted HTML
#     representation of the code snippet.
#     """
#     lexer = get_lexer_by_name(self.language)
#     linenos = self.linenos and 'table' or False
#     options = self.title and {'title': self.title} or {}
#     formatter = HtmlFormatter(style=self.style, linenos=linenos,
#                               full=True, **options)
#     self.highlighted = highlight(self.code, lexer, formatter)
#     super(Snippet, self).save(*args, **kwargs)