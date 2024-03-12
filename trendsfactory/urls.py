from django.contrib import admin
from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpView.as_view(),name="signup"),
    path('',views.SignInView.as_view(),name="signin"),
    path('index/',views.IndexView.as_view(),name="index"),
    path('products/<int:pk>/',views.ProductDetailView.as_view(),name="product-detail"),
    path('home',views.HomeView.as_view(),name="home"),
    path('products/<int:pk>/add_to_basket/',views.AddBasketView.as_view(),name="addto-basket"),
    path('basket/items/all/',views.BasketItemListView.as_view(),name="basket-items"),
    path('basket/items/<int:pk>/remove/',views.BasketItemRemoveView.as_view(),name="basketitem-remove"),
    path('basket/items/<int:pk>/qty/change',views.CartItemUpdateQuantityView.as_view(),name="editcart-qty"),
    path('checkout/',views.CheckOutView.as_view(),name="checkout"),
    path('signout/',views.SignOutView.as_view(),name="signout"),
    path('orders/summary/',views.OrderSummaryView.as_view(),name="order-summary"),
    path('orders/item/<int:pk>/remove/',views.OrderItemRemoveView.as_view(),name="order-item-remove"),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

