from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import *

router = SimpleRouter()
router.register(r'carts', CartViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserProfileListApiView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserProfileDetailListView.as_view(), name='user_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('store/', StoreListApiView.as_view(), name='store_list'),
    path('store/<int:pk>/', StoreDetailView.as_view(), name='store_detail'),

    path('store/create/', StoreCreateApiView.as_view(), name='store_create'),
    path('store/create/<int:pk>', StoreEditApiView.as_view(), name='store_edit'),

    path('products/', ProductListApiView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailApiView.as_view(), name='product_detail'),
    path('products/create/', ProductCreateApiView.as_view(), name='product_create'),
    path('products/create/<int:pk>', ProductEditApiView.as_view(), name='product_edit'),

    path('product-combos/', ProductComboListApiView.as_view(), name='product_combo_list'),
    path('product-combos/<int:pk>/', ProductComboDetailApiView.as_view(), name='product_combo_detail'),
    path('product-combos/create/', ProductComboCreateApiView.as_view(), name='product_combo_create'),
    path('product-combos/create/<int:pk>', ProductComboEditApiView.as_view(), name='product_combo_edit'),

    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),

    path('contact_info/', ContactInfoListView.as_view(), name='contact_info_list'),
    path('contact_info/<int:pk>/', ContactInfoListView.as_view(), name='contact_info_detail'),

    path('couriers/', CourierApiView.as_view(), name='couriers_detail'),

    path('orders/', CartItemApiView.as_view(), name='order_list'),
    path('orders/create/', CartItemCreateApiView.as_view(), name='order_create'),
    path('orders/create/<int:pk>/', OrderEditApiView.as_view(), name='order_edit'),

    path('cart-items/', OrderListApiView.as_view(), name='cart-items_list'),
    path('cart-items/create/', OrderCreateApiView.as_view(), name='cart-items_create'),

    path('reviews/store/create/', StoreReviewCreateApiView.as_view(), name='store_review_create'),
    path('reviews/store/', StoreReviewListApiView.as_view(), name='store_review_list'),
    path('reviews/product/create/', ProductReviewCreateApiView.as_view(), name='product_review_create'),
    path('reviews/product/', ProductReviewListApiView.as_view(), name='product_review_list'),
    path('reviews/courier/create/', CourierReviewCreateApiView.as_view(), name='courier_review_create'),
    path('reviews/courier/', CourierReviewListApiView.as_view(), name='courier_review_list'),
]

