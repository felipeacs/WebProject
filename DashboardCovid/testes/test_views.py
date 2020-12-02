from django.test import TestCase

from ..views import home, prepara_url


# Create your tests here.


class TestesViews(TestCase):
    def test_home_status_code(self):
        self.assertEqual(home('').status_code, 200)

    def test_home_return_text(self):
        self.assertEqual(home('').getvalue(), b'Hello World!')

    def test_prepara_url_start_date(self):
        country = 'brazil'
        start_date = '20200618'
        end_date = '20200618'
        self.assertEqual(prepara_url(country, start_date, end_date)[0],
                         'https://covid19-brazil-api.now.sh/api/report/v1/{}/{}/'.format(country, start_date))

    def test_prepara_url_start_date_end_null(self):
        country = 'brazil'
        start_date = '20200618'
        end_date = ''
        self.assertEqual(prepara_url(country, start_date, end_date)[0],
                         'https://covid19-brazil-api.now.sh/api/report/v1/{}/{}/'.format(country, start_date))

    def test_prepara_url_start_end_date(self):
        country = 'brazil'
        start_date = '20200618'
        end_date = '20200718'
        self.assertEqual(prepara_url(country, start_date, end_date)[0],
                         'https://covid19-brazil-api.now.sh/api/report/v1/{}/{}/'.format(country, start_date))
