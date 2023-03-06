"""ss_pdfreader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from read_pdf import views
from django.contrib.auth import views as auth_views


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('login/', auth_views.LoginView.as_view(), name="login"),
                  path('logout', views.logout_view, name='logout'),
                  path('', views.view_template),
                  path('create', views.create_template),
                  path('template_config', views.template_config),
                  path('approve', views.approve_template),
                  path('jobs', views.create_job),
                  path('show_jobs', views.show_jobs),
                  path('update/<int:p_id>', views.edit_update),
                  path('execute/<int:j_id>', views.execute),
                  path('view_result/<int:j_id>', views.view_result),
                  path('download_file/<int:j_id>', views.download_file),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
