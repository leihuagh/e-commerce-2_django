from django.shortcuts import render

# Create your views here.

def cart_home(request):
  # request.session.set_expiry(300) # 300 seconds == 5 minutes
  # print(dir(request.session))
  # key = request.session.session_key # key for logged in user
  # request.session['cart_id'] = 12 # set
  # request.session['username'] = request.user.username # set
  # request.session['username'] # get
  # request.session.get('username', 'UnKnown') # get


  cart_id = request.session.get('cart_id', None)
  if cart_id is None:# and isinstance(cart_id, int):
    print('careate new cart')
    request.session['cart_id'] = 12
  else:
    print('Cart ID exists')
  return render(request, 'carts/home.html', {})