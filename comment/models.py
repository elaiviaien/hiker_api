from django.db import models

from mainpage.models import Article
from users.models import Userc


class Comment(models.Model):
    """model for comments"""

    post = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Userc, related_name='authorofcomment', on_delete=models.CASCADE, verbose_name='Автор',default=None, blank=True, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    approved_comment = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        article = Article.objects.get(slug=self.post.slug)
        article.save()
        user = Userc.objects.get(slug=article.author.slug)
        user.save()
        # save
