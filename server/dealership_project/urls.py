from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.http import FileResponse, Http404
from django.urls import include, path
from django.views.generic import TemplateView


def react_app(_request):
    app_file = Path(settings.BASE_DIR.parent) / "frontend" / "client" / "dist" / "index.html"
    if not app_file.is_file():
        raise Http404("React app is not built. Run npm run build in frontend/client.")
    return FileResponse(app_file.open("rb"), content_type="text/html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("dealerships.urls")),
    path("about/", TemplateView.as_view(template_name="About.html"), name="about"),
    path("contact/", TemplateView.as_view(template_name="Contact.html"), name="contact"),
    path("", react_app, name="react-app"),
    path("<path:client_path>", react_app, name="react-client-route"),
]
