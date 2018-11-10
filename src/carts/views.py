from django.shortcuts import render

# Create your views here.

def cart_home(request):
  # request.session.set_expiry(300) # 300 seconds == 5 minutes
  # print(dir(request.session))


  key = request.session.session_key # key for logged in user
  request.session['cart_id'] = 12 # set
  request.session['username'] = request.user.username # set
  request.session['username'] # get
  request.session.get('username', 'UnKnown') # get

  return render(request, 'carts/home.html', {})