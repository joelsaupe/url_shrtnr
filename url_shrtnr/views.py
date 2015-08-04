from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from models import Url
import urllib
from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from django.core.validators import URLValidator


class UrlLoader(View):
    """
    Redirect handler. This view translates the slug and takes the user to the actual destination.

    :Author: Joel Saupe
    """
    def get(self, request, slug=None):
        try:
            # Find the slug in the db.
            slug = urllib.quote(slug)
            url = Url.objects.get(slug=slug)
            # Increase the view count for statistical purposes.
            url.views = url.views + 1
            url.save()
            # Redirect the user.
            return HttpResponseRedirect(url.url)
        except:
            return redirect('/shrtnr/')


class UrlAPI(View):
    """
    API view for checking and creating new shortened URLs.

    :Author: Joel Saupe
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UrlAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """
        Takes a slug in as a GET parameter and returns the long url it is related to.
        This is used to check if a slug is available or not.

        :Return: Long URL for this slug. Empty string if none.
        """
        slug = request.GET.get('slug', None)
        if slug:
            slug = urllib.quote(slug)
            try:
                url = Url.objects.get(slug=slug)
                return HttpResponse(url.url)
            except:
                pass
        return HttpResponse('')

    def post(self, request):
        """
        Saves a new URL to the db. Accepts a long url and a possible slug as post parameters.

        * If the long url can't be validated then error 404 is returned.
        * If the requested slug has already been taken, then a new slug will be generated and
            returned on success.
        * If there is not a requested slug, then one will be generated and returned on success.
        * If there is not a requested slug and the requested URL already has a slug generated,
            then the previous slug is returned.

        :Return: Saved slug
        """
        # Make sure the slug is url safe.
        requested_slug = request.POST.get('requested_slug', None)
        if requested_slug:
            requested_slug = urllib.quote(requested_slug)
        requested_url = request.POST.get('requested_url', None)

        # Validate the requested url.
        if not requested_url.startswith('http://') and not requested_url.startswith('https://'):
            requested_url = 'http://%s' % requested_url
        try:
            validator = URLValidator()
            validator(requested_url)
        except:
            return Http404('URL Invalid')

        # Find the proper slug for this url.
        if slug_available(requested_slug):
            slug = requested_slug
        else:
            # If a slug was requested and it was taken, maybe it was taken by this url before.
            # If that is the case, then we should return that one to the user. Otherwise, try
            # to find a different slug already made for this url. If unable to find a slug
            # prevously created for this url, then make a new one.
            try:
                try:
                    existing = Url.objects.get(url=requested_url, slug=requested_slug)
                except:
                    existing = Url.objects.filter(url=requested_url)[0]
                # We already have a record in the db, so we can just return now without creating.
                return HttpResponse(existing.slug)
            except:
                slug = generate_slug(4)
        # Save the new shortened url to the db.
        shortened_url = Url(
                url=requested_url,
                slug=slug
            )
        shortened_url.save()
        # Return the saved slug to the user so they can copy and use it.
        return HttpResponse(slug)


def generate_slug(length):
    """
    Generates a random slug of given length.
    :Returns: Unique Slug
    :Author: Joel Saupe

    Note:
        In order to make sure a slug is generated, the generator will make at most 10 attempts
        at creating an available slug with the requested number of characters. If unsuccessful,
        the generator will attempt to create a slug with one extra character. This will repeat
        until an unused slug is created.
        10 attempts is an arbitrary number, but necessary to ensure a random slug will always
        be returned.
    """
    if length < 0:
        length = 0
    attempts = 0
    # Generate random strings until one is aavailable to be used.
    while True:
        random_string = get_random_string(length)
        if slug_available(random_string):
            return random_string
        # Increase the attempts count each time, increase the length generated after every 10 attempts.
        attempts += 1
        if attempts % 10 == 0:
            length += 1


def slug_available(slug):
    """
    Queries the db to see if the requested slug is already in use.
    :Returns: boolean

    :Author: Joel Saupe
    """
    if not slug:
        return False
    try:
        url = Url.objects.get(slug=slug)
        return False
    except:
        return True
