from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',                                 'Bot.views.index.page',           name="index"),
    url(r'^connect$',                          'Bot.views.connect.page',         name="connect"),
    url(r'^create_user$',                      'Bot.views.create_user.page',     name="create_user"),
	url(r'^logout$',                           'Bot.views.logout.page',          name="logout"),
	url(r'^accounts/login/',                   'Bot.views.not_loggedin.page',    name='not_loggedin'),
    url(r'^chat$',                             'Bot.views.chat.page',            name="chat"),
	url(r'^webhook$',                          'Bot.views.webhook.page',         name="webhook"),
	url(r'^privacypolicy$',                    'Bot.views.privacypolicy.page',   name="privacypolicy"),
	url(r'^suggestion$',                       'Bot.views.suggestion.page',      name="suggestion"),
	url(r'^otp$',                              'Bot.views.otp.page',             name="otp"),

	url(r'^accounts/confirm/(?P<activation_key>\w+)$', 'Bot.views.register_confirm.page',         name='email_confirm'),
]
