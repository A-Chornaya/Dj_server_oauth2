from django.contrib import admin

from .models import UserData
from .models import Client
from .models import Grant
from .models import AccessToken
from .models import RefreshToken


admin.site.register(UserData)
admin.site.register(Client)
admin.site.register(Grant)
admin.site.register(AccessToken)
admin.site.register(RefreshToken)
