from django.test import TestCase
from meetmypeeps.models import Event
from django.contrib.gis.geos import Point
from django.utils.dateparse import parse_datetime


class TestEvents(TestCase):

    def test_can_save_POST_request(self):
        data, response = self.post_mock_data()
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.first()
        self.assertEqual(data['title'], event.title)

        date = parse_datetime(data['date'])
        self.assertEqual(date, event.date)

        coords = data['loc'].split(',')
        for coord in coords:
            self.assertIn(float(coord), event.location.coords)

    def test_redirects_after_post(self):
        data, response = self.post_mock_data()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_save_retrieve_events(self):
        first_event, second_event = self.create_mock_events()

        saved_items = Event.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.title, first_event.title)
        self.assertEqual(first_saved_item.location, first_event.location)
        self.assertEqual(first_saved_item.date, first_event.date)

        self.assertEqual(second_saved_item.title, second_event.title)
        self.assertEqual(second_saved_item.location, second_event.location)
        self.assertEqual(second_saved_item.date, second_event.date)

    def test_displays_own_events(self):
        first_event, second_event = self.create_mock_events()

        response = self.client.get('/')
        html = response.content.decode()

        self.assertIn(first_event.title, html)
        self.assertIn(second_event.title, html)

    def post_mock_data(self):
        data = {'loc': '52.2345504, 5.9870061',
                'title': 'Ma Bday Bash',
                'date': '2222-08-17T13:00:00+00:00',
                'submit': 'submit',
                }
        response = self.client.post('/', data=data)
        return data, response

    def create_mock_events(self):
        first_event = Event()
        first_event.title = '1st title'
        first_event.location = Point(52.2345504, 5.9870061)
        first_event.date = parse_datetime('2888-07-20T12:00:00+00:00')
        first_event.save()

        second_event = Event()
        second_event.title = '2nd title'
        second_event.location = Point(53.2435644, 4.9548342)
        second_event.date = parse_datetime('2999-08-15T17:15:00+00:00')
        second_event.save()

        return first_event, second_event
