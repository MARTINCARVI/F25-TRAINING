from email.policy import default
from rest_framework import serializers
from datetime import date
from sales.models import ArticleCategory, Article, Sale
from users.models import User

###################################
# CATEGORY ARTICLE #
###################################
class CategoryArticleSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    display_name = serializers.CharField()


###################################
# ARTICLE #
###################################
class ArticleSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    code = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(
        queryset=ArticleCategory.objects.all()
    )
    name = serializers.CharField()
    manufacturing_cost = serializers.DecimalField(max_digits=5, decimal_places=2)

    # class Meta:
    #     model = Article
    #     fields = '__all__'

    # def create(self, validated_data):
    #     return Article.objects.create(**validated_data)


###################################
# SALE #
###################################


class SaleListAgregatedSerializer(serializers.Serializer):

    # Special calculated fields:
    business_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    margin_percentage_per_sale = serializers.DecimalField(
        max_digits=10, decimal_places=2
    )

    # Retrieved fields:
    # article__category__display_name = serializers.CharField()
    # sale__article__manufacturing_cost = serializers.DecimalField(
    #     max_digits=11, decimal_places=2
    # )
    # article_name = serializers.CharField(source="article.name")
    # category_name = serializers.CharField(source="article.category.display_name")
    # article__category_id = serializers.IntegerField(read_only=True)

    # article_id = serializers.IntegerField(read_only=True)
    pk = serializers.IntegerField(read_only=True)
    article = serializers.IntegerField(read_only=True)
    # quantity = serializers.IntegerField()
    # unit_selling_price = serializers.DecimalField(max_digits=11, decimal_places=2)


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = "__all__"


class SaleCreateDeserializer(serializers.Serializer):
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())
    quantity = serializers.IntegerField()
    unit_selling_price = serializers.DecimalField(max_digits=11, decimal_places=2)


class SaleCreateSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    date = serializers.DateField()
    article = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    quantity = serializers.IntegerField()
    unit_selling_price = serializers.DecimalField(max_digits=11, decimal_places=2)


class UpdateSaleDeserializer(serializers.Serializer):
    # date = serializers.DateField()
    article = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    quantity = serializers.IntegerField()
    unit_selling_price = serializers.DecimalField(max_digits=11, decimal_places=2)


class UpdateSaleSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    date = serializers.DateField()
    article = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    quantity = serializers.IntegerField()
    unit_selling_price = serializers.DecimalField(max_digits=11, decimal_places=2)
