from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

questions = [
    {
        'id': idx,
        'title': f'title {idx}',
        'text': 'text text',
        'tag1': popular_tags[idx % 9],
        'tag2': popular_tags[idx % 9 + 1],
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

questions_ex = [
    {
        'id': 1,
        'title': 'title 0',
        'text': 'text text',
        'tag1': 'technopark',
        'tag2': 'bmstu',
        'answers': 3
    },
    {
        'id': 2,
        'title': 'title 1',
        'text': 'text text',
        'tag1': 'tag2',
        'tag2': 'tag3',
        'answers': 5
    },
    {
        'id': 3,
        'title': 'title 2',
        'text': 'text text',
        'tag1': 'technopark',
        'tag2': '',
        'answers': 2
    },
    {
        'id': 4,
        'title': 'title 3',
        'text': 'text text',
        'tag1': 'technopark',
        'tag2': 'bmstu',
        'answers': 7
    },
    {
        'id': 5,
        'title': 'title 4',
        'text': 'text text',
        'tag1': 'tag2',
        'tag2': 'tag3',
        'answers': 3
    },
    {
        'id': 6,
        'title': 'title 5',
        'text': 'text text',
        'tag1': 'tag3',
        'tag2': '',
        'answers': 4
    },
    {
        'id': 7,
        'title': 'title 6',
        'text': 'text text',
        'tag1': 'technopark',
        'tag2': 'bmstu',
        'answers': 3
    },
    {
        'id': 8,
        'title': 'title 7',
        'text': 'text text',
        'tag1': 'technopark',
        'tag2': 'bmstu',
        'answers': 3
    },
    {
        'id': 9,
        'title': 'title 8',
        'text': 'text text',
        'tag1': 'technopark',
        'tag2': 'bmstu',
        'answers': 3
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
    page_obj, page = paginate(questions, request)

    return render(request, 'main_page.html', {
        'questions': page_obj,
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
        if idx['tag1'] == tag or idx['tag2'] == tag:
            questions_.append(idx)

    page_obj, page = paginate(questions_, request)

    return render(request, 'question_by_tag.html', {
        'questions': page_obj,
        'page': page,
        'tag': tag,
        'popular_tags': popular_tags,
        'best_members': best_members
    })

def hot_questions(request):
    page_obj, page = paginate(questions, request)

    return render(request, 'hot_questions.html', {
        'questions': page_obj,
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