from django.shortcuts import render
from django.http import Http404
from webinars.models import Webinar, File, Music
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect


def show(request, id):
    if not id.isdigit():
        raise Http404('ID должно быть числом')

    try:
        webinar = Webinar.objects.get(id=id)

        return render(request, 'webinar_show.html',
                      {'name': webinar.name, 'author': webinar.author, 'date': webinar.date, 'url': webinar.url})
    except ObjectDoesNotExist as e:
        raise Http404('ID в базе данных не найдено')


def add(request):
    if request.method == "GET":
        return render(request, 'webinar_add.html')
    else:
        return post_add(request)


def post_add(request):
    if request.method != "POST":
        raise Http404('Error')
    response = request.POST

    print(response)

    name = response['name']
    author = response['author']
    date = response['date']
    url = response['url']

    webinar = Webinar.objects.create(name=name, author=author, date=date, url=url)

    files_count = int(response['files_count'])
    for i in range(files_count):
        name = response[f'file_name_{str(i)}']
        url = response[f'file_url_{str(i)}']

        File.objects.create(name=name, url=url, webinar=webinar)

    musics_count = int(response['musics_count'])
    for i in range(musics_count):
        url = response[f'music_url_{str(i)}']
        Music.objects.create(url=url, webinar=webinar)

    return redirect(f'/webinar/{webinar.id}')
