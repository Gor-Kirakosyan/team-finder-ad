from django.http import HttpResponse
from django.views import View
import sys

class ProjectListView(View):
    def get(self, request):
        print("VIEW IS CALLED!", file=sys.stderr)
        return HttpResponse("Hello World! Project list works!")