from django.forms import ModelForm
from Order.models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['name' , 'family' , 'phone' ,  'email' , 'address1' , 'address2' , 'post_code']


    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for filed in self.fields:
            self.fields[filed].widget.attrs['class'] = 'span4'