from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import *
from .serializers import *
from rest_framework import viewsets, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import *
from .permissions import *
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .paginations import ProductResultsSetPagination



class RegisterView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail':' неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileListApiView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSimpleSerializer

    # каждыый user будет смотреть свой профиль
    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class UserProfileDetailListView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    # каждыый user будет смотреть свой профиль
    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class StoreListApiView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    pagination_class = ProductResultsSetPagination


class StoreCreateApiView(generics.CreateAPIView):
    serializer_class = StoreSerializer
    permission_classes = [CheckUserCreate]
    def get_queryset(self):
        return Store.objects.filter(owner=self.request.user)


class StoreEditApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [CheckUserCreate]

    # только owner сможет изменить
    def get_queryset(self):
        return Store.objects.filter(owner=self.request.user)


class StoreDetailView(generics.RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreDetailSerializer


class ContactInfoListView(generics.ListAPIView):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer


class ProductListApiView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('price')
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductListFilter


class ProductDetailApiView(generics.RetrieveAPIView):
    queryset = Product.objects.all().order_by('price')
    serializer_class = ProductDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductListFilter


class ProductCreateApiView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [CheckUserCreate]

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)


class ProductEditApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)


class ProductComboListApiView(generics.ListAPIView):
    queryset = ProductCombo.objects.all().order_by('price')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    serializer_class = ProductListComboSerializer
    filterset_class = ProductComboListFilter


class ProductComboDetailApiView(generics.RetrieveAPIView):
    queryset = ProductCombo.objects.all().order_by('price')
    serializer_class = ProductComboDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductComboListFilter


class ProductComboCreateApiView(generics.CreateAPIView):
    serializer_class = ProductComboSerializer
    permission_classes = [CheckUserCreate]

    def get_queryset(self):
        return ProductCombo.objects.filter(owner=self.request.user)


class ProductComboEditApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCombo.objects.all()
    serializer_class = ProductComboSerializer

    def get_queryset(self):
        return ProductCombo.objects.filter(owner=self.request.user)



class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class CartItemApiView(generics.ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class CartItemCreateApiView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemCreateSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class StoreReviewCreateApiView(generics.CreateAPIView):
    queryset = ReviewStore.objects.all()
    serializer_class = StoreReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckReviewUser, CheckReviewEdit]

    def perform_create(self, serializer):
        serializer.save(user_name=self.request.user)


class StoreReviewListApiView(generics.ListAPIView):
    queryset = ReviewStore.objects.all()
    serializer_class = StoreReviewSerializer


class ProductReviewCreateApiView(generics.CreateAPIView):
    queryset = ReviewProduct.objects.all()
    serializer_class = ProductReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckReviewUser, CheckReviewEdit]

    def perform_create(self, serializer):
        serializer.save(user_name=self.request.user)


class ProductReviewListApiView(generics.ListAPIView):
    queryset = ReviewProduct.objects.all()
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        return ReviewProduct.objects.filter(id=self.request.user.id)


class CourierReviewCreateApiView(generics.CreateAPIView):
    queryset = ReviewCourier.objects.all()
    serializer_class = CourierReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,CheckReviewUser, CheckReviewEdit]

    def perform_create(self, serializer):
        serializer.save(user_name=self.request.user)


class CourierReviewListApiView(generics.ListAPIView):
    queryset = ReviewCourier.objects.all()
    serializer_class = CourierReviewSerializer


class OrderCreateApiView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckReviewUser]

    def get_queryset(self):
        return Order.objects.filter(client_order=self.request.user)


class OrderListApiView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [CheckReviewUser]

    def get_queryset(self):
        return Order.objects.filter(client_order=self.request.user)


class OrderEditApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckCourierUser]


    def get_queryset(self):
        return Order.objects.filter(client_order=self.request.user)



class CourierApiView(generics.ListAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    permission_classes = [CheckCourierUser]

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)
