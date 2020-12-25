from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class QuestionManager(models.Manager):
    def all_questions(self):
        return self.all().order_by('-date_create').reverse()

    def hot_questions(self):
        return self.annotate(sum_likes = Count('likes')).order_by('-sum_likes').reverse()

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
    answers = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    objects = QuestionManager()

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
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    objects = AnswerManager()

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.title

class QuestionsLikes(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True, verbose_name="Лайк")

    def __str__(self):
        return self.user.nickname + ' поставил лайк "' + self.question.title + '"'
    
    class Meta:
        unique_together = ('question', 'user')
        verbose_name = 'Лайк вопроса'
        verbose_name_plural = 'Лайки вопроса'

class QuestionsDislikes(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_dislike = models.BooleanField(default=True, verbose_name="Лайк")

    def __str__(self):
        return self.user.nickname + ' поставил лайк "' + self.question.title + '"'
    
    class Meta:
        unique_together = ('question', 'user')
        verbose_name = 'Лайк вопроса'
        verbose_name_plural = 'Лайки вопроса'

class AnswersLikes(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True, verbose_name='Лайк')

    def __str__(self):
        return self.user.nickname + ' поставил лайк "' + self.answer.question.title + '"'

    class Meta:
        unique_together = ('answer', 'user')
        verbose_name = 'Лайк ответа'
        verbose_name_plural = 'Лайки ответа'

class AnswersDislikes(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True, verbose_name='Лайк')

    def __str__(self):
        return self.user.nickname + ' поставил лайк "' + self.answer.question.title + '"'

    class Meta:
        unique_together = ('answer', 'user')
        verbose_name = 'Лайк ответа'
        verbose_name_plural = 'Лайки ответа'




    



