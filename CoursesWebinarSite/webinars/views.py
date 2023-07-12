from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import Http404
from watched.models import WatchedWebinar
from webinars.models import Webinar, File, Music, Photo
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect


@login_required(login_url="/login")
def show(request, id):
    if not id.isdigit():
        raise Http404('ID должно быть числом')

    try:
        user = request.user
        webinar = Webinar.objects.get(id=id)

        if webinar.user != user:
            raise Http404('Это не ваш вебинар!')

        context = {}

        if user.first_name != '':
            name = user.first_name
        else:
            name = user.username
        context['name'] = name

        photos = []
        for photo_model in Photo.objects.filter(webinar=webinar):
            photos.append(photo_model.url)

        files = []
        for file_model in File.objects.filter(webinar=webinar):
            files.append([file_model.name, file_model.url])

        musics = []
        for music_model in Music.objects.filter(webinar=webinar):
            musics.append([music_model.url, music_model.url[-10:]])

        webinar_watched = False
        try:
            WatchedWebinar.objects.get(user=user, webinar=webinar)
            webinar_watched = True
        except Exception as e:
            if str(e) == 'WatchedWebinar matching query does not exist.':
                webinar_watched = False

        context['webinar'] = {
            'id': webinar.id,
            'name': webinar.name,
            'author': webinar.author,
            'description': webinar.description,
            'date': webinar.format_date(),
            'url': webinar.url,
            'photos': photos,
            'files': files,
            'musics': musics,
            'watched': webinar_watched
        }

        return render(request, 'webinar/show.html', context=context)
    except ObjectDoesNotExist as e:
        raise Http404('ID в базе данных не найдено')


@login_required(login_url="/login")
def my(request):
    user = request.user
    context = {}

    if user.first_name != '':
        name = user.first_name
    else:
        name = user.username
    context['name'] = name

    mass = []
    for webinar in Webinar.objects.filter(user=user):
        web = [webinar.id, webinar.name]

        if webinar.description != '':
            web.append(webinar.description)
        else:
            web.append('')

        web.append(webinar.format_date(is_month_name=False))

        try:
            WatchedWebinar.objects.get(user=user, webinar=webinar)
            web.append(True)
        except Exception as e:
            if str(e) == 'WatchedWebinar matching query does not exist.':
                web.append(False)

        mass.append(web)

    context['webinars'] = mass
    return render(request, 'webinar/my.html', context=context)


@login_required(login_url="/login")
def add(request):
    if request.method == "GET":
        return render(request, 'webinar/add.html', context={'alert': ''})
    else:
        if request.method != "POST":
            raise Http404('Error')
        response = request.POST

        name = response['name']
        author = response['author']
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
        else:
            return render(request, 'webinar/add.html',
                          context={'alert': 'Ссылка на вебинар должен вести на сайт youtube.com'})
        print(url)

        webinar = Webinar.objects.create(name=name, author=author, date=date, url=url, user=request.user,
                                         description=description)

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
            Photo.objects.create(url=url, webinar=webinar)

        for id in files:
            name = files[id][0]
            url = files[id][1]

            File.objects.create(name=name, url=url, webinar=webinar)

        for url in musics:
            Music.objects.create(url=url, webinar=webinar)

        return redirect(f'/webinar/{webinar.id}')


@login_required(login_url="/login")
def make_watched(request, id):
    web = Webinar.objects.get(id=id)
    user = request.user

    WatchedWebinar.objects.create(user=user, webinar=web)
    return redirect(f'/webinar/{id}')


@login_required(login_url="/login")
def make_no_watched(request, id):
    web = Webinar.objects.get(id=id)
    user = request.user

    WatchedWebinar.objects.get(user=user, webinar=web).delete()
    return redirect(f'/webinar/{id}')


@login_required(login_url="/login")
def remove(request, id):
    web = Webinar.objects.get(id=id)

    if web.user == request.user:
        web.delete()
        return redirect('/')
    raise Http404('Это не ваш вебинар!')
