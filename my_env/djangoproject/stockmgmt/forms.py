from django import forms
from stockmgmt.models import Stock,StockHistory,Category

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name']
    # def clean_category(self):
    #     category = self.cleaned_data.get('category')
    #     if (category == ""):
    #         raise forms.ValidationError('This field cannot be left blank')
    #
    #     for instance in Stock.objects.all():
    #         if instance.category == category:
    #             raise forms.ValidationError('This Category are exist')
    #     return category
    #
    # def clean_item_name(self):
    #     name = self.cleaned_data.get('item_name')
    #     if (item_name == ""):
    #         raise forms.ValidationError('This fields is required')
    #     for instance in Stock.objects.all():
    #         if instance.item_name == item_name:
    #             raise forms.ValidationError('This Product Name are Exist')
    #     return item_name


class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    class Meta:
        model = Stock
        fields = ['category', 'item_name']


class StockHistorySearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)
    class Meta:
        model = StockHistory
        fields = ['category', 'item_name','start_date', 'end_date']

class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name','quantity']

class ExportForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['export_quantity', 'export_to']

class ImportForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['import_quantity', 'import_by']

class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
