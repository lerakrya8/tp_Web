from django.core.management.base import BaseCommand
from app.models import UserProfile, Question, Answer, Tag, User
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
        users_dislikes = randint(1, 53)

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
            array_dislikes = list()

            for _ in range(users_dislikes):
                dislike = choice(author_ids)
                if dislike in array_dislikes or dislike in array_likes:
                    continue
                array_dislikes.append(users_dislikes)
                dislike_user = UserProfile.objects.get(pk=dislike)
                question.dislikes.add(dislike_user)
            question.save()

    def fill_tags(self, cnt):
        for _ in range(cnt):
            tag = Tag.objects.create(
                tag_title=f.word())
            tag.save()

    def fill_users(self, cnt):
        for _ in range(cnt):
            user_u = User.objects.create(
                username=f.name(),
                email=f.email(),
                password=f.password()
            )
            user_u.save()
            user_profile = UserProfile.objects.create(
                user = user_u,
                image_profile="https://loremflickr.com/320/240",
                nickname = f.name())
            user_profile.save()

    def fill_answers(self, cnt):
        author_ids = list(
            UserProfile.objects.values_list(
                'id', flat=True
            )
        )

        questions = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )

        users_likes = randint(1, 234)
        users_dislikes = randint(1, 53)

        for _ in range(cnt):
            questions_id = choice(questions)
            answer = Answer.objects.create(
                author_id=choice(author_ids),
                text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                title=f.sentence()[:128],
                question_id=questions_id,
                correct=choice([True, False]))
            array_likes = list()
            for _ in range(users_likes):
                like = choice(author_ids)
                if like in array_likes:
                    continue
                array_likes.append(like)
                like_user = UserProfile.objects.get(pk=like)
                answer.likes.add(like_user)
            array_dislikes = list()
            
            for _ in range(users_dislikes):
                dislike = choice(author_ids)
                if dislike in array_dislikes or dislike in array_likes:
                    continue
                array_dislikes.append(users_dislikes)
                dislike_user = UserProfile.objects.get(pk=dislike)
                answer.dislikes.add(dislike_user)
            answer.save()
            question = Question.objects.get(pk=questions_id)
            question.answers += 1
            question.save()

    def handle(self, *args, **kwards):
        # num_questions = kwards['questions']
        # num_tags = kwards['tags']
        # num_user = kwards['users']
        num_answers = kwards['answers']
        # db_size = kwards['db_size']
        # self.fill_questions(num_questions)

        # if  num_questions != None:
            
            # self.fill_answers(db_size)
            # self.fill_users(db_size)
        # if num_tags != None:
        #     self.fill_tags(num_tags)
          
        # self.fill_questions(num_questions)
        if num_answers != None:
            self.fill_answers(num_answers)
