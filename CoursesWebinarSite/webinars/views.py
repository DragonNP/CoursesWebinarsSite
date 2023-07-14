from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import redirect

from users.models import UserWebinarLink
from webinars.models import Webinar, Author, Material, MaterialType


@login_required
def all_webinars(request):
    return redirect('/webinars/my')


@login_required
def my(request):
    user = request.user
    context = {}

    mass = []
    for user_webinar_link in UserWebinarLink.objects.filter(user=user, is_my=True):
        webinar = user_webinar_link.webinar

        web = [webinar.id, webinar.name]

        if webinar.description != '':
            web.append(webinar.description)
        else:
            web.append('')

        web.append(webinar.format_date(is_month_name=False))
        web.append(user_webinar_link.is_watched)

        mass.append(web)

    context['webinars'] = mass
    return render(request, 'webinars/my.html', context=context)


@login_required
def add(request):
    if request.method == "GET":
        return render(request, 'webinars/add.html', context={'alert': ''})

    if request.method != "POST":
        raise Http404('Error')

    response = request.POST

    name = response['name']
    author_name = response['author']
    description = response['description']
    date = response['date']
    url = str(response['url'])

    if url.startswith('https://www.youtube.com/watch'):
        for code in url.split('?')[1].split('&'):
            if code[0:2] == 'v=':
                url = 'https://www.youtube.com/embed/' + code[2:]
                break
    elif url.startswith('https://www.youtube.com/embed'):
        url = url.split('?')[0]

    author = Author.objects.filter(name=author_name).first()
    if author is None:
        author = Author.objects.create(name=author_name)

    webinar = Webinar.objects.create(name=name, author=author, date=date, url=url,
                                     description=description)
    UserWebinarLink.objects.create(user=request.user, webinar=webinar, is_watched=False, is_my=True)

    photos = []
    files = {}
    musics = []
    for key in response.keys():
        if 'photo_' in key:
            photos.append(response[key])
        elif 'file_name_' in key:
            id = key.replace('file_name_', '')
            files[id] = [response[f'file_name_{id}'], response[f'file_url_{id}']]
        elif 'music_' in key:
            musics.append(response[key])

    for url in photos:
        Material.objects.create(name=url[-10:],
                                url=url,
                                webinar=webinar,
                                type=MaterialType.PHOTO)

    for id in files:
        name = files[id][0]
        url = files[id][1]

        Material.objects.create(name=name,
                                url=url,
                                webinar=webinar,
                                type=MaterialType.FILE)

    for url in musics:
        Material.objects.create(name=url[-10:],
                                url=url,
                                webinar=webinar,
                                type=MaterialType.MUSIC)

    return redirect(f'/webinars/{webinar.id}')


@login_required
def show(request, id):
    if not id.isdigit():
        raise Http404('ID должно быть числом')

    webinar = Webinar.objects.filter(id=id).first()
    if webinar is None:
        return redirect('/')

    user = request.user
    context = {}

    if user.first_name != '':
        name = user.first_name
    else:
        name = user.username
    context['name'] = name

    photos = []
    files = []
    musics = []

    for material in Material.objects.filter(webinar=webinar):
        if material.type == MaterialType.PHOTO:
            photos.append(material.url)
        elif material.type == MaterialType.FILE:
            files.append([material.name, material.url])
        elif material.type == MaterialType.MUSIC:
            musics.append([material.url, material.url[-10:]])

    user_webinar_link = UserWebinarLink.objects.filter(user=user, webinar=webinar).first()
    if user_webinar_link is None:
        user_webinar_link = UserWebinarLink.objects.create(user=user, webinar=webinar, is_my=False, is_watched=False)

    context['webinar'] = {
        'id': webinar.id,
        'name': webinar.name,
        'author': webinar.author.name,
        'description': webinar.description,
        'date': webinar.format_date(),
        'url': webinar.url,
        'photos': photos,
        'files': files,
        'musics': musics,
        'watched': user_webinar_link.is_watched,
        'is_my': user_webinar_link.is_my
    }

    return render(request, 'webinars/show.html', context=context)


@login_required
def make_watched(request, id):
    web = Webinar.objects.get(id=id)
    user = request.user

    user_webinar_link = UserWebinarLink.objects.filter(user=user, webinar=web).first()
    if user_webinar_link is None:
        UserWebinarLink.objects.create(user=user, webinar=web, is_my=False, is_watched=True)
    else:
        user_webinar_link.is_watched = True
        user_webinar_link.save()

    return redirect(f'/webinars/{id}')


@login_required
def make_no_watched(request, id):
    web = Webinar.objects.get(id=id)
    user = request.user

    user_webinar_link = UserWebinarLink.objects.filter(user=user, webinar=web).first()
    if user_webinar_link is None:
        UserWebinarLink.objects.create(user=user, webinar=web, is_my=False, is_watched=False)
    else:
        user_webinar_link.is_watched = False
        user_webinar_link.save()

    return redirect(f'/webinars/{id}')


@login_required
def remove(request, id):
    current_webinar = Webinar.objects.get(id=id)
    user_webinar_link = UserWebinarLink.objects.get(user=request.user, webinar=current_webinar)

    if user_webinar_link.is_my:
        current_webinar.delete()
    return redirect('/')
