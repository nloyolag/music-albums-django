# Python imports
from time import timezone
from datetime import datetime

# Django imports
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Rest Framework imports
from rest_framework import status
from rest_framework.test import APITestCase

# Music Albums imports
from music_albums import models
from music_albums import common

################################################################################
#
# Class: TestHomeView
# Description: Test methods from the Home view
#
# Pieces of code tested:
#       - Cannot create an album with a future date
#       - View displays correct message after form submission
#       - Display albums correctly
#       - Display message if no albums are available
#
################################################################################

def create_album(title, days, rating):
    """
    Creates an album with the given attributes. Used in the test cases.
    It receives days to create a datetime relative to the current one.
    """
    release_date = timezone.now() + datetime.timedelta(days=days)
    return models.Album.objects.create(
        title=title,
        release_date=release_date,
        rating=rating
    )

class TestHomeView(TestCase):

    def test_future_album_error(self):
        """
        Check if the view sends an error when receiving a date from
        the future.
        """
        new_album = {
            title: "Galactic Warfare",
            release_date: timezone.now() + datetime.timedelta(days=5),
            rating: models.Album.THREE
        }
        response = self.client.post(reverse('home'), new_album)
        self.assertContains(response, common.ERROR__FUTURE_ALBUM, 200)

    def test_correct_album_submission(self):
        """
        Check if an album is created correctly and a success message is shown.
        """
        new_album = {
            title: "Justin Bieber Greatest Hits",
            release_date: timezone.now() + datetime.timedelta(days=-5),
            rating: models.Album.ONE
        }
        response = self.client.post(reverse('home'), new_album)
        self.assertContains(
            response,
            common.MESSAGE__ALBUM_CORRECTLY_CREATED,
            200
        )

    def test_home_view_with_albums(self):
        """
        Check if albums are obtained correctly.
        """
        create_album(title="White Album", days=-30, rating=models.Album.FOUR)
        create_album(title="Grace", days=-100, rating=models.Album.FIVE)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['albums'],
            ['<Album: White Album>', '<Album: Grace>']
        )

    def test_empty_home_view(self):
        """
        If no albums exist, display an adequate message.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, common.MESSAGE__NO_ALBUMS_TO_SHOW)
        self.assertQuerysetEqual(response.context['albums'], [])
