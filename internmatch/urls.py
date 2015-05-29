from django.conf.urls import include, url
from django.contrib import admin
from login_process import urls as login_urls
from skills import urls as skills_urls
from survey import urls as survey_urls
from django.conf import settings
from django.conf.urls.static import static
from upload import urls as upload_urls
from reference import urls as ref_urls
from job import urls as job_urls
from profiles import urls as profile_urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'internmatch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(login_urls)),
    url(r'^', include(skills_urls)),
    url(r'^', include(survey_urls)),
    url(r'^', include(upload_urls)),
    url(r'^', include(ref_urls)),
    url(r'^', include(job_urls)),
    url(r'^', include(profile_urls)),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
