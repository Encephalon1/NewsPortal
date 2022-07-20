from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    authors_rating = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating_of_post'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.author.comment_set.aggregate(commentRating=Sum('rating_of_comment'))
        cRat = 0
        cRat += commentRat.get('commentRating')
        
        com_post_rat = self.post_set.all()
        cp_rat = 0
        for i in com_post_rat:
            a = i.comment_set.aggregate(commentPostRating=Sum('rating_of_comment'))
            cp_rat += a.get('commentPostRating')
        self.authors_rating = p_rat * 3 + c_rat + cp_rat
        self.save()


class Category(models.Model):
    name_of_category = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    title = models.CharField(max_length=128)
    post_text = models.TextField()
    rating_of_post = models.IntegerField(default=0)
    date_and_time_of_creation_post = models.DateTimeField(auto_now_add=True)
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    NEWS = 'NW'
    ARTICLE = 'AR'
    CHOICE = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )
    post_type = models.CharField(max_length=2, choices=CHOICE, default=ARTICLE)

    def like(self):
        self.rating_of_post += 1
        self.save()

    def dislike(self):
        self.rating_of_post -= 1
        self.save()

    def preview(self):
        return self.post_text[0:123] + '...'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_text = models.CharField(max_length=255)
    date_and_time_of_creation_comment = models.DateTimeField(auto_now_add=True)
    rating_of_comment = models.IntegerField(default=0)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating_of_comment += 1
        self.save()

    def dislike(self):
        self.rating_of_comment -= 1
        self.save()
