from django_filters.rest_framework import DjangoFilterBackend
from balances.models import Balances
from products.models import Products
from brands.models import Brands
from users.models import User
from locations.models import (
    Locations, City, Governorate
)
from faqs.models import Faqs
from operator import and_, or_
from django.db.models import Q
from functools import reduce
import django_filters


class BalanceFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_q", help_text="should be string search in `product title` or `brand name` or `metal type name`")
    sort = django_filters.BooleanFilter(method='filter_sort', help_text="should be boolean. sorted by purchase date")
    
    def filter_q(self, queryset, name, value):
        if value:
            query = reduce(and_, [
                                #   Q(gm_price=keyword) | 
                                #   Q(purchase_price=keyword) |
                                #   Q(purchase_date=keyword) |
                                  Q(product__title__icontains=keyword) |
                                  Q(product__brand__name__icontains=keyword) |
                                  Q(product__metal_type__name__icontains=keyword)
                                  for keyword in value.split()])

            return queryset.filter(query)

        return queryset
    
    def filter_sort(self, queryset, name, value):
        
        if value:
            return queryset.order_by('purchase_date')

        return queryset
    
    class Meta:
        model = Balances
        fields = ('search',)
    

class BrandFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_q", help_text="should be string. search in name")

    def filter_q(self, queryset, name, value):
        if value:
            query = reduce(and_, [Q(name__icontains=k) for k in value.split()])
            return queryset.filter(query)
        
        return queryset

    class Meta:
        model = Brands
        fields = ('search','is_popular')
  
  
class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_q', help_text="should be string. search in `product name` or `brand name` or `meta type name`")
    sort = django_filters.BooleanFilter(method="filter_sort", help_text="should be boolean. sorted by created at")  
    
    
    def filter_q(self, queryset, name, value):
        if value:
            query = reduce(and_, [Q(title__icontains=k) |
                                  Q(metal_type__name__icontains=k) |
                                  Q(brand__name__icontains=k)
                                  for k in value.split()])
            
            return queryset.filter(query)
        
        return queryset
    
    def filter_sort(self, queryset, name, value):
        if value:
            return queryset.order_by('created_at')
        
        return queryset
    
    class Meta:
        model = Products
        fields = ('search', 'is_available', 'is_popular')


class UserFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_q", help_text="should be string. search in 'username' or `first / last name` or `email`")
    sort = django_filters.BooleanFilter(method="filter_sort", help_text="should be boolean. sorted by `date joined`")
    
    def filter_q(self, queryset, name, value):
        if value:
            query = reduce(and_, [Q(username__icontains=k) |
                                  Q(first_name__icontains=k) |
                                  Q(last_name__icontains=k) |
                                  Q(email__icontains=k)
                                  for k in value.split()])
            
            return queryset.filter(query)
        
        return queryset

    def filter_sort(self, queryset, name, value):
        if value:
            return queryset.order_by('date_joined')
        
        return queryset
    
    class Meta:
        model = User
        fields = ('search', 'is_active', 'is_deleted', 'is_email_verified')


class CityFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_q", help_text="should be string. search in 'name' or `name in arabic`")
    
    def filter_q(self, queryset, name, value):
        if value:
            query = reduce(and_, [Q(name__icontains=k) |
                                  Q(name_ar__icontains=k)
                                  for k in value.split()])
            
            return queryset.filter(query)
        
        return queryset
    
    class Meta:
        model = City
        fields = ('search',)


class GovernorateFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_q", help_text="should be string. search in 'name' or `name in arabic`")
    
    def filter_q(self, queryset, name, value):
        if value:
            query = reduce(and_, [Q(name__icontains=k) |
                                  Q(name_ar__icontains=k)
                                  for k in value.split()])
            
            return queryset.filter(query)
        
        return queryset
    
    class Meta:
        model = Governorate
        fields = ('search',)
        

class LocationFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_q", 
                                       help_text='''should be string. 
                                       search in 'merchant name' or 
                                       `address line 1 / 2` 
                                       or `city name / name_ar` 
                                       or `governorate name / name_ar`''')
    
    def filter_q(self, queryset, name, value):
        if value:
            query = reduce(and_, [Q(merchant_name__icontains=k) |
                                  Q(address_line_1__icontains=k)|
                                  Q(address_line_2__icontains=k)|
                                  Q(city__name__icontains=k) |
                                  Q(city__name_ar__icontains=k) |
                                  Q(governorate__name__icontains=k) |
                                  Q(governorate__name_ar__icontains=k) 
                                  for k in value.split()])
            
            return queryset.filter(query)
        
        return queryset
    
    class Meta:
        model = Locations
        fields = ('search',)
     

class FaqsFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_q", help_text="should be string. search in 'question_body' or `answer`")
    sort = django_filters.BooleanFilter(method="filter_sort", help_text="should be boolean. sorted by `sort_order`")
    
    def filter_q(self, queryset, name, value):
        if value:
            query = reduce(and_, [Q(question_body__icontains=k) |
                                  Q(answer__icontains=k)
                                  for k in value.split()])
            
            return queryset.filter(query)
        
        return queryset

    def filter_sort(self, queryset, name, value):
        if value:
            return queryset.order_by('sort_order')
        
        return queryset
    
    class Meta:
        model = Faqs
        fields = ('search', 'num_useful', 'num_unuseful')


__all__ = [
    'DjangoFilterBackend',
    'BalanceFilter',
    'BrandFilter',
    'ProductFilter',
    'UserFilter',
    'CityFilter',
    'GovernorateFilter',
    'LocationFilter',
    'FaqsFilter'
]