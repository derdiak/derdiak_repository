from rest_framework import routers
from .views import CompanyViewSet, UserViewSet, TransferViewSet

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'users', UserViewSet)
router.register(r'transfers', TransferViewSet)

# URLs настраиваются автоматически роутером
urlpatterns = router.urls

