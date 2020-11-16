from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Question, Tag, Answer, UserProfile

popular_tags = [
    'technopark',
    'C/C+',
    'perl',
    'Python',
    'MySQ',
    'django',
    'Mail.ru',
    'Firefox',
    'Web-technology'
]

tags = ['technopark', 'bmstu']

questions = [
    {
        'id': idx,
        'title': f'title {idx}',
        'text': 'text text',
        'tags': tags,
        'answers': idx % 6 + idx % 2,
    } for idx in range(8)
]


best_members = [
    'Mr.Freeman',
    'Dr.House',
    'Bender',
    'Queen Victoria',
    'V.Pupkin'
]

name_blocks = ['Login', 'Email', 'Nickname', 'Password', 'Repeat password']
type_blocks = ['text', 'email', 'text', 'password', 'password'] 
placeholders = ['vellerochka_', 'ivanivanov@mail.ru', 'Лерочка', '', '', '']
values = ['vellerochka_', 'lerakrya8@gmail.com', 'Лерочка', 'leraleralera15', ]

getRegBlocks = []
login = []
settings = []

answers = [
    {
        'text': 'text1 tex1t'
    },
        {
        'text': 'text2 text2'
    },
        {
        'text': 'text text'
    },
        {
        'text': 'text text'
    },
        {
        'text': 'text text'
    },
        {
        'text': 'text text'
    },
        {
        'text': 'text text'
    },
        {
        'text': 'text text'
    }
]


for idx, ids, pl, value in zip(name_blocks, type_blocks, placeholders, values):
        getRegBlocks.append({
            'type': ids,
            'name': idx,
            'place': pl,
            'value': '',
            'button': 'Register!'
        })
        if idx == 'Login' or idx == 'Password':
            login.append({
                'type': ids,
                'name': idx,
                'place': '',
                'value': '',
                'button': 'Log In!'
            })
        if idx != 'Repeat password':
            settings.append({
                'type': ids,
                'name': idx,
                'value': value,
                'place': '',
                'button': 'Save'
            })

def paginate (array, request):
    page_num = request.GET.get('page', 1)

    if page_num == None:
        page_num = 1

    paginator = Paginator(array, 5)
    if (paginator.num_pages == 0):
        return None, None
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page.object_list, page


def main_page(request):
    questions = Question.objects.all_questions()
    print(questions)
    page_obj, page = paginate(questions, request)

    best_members = UserProfile.objects.best_members()

    popular_tags = Tag.objects.popular_tags()

    return render(request, 'main_page.html', {
        'questions': page_obj,
        'tags': tags,
        'page': page,
        'popular_tags': popular_tags,
        'best_members': best_members
        })

def form_with_settings(request):
    return render(request, 'form_with_settings.html', {
        'popular_tags': popular_tags,
        'best_members': best_members,
        'settings': settings
        })

def question_by_tag(request, tag):
    questions_ = []
    for idx in questions:
        for ids in questions['tags']:
            if ids == tag:
                questions_.append(idx)

    page_obj, page = paginate(questions_, request)

    return render(request, 'question_by_tag.html', {
        'questions': page_obj,
        'tags': tags,
        'page': page,
        'tag': tag,
        'popular_tags': popular_tags,
        'best_members': best_members
    })

def hot_questions(request):
    page_obj, page = paginate(questions, request)

    return render(request, 'hot_questions.html', {
        'questions': page_obj,
        'tags': tags,
        'page': page,
        'popular_tags': popular_tags,
        'best_members': best_members
        })

def one_question_page(request, num_quest):
    question = questions[int(num_quest)]
    print(question)
    print(question['answers'])
    print(answers[:question['answers']])

    return render(request, 'one_question_page.html', {
        'question': question,
        'tags': tags,
        'num_q': num_quest,
        'answers': answers[:question['answers']],
        'popular_tags': popular_tags,
        'best_members': best_members
    })

def autorisation(request):
    return render(request, 'autorisation.html', {
        'logs': login,
        'popular_tags': popular_tags,
        'best_members': best_members
        })

def registration(request):
    return render(request, 'registration.html', {
        'getRegBlocks': getRegBlocks,
        'popular_tags': popular_tags,
        'best_members': best_members
        })

def add_question(request):
    return render(request, 'add_question.html', {
        'popular_tags': popular_tags,
        'best_members': best_members
    })