from django.test import TestCase
from django.contrib.auth.models import User
from ..services import get_context_for_user_courses, get_context_for_module, get_list_courses_from_get_course


class ServicesTestCase(TestCase):
    def test_get_context_for_user_courses(self):
        empty_user = User.objects.create(username="test", password="1234")
        self.assertEqual(get_context_for_user_courses(empty_user), {'courses': []})

    def test_get_context_for_module(self):
        empty_user = User.objects.create(username="test", password="1234")
        self.assertEqual(get_context_for_module(empty_user, '-1111'), {'lessons': [], 'modules': []})

    def test_get_list_courses_from_get_course(self):
        # Проверка на пустые параметры
        self.assertEqual(get_list_courses_from_get_course({}),
                         {'success': False,
                          'data': {},
                          'errorMessage': 'Необходимые параметры не указаны'})

        # Проверка на невалдиную ссылку
        urls = ['1111', '', 'dsfsdfsd', 'https://111.111', 'https://dddd2222.2222']
        for url in urls:
            self.assertEqual(get_list_courses_from_get_course({'url': url,
                                                               'email': 'dragg',
                                                               'password': '111'}),
                             {'success': False,
                              'data': {},
                              'errorMessage': 'Ссылка не валидная'})

        self.assertEqual(get_list_courses_from_get_course(
            {'url': 'https://valentina-krasnikova.ru/teach/control/stream/view/id/542901403',
             'email': 'dragg',
             'password': '111'}),
                         {'data': {},
                          'errorMessage': 'Неверный формат e-mail',
                          'success': False})
