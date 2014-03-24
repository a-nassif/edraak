"""
Middleware that checks user standing for the purpose of keeping users with
disabled accounts from accessing the site.
"""
from django.http import HttpResponseForbidden
from django.utils.translation import ugettext as _
from django.conf import settings
from student.models import UserStanding
from django.utils.cache import patch_vary_headers
from django.utils import translation
class UserStandingMiddleware(object):
    """
    Checks a user's standing on request. Returns a 403 if the user's
    status is 'disabled'.
    """
    def process_request(self, request):
        user = request.user
        try:
            user_account = UserStanding.objects.get(user=user.id)
            # because user is a unique field in UserStanding, there will either be
            # one or zero user_accounts associated with a UserStanding
        except UserStanding.DoesNotExist:
            pass
        else:
            if user_account.account_status == UserStanding.ACCOUNT_DISABLED:
                msg = _(
                            'Your account has been disabled. If you believe '
                            'this was done in error, please contact us at '
                            '{link_start}{support_email}{link_end}'
                        ).format(
                            support_email=settings.DEFAULT_FEEDBACK_EMAIL,
                            link_start=u'<a href="mailto:{address}?subject={subject_line}">'.format(
                                address=settings.DEFAULT_FEEDBACK_EMAIL,
                                subject_line=_('Disabled Account'),
                            ),
                            link_end=u'</a>'
                        )
                return HttpResponseForbidden(msg)


class ForceLangMiddleware(object):

    def process_request(self, request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del request.META['HTTP_ACCEPT_LANGUAGE']
        if 'LANG' in request.environ:
            del request.environ['LANG']


class SessionBasedLocaleMiddleware(object):
    """
    This Middleware saves the desired content language in the user session.
    The SessionMiddleware has to be activated.
    """
    def process_request(self, request):
        if request.method == 'GET' and 'lang' in request.GET:
            if 'language_flag' in request.session and request.session['language_flag']:
                language = request.session['language_reference']
                request.session['language_flag'] = False
            else:
                language = request.GET['lang']
            request.session['language'] = language
        elif 'django_language' in request.session and 'language' in request.POST:
            language = request.POST['language']
            request.session['language_reference'] = request.POST['language']
            request.session['language_flag'] = True
        else:
            language = translation.get_language_from_request(request)

        for lang in settings.LANGUAGES:
            if lang[0] == language:
                translation.activate(language)

        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response