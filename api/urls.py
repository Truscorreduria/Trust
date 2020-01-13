from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register('brands', MarcaViewSet, 'brands')
router.register('years', AnnoViewSet, 'years')
router.register('models', ModeloViewSet, 'models')

urlpatterns = router.urls