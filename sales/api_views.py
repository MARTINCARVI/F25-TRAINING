from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.db.models import Avg, F, Sum
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

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
from rest_framework import generics


from sales.serializers import (
    ArticleListAgregatedSerializer,
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


class CategoryArticleListCreateView(generics.ListCreateAPIView):

    """
    GET List of ALL Category article
    """

    permissions_classes = (permissions.IsAuthenticated,)
    queryset = ArticleCategory.objects.all()
    serializer_class = CategoryArticleSerializer

    """
    CREATE a new Category article
    """

    @extend_schema(
        request=CategoryArticleSerializer, responses={201: CategoryArticleSerializer}
    )
    # TODO : catch exception if category already exists (TRY / CATCH)

    def post(self, request):
        context = {"resquest": request}
        deserializer = CategoryArticleSerializer(data=request.data, context=context)
        deserializer.is_valid(raise_exception=True)
        try:
            new_category = ArticleCategory.objects.create(**deserializer.validated_data)
        except IntegrityError as e:
            raise exceptions.ValidationError({"display_name": "Already exists"})

        serializer = CategoryArticleSerializer(instance=new_category)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


###################################
# ARTICLE #
###################################


class ArticleListCreateView(generics.ListCreateAPIView):
    """
    GET List of all Articles
    """

    permissions_classes = (permissions.IsAuthenticated,)
    serializer_class = ArticleSerializer
    queryset = Article.objects.all().order_by("category")
    # DOES NOT WORK: WHY ?
    # filter_backends = [filters.OrderingFilter]
    ordering_fields = ["category"]

    """
    CREATE a new Article
    """
    # TODO : catch exception if category already exists (TRY / CATCH)

    @extend_schema(request=ArticleSerializer, responses={201: ArticleSerializer})
    def post(self, request, *args, **kwargs):
        deserializer = ArticleSerializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        try:
            new_article = Article.objects.create(**deserializer.validated_data)
        except ValidationError as e:
            raise exceptions.ValidationError({"code": "Already exists"})

        serializer = ArticleSerializer(instance=new_article)
        return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ArticleListAgregatedView(generics.ListAPIView):
    """
    GET List of all Sales sorted in the following manner:
    -> 'liste agrégée des ventes (paginée par 25 éléments également) par article avec catégorie associée,
    totaux des prix de vente, pourcentage de marge, date de la dernière vente,
    ordonnée par totaux des prix de vente décroissants.'
    """

    permissions_classes = (permissions.IsAuthenticated,)
    serializer_class = ArticleListAgregatedSerializer
    pagination_class = SalesPagination
    queryset = Article.objects.select_related("category").with_revenues_subquery()


###################################
# SALE #
###################################


class SaleListAgregatedView(generics.ListAPIView):
    """
    GET List of all Sales sorted in the following manner:
    -> 'liste agrégée des ventes (paginée par 25 éléments également) par article avec catégorie associée,
    totaux des prix de vente, pourcentage de marge, date de la dernière vente,
    ordonnée par totaux des prix de vente décroissants.'
    """

    permissions_classes = (permissions.IsAuthenticated,)
    serializer_class = SaleListAgregatedSerializer
    pagination_class = SalesPagination
    queryset = Sale.objects.with_revenues()


class SaleListCreateView(generics.ListCreateAPIView):
    """
    GET List of all Sales
    """

    permissions_classes = (permissions.IsAuthenticated,)
    serializer_class = SaleSerializer
    pagination_class = SalesPagination

    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["author"]

    """
    if the string 'author' is passed as query param, then the list of sales is filtered by the 
    user (author) making the request
    """
    # TODO: Use Django Filter Backend

    def get_queryset(self):
        # django drf query params
        queryset = Sale.objects.all().order_by("-unit_selling_price")
        author = self.request.query_params.get("author", None)
        if author is not None:
            queryset = queryset.filter(author=author)
        return queryset

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


class RetrieveUpdateDeleteSaleView(generics.RetrieveDestroyAPIView):
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

    # DELETE -> RetrieveDestroyAPIView does not provide any response: empty 204
    # """
    # Delete a Sale by sale_id
    # """
    # # SUPPRESS DELETE
    # @extend_schema(request=None, responses={204: None})
    # def delete(self, request, *args, **kwargs):
    #     sale = get_object_or_404(Sale, pk=kwargs["pk"])
    #     sale.delete()
    #     return response.Response("Sale deleted", status=status.HTTP_204_NO_CONTENT)
