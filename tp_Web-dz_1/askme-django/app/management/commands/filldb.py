from django.core.management.base import BaseCommand
from app.models import UserProfile, Question, Answer, Tag, User, QuestionsLikes, QuestionsDislikes, AnswersLikes, AnswersDislikes
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
        parser.add_argument('--questions_likes', type=int)
        parser.add_argument('--answers_likes', type=int)
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
            # array_likes = list()
            # for _ in range(users_likes):
            #     like = choice(author_ids)
            #     if like in array_likes:
            #         continue
            #     array_likes.append(like)
            #     like_user = UserProfile.objects.get(pk=like)
            #     question.likes.add(like_user)
            # array_dislikes = list()

            # for _ in range(users_dislikes):
            #     dislike = choice(author_ids)
            #     if dislike in array_dislikes or dislike in array_likes:
            #         continue
            #     array_dislikes.append(users_dislikes)
            #     dislike_user = UserProfile.objects.get(pk=dislike)
            #     question.dislikes.add(dislike_user)
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

        # users_likes = randint(1, 234)
        # users_dislikes = randint(1, 53)

        for _ in range(cnt):
            questions_id = choice(questions)
            answer = Answer.objects.create(
                author_id=choice(author_ids),
                text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                title=f.sentence()[:128],
                question_id=questions_id,
                correct=choice([True, False]))
            # array_likes = list()
            # for _ in range(users_likes):
            #     like = choice(author_ids)
            #     if like in array_likes:
            #         continue
            #     array_likes.append(like)
            #     like_user = UserProfile.objects.get(pk=like)
            #     answer.likes.add(like_user)
            # array_dislikes = list()
            
            # for _ in range(users_dislikes):
            #     dislike = choice(author_ids)
            #     if dislike in array_dislikes or dislike in array_likes:
            #         continue
            #     array_dislikes.append(users_dislikes)
            #     dislike_user = UserProfile.objects.get(pk=dislike)
            #     answer.dislikes.add(dislike_user)
            answer.save()
            question = Question.objects.get(pk=questions_id)
            question.answers += 1
            question.save()
    
    def fill_questions_likes(self, cnt):
        users = list(UserProfile.objects.values_list(
            'id', flat=True
        ))

        questions = list(Question.objects.values_list(
            'id', flat=True
        ))

        for i in questions:
            likes_amount = randint(3, 21)
            dislikes_amount = randint(2, 15)
            likes_question = list()
            dislikes_question = list()
            for j in range(likes_amount):
                id_user = choice(users)
                if id_user in likes_question:
                    continue
                likes_question.append(id_user)
                like = QuestionsLikes.objects.create(user_id=id_user, question_id=i)
                like.save()
                question = Question.objects.get(pk=i)
                question.likes += 1
                question.save()
            for j in range(dislikes_amount):
                id_user = choice(users)
                if id_user in likes_question or id_user in dislikes_question:
                    continue
                dislikes_question.append(id_user)
                dislike = QuestionsDislikes.objects.create(user_id=id_user, question_id=i)
                dislike.save()
                question = Question.objects.get(pk=i)
                question.dislikes += 1
                question.save()
    
    def fill_answers_likes(self, cnt):
        users = list(UserProfile.objects.values_list(
            'id', flat=True
        ))

        answers = list(Answer.objects.values_list(
            'id', flat=True
        ))

        for i in answers:
            likes_amount = randint(1, 120)
            dislikes_amount = randint(1, 34)
            likes_answers = list()
            dislike_answers = list()
            for j in range(likes_amount):
                id_user = choice(users)
                if id_user in likes_answers:
                    continue
                likes_answers.append(id_user)
                like = AnswersLikes.objects.create(user_id=id_user, answer_id=i)
                like.save()
                answer = Answer.objects.get(pk=i)
                answer.likes += 1
                answer.save()
            for j in range(dislikes_amount):
                id_user = choice(users)
                if id_user in likes_answers or id_user in dislike_answers:
                    continue
                dislike_answers.append(id_user)
                dislike = AnswersDislikes.objects.create(user_id=id_user, answer_id=i)
                dislike.save()
                answer = Answer.objects.get(pk=i)
                answer.dislikes += 1
                answer.save()

    def handle(self, *args, **kwards):
        num_questions = kwards['questions']
        num_tags = kwards['tags']
        num_user = kwards['users']
        num_answers = kwards['answers']
        num_que_likes = kwards['questions_likes']
        num_ans_likes = kwards['answers_likes']
        db_size = kwards['db_size']

        if  db_size != None:
            self.fill_users(db_size)
            self.fill_tags(db_size)
            self.fill_questions(db_size)
            self.fill_answers(db_size)
            self.fill_questions_likes(db_size)
            self.fill_answers_likes(db_size)

        if num_tags != None:
          self.fill_tags(num_tags)
        if num_user != None:
            self.fill_users(num_user)
        if num_questions != None:
            self.fill_questions(num_questions)
        if num_answers != None:
            self.fill_answers(num_answers)
        if num_que_likes != None:
            self.fill_questions_likes(num_que_likes)
        if num_ans_likes != None:
            self.fill_answers_likes(num_ans_likes)
