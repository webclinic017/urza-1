from rest_framework.routers import DefaultRouter

from account.views import CreateUserView

router = DefaultRouter()
router.register(r'create/', CreateUserView)

urlpatterns = router.urls
