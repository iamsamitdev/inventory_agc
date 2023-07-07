from django import forms
from django.contrib import admin
from .models import Product, DataPoint
from ckeditor.widgets import CKEditorWidget

# Custom admin title
admin.site.site_header = 'AGC Inventory System'
admin.site.site_title = 'AGC Inventory System'
admin.site.index_title = 'Welcome to AGC Inventory System'


class ProductForm(forms.ModelForm):
    product_detail = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Product
        fields = '__all__'

# Register product model


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('product_name', 'product_barcode',
                    'product_qty', 'product_price', 'product_status')
    list_filter = ('product_name', 'product_barcode',
                   'product_qty', 'product_price', 'product_status')
    search_fields = ('product_name', 'product_detail', 'product_barcode',
                     'product_qty', 'product_price', 'product_image', 'product_status')
    ordering = ['product_name']
    fieldsets = (
        (None, {
            'fields': ('product_name', 'product_detail', 'product_barcode', 'product_qty', 'product_price', 'product_image', 'product_status')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('product_name', 'product_detail', 'product_barcode', 'product_qty', 'product_price', 'product_image', 'product_status')
        }),
    )

# Register DataPoint model


@admin.register(DataPoint)
class DataPointAdmin(admin.ModelAdmin):
    list_display = ('x_value', 'y_value')
    list_filter = ('x_value', 'y_value')
    search_fields = ('x_value', 'y_value')
    ordering = ['x_value']
    fieldsets = (
        (None, {
            'fields': ('x_value', 'y_value')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('x_value', 'y_value')
        }),
    )
