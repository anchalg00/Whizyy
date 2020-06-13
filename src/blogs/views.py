from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import login, authenticate, logout
from users.forms import RegistrationForm,AccountAuthenticationForm
from .models import BlogPost,Category
from .forms import BlogForm,CommentForm
from django.contrib.auth.decorators import login_required
from users.models import Account,UserFollowing
from .models import Comment
import simplejson as json
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.forms.models import model_to_dict
# Create your views here.

def home_view(request,*args,**kwargs):
	context = {}
	all_blog=BlogPost.objects.all()
	
	
	context={
	'all_blog':all_blog,
	}
	
	return render(request, 'home.html', context)



def login_view(request):
	#####LOGIN FORM ###########
	if request.POST:
		login_form = AccountAuthenticationForm(request.POST)
		if login_form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("blogs", category_id=0)

	else:
		login_form = AccountAuthenticationForm()


	if request.POST:
		register_form = RegistrationForm(request.POST)
		if register_form.is_valid():
			register_form.save()
			email = register_form.cleaned_data.get('email')
			raw_password = register_form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect("blogs", category_id=0)
		
			
	else: 
		register_form = RegistrationForm()
		
	user = request.user
	


	context={
	'login_form':login_form,
	'register_form':register_form,

	}
	return render(request, 'login.html', context)




def logout_view(request):
	logout(request)
	return redirect ('home')

def blog_view(request,category_id):
	category_list=Category.objects.all()
	
	if category_id==0:
		all_blog=BlogPost.objects.all()
	else:
		all_blog=BlogPost.objects.filter(category_id=category_id)
	context={
	'all_blog': all_blog,
	'category_list':category_list
	}
	return render(request,'main_blog.html',context)

def write_blog(request):
	if request.method=='POST':
		form = BlogForm(request.POST, request.FILES)
		if form.is_valid():
			obj= form.save(commit=False)
			obj.author=request.user				
			obj.save()
			return redirect('home')
	else:
		form=BlogForm()
	return render(request,'writeblog.html',{'form':form})

@login_required()
def userpage_view(request,username):
	user=Account.objects.get(username=username)
	followers_count=user.followers.all().count()
	blog_list1=BlogPost.objects.filter(author=user)
	is_follower=False	
	for element in user.followers.all():
		if request.user==element.user_id:
			is_follower=True
	context={
	'followers_count':followers_count,
	'is_follower':is_follower,
	'profile_user': user,
	'blog_list1':blog_list1,
	}	
	return render(request,'userpage.html',context)


@login_required()
def follow_view(request,username):
	user=Account.objects.get(username=username)
	print(user)
	UserFollowing.objects.create(user_id=request.user,
                             following_user_id=user)
	
	return redirect('userpage', username=username)


@login_required()
def unfollow_view(request,username):
	user=Account.objects.get(username=username)
	element=UserFollowing.objects.get(user_id=request.user,
                             following_user_id=user)
	element.delete()
	
	return redirect('userpage', username=username)

def single_blog_view(request,blogslug):
	single_blog=BlogPost.objects.get(slug=blogslug)
	comment_list=Comment.objects.filter(post=single_blog).order_by("-created_on")
	comment_count=Comment.objects.filter(post=single_blog).count()
	like_count=single_blog.liked_by.count()

	liked_by_me=False
	if request.user in single_blog.liked_by.all():
		liked_by_me=True
	if request.method=='POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			obj= form.save(commit=False)
			obj.user=request.user	
			obj.post=single_blog			
			obj.save()
			# return redirect('single_blog', blogslug=blogslug)
			return JsonResponse({'comment':model_to_dict(obj)},status=200)
	else:
		form=CommentForm()
	
	

	context={
	'single_blog': single_blog,
	'comment_list': comment_list,
	'comment_form':form,
	'comment_count':comment_count,
	'like_count':like_count,
	'liked_by_me':liked_by_me,

	}
	
	return render(request,'single-blog.html', context)

def like_blog(request,blogslug):
	single_blog=BlogPost.objects.get(slug=blogslug)
	single_blog.liked_by.add(request.user)
	return redirect('single_blog', blogslug=blogslug)

def unlike_blog(request,blogslug):
	single_blog=BlogPost.objects.get(slug=blogslug)
	single_blog.liked_by.remove(request.user)
	return redirect('single_blog', blogslug=blogslug)




