from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,DetailView
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from store.forms import RegistrationForm,LoginForm
from store.models import Product,BasketItem,Size,Order,OrderItems
from store.decorators import  signin_required,owner_permission_required



# Create your views here.

def signin_required(fn):

    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else: 
            return fn(request,*args,**kwargs)
        return wrapper



# url:localhost:8000/register/
# method:get,post
# form_class:RegistrationForm

class SignUpView(View):

    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
        return render(request,"login.html",{"form":form})
    
# url:localhost:8000/
# method:get,post
# form_class:LoginForm
    
class SignInView(View):
    def get(self,request,*args,**Kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
           u_name=form.cleaned_data.get("username")
           pwd=form.cleaned_data.get("password")
           user_object=authenticate(request,username=u_name,password=pwd)
           if user_object:
              login(request,user_object)
              return redirect("index")
        messages.error(request,"invalid credentials")
        return render(request,"login.html",{"form":form})



# views=>generics=>view,templateview,deleteview,createview,updateview...
# localhost:8000/index/ 
@method_decorator([signin_required,never_cache],name="dispatch")     
class IndexView(View):
    def get(self,request,*args,**kwargs):
        qs=Product.objects.all()
        return render(request,"index.html",{"data":qs})
    

#url:localhost:8000/products/{id}/
@method_decorator([signin_required,never_cache],name="dispatch")           
class ProductDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Product.objects.get(id=id)
        return render(request,"product_detail.html",{"data":qs})                                          


class HomeView(TemplateView):
    template_name="base.html"

@method_decorator([signin_required,never_cache],name="dispatch")     
class AddBasketView(View):
    def post(self,request,*args,**kwargs):
        size=request.POST.get("size")
        size_obj=Size.objects.get(name=size)
        qty=request.POST.get("qty")
        id=kwargs.get("pk")
        product_obj=Product.objects.get(id=id)    
        BasketItem.objects.create(
            size_object=size_obj,
            qty=qty,
            product_object=product_obj,
            basket_object=request.user.cart
        )
        return redirect("index")
    

@method_decorator([signin_required,never_cache],name="dispatch")          
class BasketItemListView(View):
    def get(self,request,*args,**kwargs):
        qs=request.user.cart.cartitem.filter(is_order_placed=False)
        return render(request,"cart_list.html",{"data":qs})
    

# basket item remove
# localhost:8000/basket/items/{id}/remove/


@method_decorator([signin_required,owner_permission_required,never_cache],name="dispatch")   
class BasketItemRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        basket_item_object=BasketItem.objects.get(id=id)
        basket_item_object.delete()
        return redirect("basket-items")


@method_decorator([signin_required,owner_permission_required,never_cache],name="dispatch")   
class CartItemUpdateQuantityView(View):
    def post(self,request,*args,**kwargs):
        action=request.POST.get("counterbutton")
        print(action)
        id=kwargs.get("pk")
        basket_item_object=BasketItem.objects.get(id=id)

        if action=="+":
            basket_item_object.qty+=1
            basket_item_object.save()
        else:
            basket_item_object.qty-=1
            basket_item_object.save()  
              
        return redirect("basket-items")
    


class CheckOutView(View):
    
    def get(self,request,*args,**kwargs):
        return render(request,"checkout.html")
    
    def post(self,request,*args,**kwargs):
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        address=request.POST.get("address")

        # create order instance

        order_obj=Order.objects.create(
            user_object=request.user,
            delivery_address=address,
            phone=phone,
            email=email,
            total=request.user.cart.basket_total
        )
        # creating order_item instance

        try:
            basket_items=request.user.cart.cart_items
            for bi in basket_items:
                OrderItems.objects.create(
                    order_object=order_obj,
                    basket_item_object=bi

            )
            bi.is_order_placed=True
            bi.save()
        except:
            order_obj.delete()
        finally:
            return redirect("index")

@method_decorator([signin_required,never_cache],name="dispatch")   
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout=(request)
        return redirect("signin") 
       


class OrderSummaryView(View):
    def get(self,request,*args,**kwargs):
        qs=Order.objects.filter(user_objects=request.user)
        return render(request,"order_summary.html",{"data":qs})
    