from django.db import models
from userapp.models import HabaUser
import datetime


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="Категория", db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='url')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name', ]


class Tag(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name="Тэг", db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='url')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['name', ]


class Post(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE,
                            verbose_name='Категория')
    author = models.ForeignKey(HabaUser, on_delete=models.CASCADE,
                               verbose_name='Автор')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='url')
    content = models.TextField(blank=True, verbose_name='Текст')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='url')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Презентационная картинка')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=False, verbose_name='Публикация')
    is_blocked = models.BooleanField(default=False, verbose_name='Заблокирована')
    tags = models.ManyToManyField(Tag, verbose_name='Тэги', related_name='tags')

    def __str__(self):
        return f'{self.title[:25]}...'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['time_create', 'title']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Статья')
    user = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name="Комментарий")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=False, verbose_name='Публикация')

    def __str__(self):
        return f'{self.user} / {self.post}'

    @staticmethod
    def get_count(post):
        return Comment.objects.filter(post=post).count()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['time_create', 'user']


class AuthorLike(models.Model):
    user = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='user_author_set')
    author = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Автор', related_name='author_set')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return f'{self.user} / {self.author}'

    @staticmethod
    def get_count(author):
        return AuthorLike.objects.filter(author=author).count()

    class Meta:
        verbose_name = 'Лайк автору'
        verbose_name_plural = 'Лайки автору'
        ordering = ['time_create']


class PostLike(models.Model):
    user = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Статья')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return f'{self.user} / {self.post}'

    @staticmethod
    def get_count(post):
        return PostLike.objects.filter(post=post).count()

    class Meta:
        verbose_name = 'Лайк к статье'
        verbose_name_plural = 'Лайки к статье'
        ordering = ['time_create']


class CommentLike(models.Model):
    user = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    comment = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Комментарий')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return f'{self.user} / {self.comment}'

    @staticmethod
    def get_count(comment):
        return CommentLike.objects.filter(comment=comment).count()

    class Meta:
        verbose_name = 'Лайк к комментарию'
        verbose_name_plural = 'Лайки к комментарию'
        ordering = ['time_create']


class UserComplaints(models.Model):
    user = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Заявитель',
                             related_name='user_complaint_set')
    bad_user = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Виновный',
                                 related_name='bad_user_set')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Статья')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='Комментарий')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    moderator = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Модератор',
                                  related_name='moderator_complaint_set')
    moderated_time = models.DateTimeField(default=datetime.date(2000, 1, 1), verbose_name='Время создания')

    def __str__(self):
        return f'{self.user} / {self.bad_user} / {self.post}'

    class Meta:
        verbose_name = 'Жалоба пользователя'
        verbose_name_plural = 'Жалобы пользователя'
        ordering = ['time_create']


class BlockedUser(models.Model):
    user = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='user_block_set')
    moderator = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Модератор',
                                  related_name='moderator_block_set')
    complaint = models.ForeignKey(UserComplaints, on_delete=models.CASCADE, verbose_name='Жалоба пользователя')
    lock_date = models.DateField(verbose_name='Заблокирован до')
    reason_for_blocking = models.CharField(max_length=255, verbose_name='Причина блокировки')

    def __str__(self):
        return f'{self.user} / {self.moderator} / {self.complaint}'

    class Meta:
        verbose_name = 'Заблокированный пользователь'
        verbose_name_plural = 'Заблокированные пользователи'
        ordering = ['lock_date']
