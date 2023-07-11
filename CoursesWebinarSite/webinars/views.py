from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import Http404
from webinars.models import Webinar, File, Music, Photo
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect


@login_required(login_url="/login")
def show(request, id):
    if not id.isdigit():
        raise Http404('ID должно быть числом')

    try:
        webinar = Webinar.objects.get(id=id)

        if webinar.user != request.user:
            raise Http404('Это не ваш вебинар!')

        photos = []
        for photo_model in Photo.objects.filter(webinar=webinar):
            photos.append(photo_model.url)

        files = []
        for file_model in File.objects.filter(webinar=webinar):
            files.append([file_model.name, file_model.url])

        musics = []
        for music_model in Music.objects.filter(webinar=webinar):
            musics.append(music_model.url)

        context = {
            'name': webinar.name,
            'author': webinar.author,
            'description': webinar.description,
            'date': webinar.date,
            'url': webinar.url,
            'photos': photos,
            'files': files,
            'musics': musics,
        }

        return render(request, 'webinar_show.html', context=context)
    except ObjectDoesNotExist as e:
        raise Http404('ID в базе данных не найдено')


@login_required(login_url="/login")
def add(request):
    if request.method == "GET":
        return render(request, 'webinar_add.html')
    else:
        return post_add(request)


@login_required(login_url="/login")
def post_add(request):
    if request.method != "POST":
        raise Http404('Error')
    response = request.POST

    print(response)

    name = response['name']
    author = response['author']
    description = response['description']
    date = response['date']
    url = response['url']

    webinar = Webinar.objects.create(name=name, author=author, date=date, url=url, user=request.user,
                                     description=description)

    photos = []
    files = {}
    musics = []
    for key in response.keys():
        if 'photo_url_' in key:
            photos.append(response[key])
        elif 'file_name_' in key:
            id = key.replace('file_name_', '')
            files[id] = [response[f'file_name_{id}'], response[f'file_url_{id}']]
        elif 'music_url_' in key:
            musics.append(response[key])

    for url in photos:
        Photo.objects.create(url=url, webinar=webinar)

    for id in files:
        name = files[id][0]
        url = files[id][1]

        File.objects.create(name=name, url=url, webinar=webinar)

    for url in musics:
        Music.objects.create(url=url, webinar=webinar)

    return redirect(f'/webinar/{webinar.id}')


@login_required(login_url="/login")
def remove(request, id):
    web = Webinar.objects.get(id=id)

    if web.user == request.user:
        web.delete()
        return redirect('/')
    raise Http404('Это не ваш вебинар!')
