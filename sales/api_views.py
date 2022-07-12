from django.shortcuts import get_object_or_404
from django.db.models import Avg, F, Sum
from drf_spectacular.utils import extend_schema

# from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import (
    mixins,
    viewsets,
    exceptions,
    permissions,
    response,
    status,
    views,
    serializers,
    generics,
    filters,
)
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from sales.serializers import (
    ArticleSerializer,
    CategoryArticleSerializer,
    UpdateSaleDeserializer,
    UpdateSaleSerializer,
    SaleListAgregatedSerializer,
    SaleCreateDeserializer,
    SaleCreateSerializer,
    SaleSerializer,
)

from sales.models import Article, ArticleCategory, Sale
from sales.pagination import SalesPagination

###################################
# CATEGORY ARTICLE #
###################################


class CategoryArticleCreateView(views.APIView):
    permissions_classes = (permissions.IsAuthenticated,)
    """
    CREATE a new Category article
    """

    @extend_schema(
        request=CategoryArticleSerializer, responses={201: CategoryArticleSerializer}
    )
    def post(self, request):
        context = {"resquest": request}
        deserializer = CategoryArticleSerializer(data=request.data, context=context)
        deserializer.is_valid(raise_exception=True)
        new_category = ArticleCategory.objects.create(**deserializer.validated_data)
        serializer = CategoryArticleSerializer(instance=new_category)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


###################################
# ARTICLE #
###################################


class ArticleListView(ListCreateAPIView):
    """
    GET List of all Articles
    """

    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    """
    CREATE a new Article
    """

    @extend_schema(request=ArticleSerializer, responses={201: ArticleSerializer})
    def post(self, request, *args, **kwargs):
        deserializer = ArticleSerializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        new_article = Article.objects.create(**deserializer.validated_data)
        serializer = ArticleSerializer(instance=new_article)
        return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)


###################################
# SALE #
###################################


class SaleListAgregatedView(ListAPIView):
    """
    GET List of all Sales sorted in the following manner:
    -> 'liste agrégée des ventes (paginée par 25 éléments également) par article avec catégorie associée,
    totaux des prix de vente, pourcentage de marge, date de la dernière vente,
    ordonnée par totaux des prix de vente décroissants.'
    """

    total_sale_price = F("unit_selling_price") * F("quantity")
    total_sale_cost = F("manufacturing_cost") * F("quantity")
    business_revenue = Sum(total_sale_price)
    margin_percentage_per_sale = (
        100 * (total_sale_price - total_sale_cost) / total_sale_cost
    )

    permissions_classes = (permissions.IsAuthenticated,)
    serializer_class = SaleListAgregatedSerializer
    pagination_class = SalesPagination

    def get_queryset(self):
        return (
            Sale.objects.all()
            .select_related("article__category")
            .values("article")
            .annotate(
                business_revenue=Sum(F("unit_selling_price") * F("quantity")),
                margin_percentage_per_sale=(
                    F("unit_selling_price") - F("article__manufacturing_cost")
                )
                / F("article__manufacturing_cost"),
            )
            .order_by("-business_revenue")
        )


class SaleListAllView(ListAPIView):
    """
    GET List of all Sales
    """

    permissions_classes = (permissions.IsAuthenticated,)
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    pagination_class = SalesPagination


class SaleListAuthorView(ListAPIView):
    """
    GET List of Sales, of the connected user only !
    """

    permissions_classes = (permissions.IsAuthenticated,)
    serializer_class = SaleSerializer
    pagination_class = SalesPagination

    def get_queryset(self):
        user = self.request.user
        return Sale.objects.filter(author=user.pk)


class SaleCreateView(views.APIView):
    permissions_classes = (permissions.IsAuthenticated,)
    """
    CREATE a new Sale
    """

    @extend_schema(
        request=SaleCreateDeserializer,
        responses={201: SaleCreateSerializer},
    )
    def post(self, request, *args, **kwargs):
        deserializer = SaleCreateDeserializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        new_sale = Sale.objects.create(
            **deserializer.validated_data, author=request.user
        )
        serializer = SaleCreateSerializer(instance=new_sale)
        return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDeleteSaleView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve (Get) a Sale by sale_id
    """

    permissions_classes = (permissions.IsAuthenticated,)
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()

    """
    Update Sale:
     - the author (user who made the sale) cannot be modified.
     - the date of the sale cannot be modified.
    """

    @extend_schema(
        request=UpdateSaleDeserializer, responses={202: UpdateSaleSerializer}
    )
    def put(self, request, *args, **kwargs):
        sale = self.get_object()
        deserializer = UpdateSaleDeserializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        sale.update(**deserializer.validated_data)
        serializer = UpdateSaleSerializer(instance=sale)
        return response.Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    """
    Delete a Sale by sale_id
    """

    @extend_schema(request=None, responses={204: None})
    def delete(self, request, *args, **kwargs):
        sale = get_object_or_404(Sale, pk=kwargs["pk"])
        sale.delete()
        return response.Response("Sale deleted", status=status.HTTP_204_NO_CONTENT)
