from django.db import models
from django.contrib.auth.models import User

class QuestionManager(models.Manager):
    def all_questions(self):
        return self.all().order_by('-date_create').reverse()

    def hot_questions(self):
        return self.annotate(sum_likes = sum('likes')).order_by('-sum_likes').reverse()

    def questions_by_tag(self, tag):
        return self.filter(tags__tag_title = tag)

    def one_question(self, number):
        return self.filter(pk = number)

    
class AnswerManager(models.Manager):
    def answers_by_que(self, index):
        return self.all().filter(question__pk=index).all()

class TagManager(models.Manager):
    def popular_tags(self):
        return self.all()[:9]

class ProfileManager(models.Manager):
    def best_members(self):
        return self.all()[:5]



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    image_profile = models.ImageField(blank=True)
    nickname = models.CharField(max_length=256, verbose_name='Псевдоним')

    objects = ProfileManager()

    def __str__(self):
        return self.nickname

class Tag(models.Model):
    tag_title = models.CharField(max_length=512, verbose_name='Теги')
    rating = models.IntegerField(default=0)

    objects = TagManager()

    def __str__(self):
        return self.tag_title

class Question(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=512, verbose_name='Заголовок вопроса')
    text = models.TextField(verbose_name='Текст')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    tags = models.ManyToManyField(Tag, blank=True)
    likes = models.ManyToManyField(UserProfile, blank=True, related_name='questions_like')
    answers = models.IntegerField(default=0)

    objects = QuestionManager()

    # def number_of_likes(self):
    #     return self.likes.count()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.title

class Answer(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=512, verbose_name='Заголовок ответа')
    text = models.TextField(verbose_name='Текст')
    correct = models.BooleanField(default=False, verbose_name='Полезно')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    likes = models.ManyToManyField(UserProfile, blank=True, related_name='answers_like')

    objects = AnswerManager()

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.title




    



