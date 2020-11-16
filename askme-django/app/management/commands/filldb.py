from django.core.management.base import BaseCommand
from app.models import UserProfile, Question, Answer, Tag 
from random import choice
from faker import Faker
from random import randint

f = Faker()

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--tags', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--answers', type=int)
        parser.add_argument('--users', type=int)
        parser.add_argument('--db_size', type=int)


    def fill_questions(self, cnt):
        author_ids = list(
            UserProfile.objects.values_list(
                'id', flat=True
            )
        )

        tags_id = list(
            Tag.objects.values_list(
                'id', flat=True
            )
        )

        tags_count = randint(1, 4)
        users_likes = randint(1, 234)

        for _ in range(cnt):
            question = Question.objects.create(
                author_id=choice(author_ids),
                text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                title=f.sentence()[:128])
            for _ in range(tags_count):
                tag = Tag.objects.get(pk=(choice(tags_id)))
                question.tags.add(tag)
                tag.rating += 1
                tag.save()
            array_likes = list()
            for _ in range(users_likes):
                like = choice(author_ids)
                if like in array_likes:
                    continue
                array_likes.append(like)
                like_user = UserProfile.objects.get(pk=like)
                question.likes.add(like_user)
            question.save()

    def handle(self, *args, **kwards):
        num_questions = kwards['questions']
        # num_user = kwards['users']
        # num_answers = kwards['answers']
        # db_size = kwards['db_size']
        self.fill_questions(num_questions)

        # if db_size != None:
        #     self.fill_questions(db_size)
        #     self.fill_answers(db_size)
        #     self.fill_users(db_size)
        #     self.fill_tags(db_size)