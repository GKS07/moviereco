from django.shortcuts import render,redirect
from .models import users 
from .movie_recomendation import *
from datetime import date
from dateutil import parser
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.core.mail import send_mail
from django.db import IntegrityError
import random
import socket
import re

# Create your views here.
def signup(request):
    return render(request,'signup.html')

def signin(request):
    return render(request,'login.html')


def home(request):

    action = top_movie_based_on_genre('Action').head(8)
    action_title = action.title
    action_title1 = []
    for act_mov in action_title:
        action_title1.append(act_mov)
    action_year = action.year
    action_year1 = []
    for act_yea in action_year:
        action_year1.append(act_yea)
    action_poster = action.poster_path
    urls = []
    for i in action_poster:
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i)
        for j in url:
            k = j.replace("'", "")
            urls.append(k)

    action_id = action.movieId
    action_id1 = []
    for i in action_id:
        action_id1.append(i)       

    
    romance = top_movie_based_on_genre('Romance').head(8)
    romance_title = romance.title
    romance_title1 = []
    for rom_mov in romance_title:
        romance_title1.append(rom_mov)
    romance_year = romance.year
    romance_year1 = []
    for rom_yea in romance_year:
        romance_year1.append(rom_yea)
    romance_poster = romance.poster_path
    romance_urls = []
    for i in romance_poster:
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i)
        for j in url:
            k = j.replace("'", "")
            romance_urls.append(k)
    romance_id = romance.movieId
    romance_id1 = []
    for i in romance_id:
        romance_id1.append(i)        

    comedy = top_movie_based_on_genre('Comedy').head(8)
    comedy_title = comedy.title
    comedy_title1 = []
    for com_mov in comedy_title:
        comedy_title1.append(com_mov)
    comedy_year = comedy.year
    comedy_year1 = []
    for com_yea in comedy_year:
        comedy_year1.append(com_yea)
    comedy_poster = comedy.poster_path
    comedy_urls = []
    for i in comedy_poster:
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i)
        for j in url:
            k = j.replace("'", "")
            comedy_urls.append(k)

    comedy_id = comedy.movieId
    comedy_id1 = []
    for i in comedy_id:
        comedy_id1.append(i)        

    drama = top_movie_based_on_genre('Drama').head(8)
    drama_title = drama.title
    drama_title1 = []
    for dr_mov in drama_title:
        drama_title1.append(dr_mov)
    drama_year = drama.year
    drama_year1 = []
    for dr_yea in drama_year:
        drama_year1.append(dr_yea)
    drama_poster = drama.poster_path
    drama_urls = []
    for i in drama_poster:
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i)
        for j in url:
            k = j.replace("'", "")
            drama_urls.append(k)

    drama_id = drama.movieId
    drama_id1 = []
    for i in drama_id:
        drama_id1.append(i)        

    return render(request,'home.html', {"action_title": action_title1, "action_year": action_year1, "action_url": urls,"action_id": action_id1, "romance_title": romance_title1, "romance_year": romance_year1, "romance_url": romance_urls, "romance_id": romance_id1, "comedy_title": comedy_title1, "comedy_year": comedy_year1, "comedy_url": comedy_urls, "comedy_id": comedy_id1,  "drama_title": drama_title1, "drama_year": drama_year1, "drama_url": drama_urls, "drama_id": drama_id1}) 

def product(request):
    return render(request,'product.html') 

def fgtpwdgo(request):
    return render(request,'fgtpwd.html') 


def add(request):
    uname = request.POST['uname']
    pwd = request.POST['pwd']
    fname = request.POST['fname']
    lname = request.POST['lname']
    mob = request.POST['mob']
    email = request.POST['email']
    dob = parser.parse(request.POST['dob']).date()
    if 'romantic' in request.POST:
        romantic = request.POST['romantic']
    else:
        romantic = False
    if 'act' in request.POST:
        act = request.POST['act']
    else:
        act = False
    if 'comedy' in request.POST:
        comedy = request.POST['comedy']
    else:
        comedy = False
    if 'animation' in request.POST:
        animation = request.POST['animation']
    else:
        animation = False
    if 'horror' in request.POST:
        horror = request.POST['horror']
    else:
        horror = False

    days_in_year = 365.2425    
    age = int((date.today() - dob).days / days_in_year)
    otp = random.randint(100000,999999)

    u = users(uname = uname,pwd=pwd,fname=fname,lname=lname,mob=mob,email=email,
    dob=dob,age=age,otp=otp,romantic=romantic,action=act,comedy=comedy,animation=animation,
    horror=horror)
    try:
        u.save()
    except IntegrityError:
        messages.error(request,"This e-mail is already registered, try another email to Signup")
        return redirect('signup')

    try:
        send_mail('Email verification', 'your email verification OTP is '+ str(otp), 'hypemoveis2020@gmail.com', [email])
    except socket.gaierror:
        print('email not sent')

    record = users.objects.filter(uname = uname,pwd=pwd,otp=otp)
    for r in record:
        request.session['id'] = r.uid
    return render(request,'verification.html')

def check(request):
    uname = request.POST['uname']
    pwd = request.POST['pwd']
    recs = users.objects.filter(uname = uname,pwd = pwd)
    if recs: 
        for a in recs:
            request.session['uname']=uname
            request.session['uid'] = a.uid
        return redirect('home')
    else:
        rec = users.objects.filter(email = uname,pwd = pwd)
        if rec:
            for b in rec:
                request.session['uname']=b.uname
                request.session['uid'] = b.uid
            return redirect('home')
        else:
            messages.error(request,'login failed, wrong credentials!')
            return redirect('signin')
        
def verify(request):
    otp = int(request.POST['otp'])
    if request.session.has_key('id'):
        uid = request.session.get('id')
        rec = users.objects.filter(uid = uid)
    elif request.session.has_key('mail'):
        email = request.session.get('mail')
        rec = users.objects.filter(email = email)
    if rec:
        for a in rec:
            if a.otp == otp:
                if request.session.has_key('id'):
                    del request.session['id']
                    return render(request,'login.html')
                elif request.session.has_key('mail'):
                    return render(request,'changepwd.html')

            else:
                if request.session.has_key('id'):
                    del request.session['id']
                    rec.delete()
                    return render(request,'signup.html')
                elif request.session.has_key('mail'):
                    del request.session['mail']
                    messages.error(request,'wrong OTP')
                    return redirect('verify')
        
def profile(request):
    if request.session.has_key('uid'):
        uid = request.session.get('uid')
        rec = users.objects.get(uid = uid)
        return render(request,'profile.html',{'data':rec})
    else:
        return HttpResponse('invalid')

def logout(request):
    if request.session.has_key('uid'):
        del request.session['uid']
    if request.session.has_key('uname'):
        del request.session['uname']
    return render(request,'login.html')

def editprofile(request):
    if request.session.has_key('uid'):
        uid = request.session.get('uid')
        rec = users.objects.get(uid = uid)
        return render(request,'editprofile.html',{'data':rec})
    else:
        messages.error(request,'invalid')
        return redirect('profile')

def saveprofile(request):
    if request.session.has_key('uid'):
        uid = request.session.get('uid')
        rec = users.objects.get(uid = uid)
        umail = rec.email
        rec.pwd = request.POST['pwd']
        rec.fname = request.POST['fname']
        rec.lname = request.POST['lname']
        rec.mob = request.POST['mob']
        rec.email = request.POST['email']
        rec.dob = parser.parse(request.POST['dob']).date()
        if 'romantic' in request.POST:
            rec.romantic = request.POST['romantic']
        else:
            rec.romantic = False
        if 'act' in request.POST:
            rec.act = request.POST['act']
        else:
            rec.act = False
        if 'comedy' in request.POST:
            rec.comedy = request.POST['comedy']
        else:
            rec.comedy = False
        if 'animation' in request.POST:
            rec.animation = request.POST['animation']
        else:
            rec.animation = False
        if 'horror' in request.POST:
            rec.horror = request.POST['horror']
        else:
            rec.horror = False

        days_in_year = 365.2425    
        rec.age = int((date.today() - rec.dob).days / days_in_year)
        if request.POST['email'] != umail:
            rec.otp = random.randint(100000,999999)
            rec.save()
            try:
                send_mail('Email verification', 'your email verification OTP is '+ str(rec.otp), 'hypemoveis2020@gmail.com', [email])
            except socket.gaierror:
                print('email not sent')
            record = users.objects.get(uid = uid)
            for r in record:
                request.session['id'] = r.uid
            return render(request,'verification.html')
        else:
            rec.save()
            record = users.objects.get(uid = uid)
            return render(request,'profile.html',{'data':record})

def resend(request):
    if request.session.has_key('id'):
        rec = users.objects.get(uid = id)
        email = rec.email
        rec.otp = random.randint(100000,999999)
        rec.save()
        try:
            send_mail('Email verification', 'your email verification OTP is '+ str(rec.otp), 'hypemoveis2020@gmail.com', [email])
        except socket.gaierror:
            print('email not sent')
        return render(request,'verification.html')
    else:
        messages.error(request,'OTP already sent')
        return redirect('verify')

def fgtpwd(request):
    email = request.POST['email']
    fname = request.POST['fname']
    lname = request.POST['lname']
    request.session['mail'] = email
    rec = users.objects.get(email = email, fname=fname,lname=lname)
    if rec:
        rec.otp = random.randint(100000,999999)
        rec.save()
        try:
            send_mail('Email verification', 'your email verification OTP is '+ str(rec.otp), 'hypemoveis2020@gmail.com', [email])
        except socket.gaierror:
            print('email not sent')
        return render(request,'verification.html')
    else:
        messages.error(request,'invalid')
        return redirect('signin')

def changepwd(request):
    if request.session.has_key('mail'):
        email = request.session['mail']
        pwd = request.POST['pwd']
        rec = users.objects.get(email = email)
        rec.pwd = pwd
        rec.save()
        del request.session['mail']
        return render(request,'login.html')
    else:
        messages.error(request,'invalid')
        return redirect('changepwd')


def watch(request):
    if request.session.has_key('uid'):

        #print(our_qualified_movies['movieId'])
        id1 = request.GET.get('movieid')
        #print(id1)
        movie_data = parent_movies.loc[parent_movies['movieId'] == id1]
        print(movie_data)
        title = movie_data.title.iloc[0]
        print(title)
        year = movie_data.year.iloc[0]
        print(year)

        genre = movie_data.genres.iloc[0]
        genre1 = ""
        for i in genre:
            genre1 = genre1 +"|"+i

        urls = []
        for i in movie_data.poster_path:#.iloc[0]:
            url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i)
            for j in url:
                k = j.replace("'", "")
                urls.append(k)     
        
        print(urls)
        url1 = urls[0]

        return render(request, 'watch.html', {"title": title, "year": year, "url": url1, "genre":genre1})
    else:
        return redirect('signin')


def actionmovies(request):

    action = top_movie_based_on_genre('Action').head(40)
    action_title = action.title
    action_title1 = []
    for act_mov in action_title:
        action_title1.append(act_mov)
    action_year = action.year
    action_year1 = []
    for act_yea in action_year:
        action_year1.append(act_yea)
    action_poster = action.poster_path
    urls = []
    for i in action_poster:
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i)
        for j in url:
            k = j.replace("'", "")
            urls.append(k)

    action_id = action.movieId
    action_id1 = []
    for i in action_id:
        action_id1.append(i)        
    return render(request, 'Action_movies.html', {"title": action_title1, "year": action_year1, "url": urls, "action_id": action_id1})


def romantic(request):

    romance = top_movie_based_on_genre('Romance').head(40)
    romance_title = romance.title
    romance_title1 = []
    for rom_mov in romance_title:
        romance_title1.append(rom_mov)
    romance_year = romance.year
    romance_year1 = []
    for rom_yea in romance_year:
        romance_year1.append(rom_yea)
    romance_poster = romance.poster_path
    romance_urls = []
    for i in romance_poster:
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i)
        for j in url:
            k = j.replace("'", "")
            romance_urls.append(k)
    
    romance_id = romance.movieId
    romance_id1 = []
    for i in romance_id:
        romance_id1.append(i)

    return render(request, 'romantic.html', {"title": romance_title1, "year": romance_year1, "url": romance_urls, "romance_id": romance_id1})

def comedy(request):

    comedy = top_movie_based_on_genre('Comedy').head(40)
    comedy_title = comedy.title
    comedy_title1 = []
    for com_mov in comedy_title:
        comedy_title1.append(com_mov)
    comedy_year = comedy.year
    comedy_year1 = []
    for com_yea in comedy_year:
        comedy_year1.append(com_yea)
    comedy_poster = comedy.poster_path
    comedy_urls = []
    for i in comedy_poster:
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i)
        for j in url:
            k = j.replace("'", "")
            comedy_urls.append(k)
    
    comedy_id = comedy.movieId
    comedy_id1 = []
    for i in comedy_id:
        comedy_id1.append(i)

    return render(request, 'comedy.html', {"title": comedy_title1, "year": comedy_year1, "url": comedy_urls, "comedy_id": comedy_id1})

def drama(request):

    drama = top_movie_based_on_genre('Drama').head(40)
    drama_title = drama.title
    drama_title1 = []
    for dr_mov in drama_title:
        drama_title1.append(dr_mov)
    drama_year = drama.year
    drama_year1 = []
    for dr_yea in drama_year:
        drama_year1.append(dr_yea)
    drama_poster = drama.poster_path
    drama_urls = []
    for i in drama_poster:
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i)
        for j in url:
            k = j.replace("'", "")
            drama_urls.append(k) 
    drama_id = drama.movieId
    drama_id1 = []
    for i in drama_id:
        drama_id1.append(i)

    return render(request, 'drama.html', {"title": drama_title1, "year": drama_year1, "url": drama_urls, "drama_id": drama_id1})

def watch_1(request):
    try:

        
        if request.session.has_key('uid'):
            id2 = request.session['uid']
            search_movie = request.GET.get('movieid')
            print(id2)
            print(search_movie)

            movie_data = parent_movies.loc[parent_movies['title'] == search_movie]
            #print(movie_data)

            title = movie_data.title.iloc[0]
            #print(title)
            year = movie_data.year.iloc[0]
            #print(year)
            genre = movie_data.genres.iloc[0]
            genre1 = ""
            for i in genre:
                genre1 = genre1 +"|"+i
              
            urls = []
            for i in movie_data.poster_path:#.iloc[0]:
                url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i)
                for j in url:
                    k = j.replace("'", "")
                    urls.append(k)     
                
            #print(urls[0])
            url1 = urls[0]

            recomender = hybrid_recommender(id2, search_movie)
            
            recomender_title = recomender.title
            recomender_title1 = []
            for dr_mov in recomender_title:
                recomender_title1.append(dr_mov)
            recomender_year = recomender.year
            recomender_year1 = []
            for dr_yea in recomender_year:
                recomender_year1.append(dr_yea)
            recomender_poster = recomender.poster_path
            recomender_urls = []
            for i in recomender_poster:
                url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i)
                for j in url:
                    k = j.replace("'", "")
                    recomender_urls.append(k)
            #recomender_urls1 = recomender_urls[0]
            #print(recomender_urls1)         
            recomender_id = recomender.movieId
            recomender_id1 = []
            for i in recomender_id:
                recomender_id1.append(i)

            #    #print(recomender)

            return render(request, 'watch_1.html', {"recomender_title": recomender_title1, "recomender_year": recomender_year1, "recomender_url": recomender_urls, "recomender_id": recomender_id1 , "title": title, "year": year, "url": url1, "genre": genre1})

        else:
            return redirect('signin')

    except:
        messages.error(request, 'Oops! something went wrong' )
        return redirect('home')

        

def searchmovies(request):

    #search_movie = request.POST.get('search_movies')
    #search_movie = search_movie.title()
    #search_movie = search_movie.lower()
    #print(search_movie)

    #dc = parent_movies['title'].values.tolist()
    #dc = dc.lower()
    #print(dc)
    #movie_data = parent_movies.loc[parent_movies['title'] == search_movie]
    #print(movie_data)

    try:

        if request.session.has_key('uid'):

            search_movie = request.POST.get('search_movies')
            search_movie = search_movie.title()
            #search_movie = search_movie.lower()
            print(search_movie)

            #dc = parent_movies['title'].values.tolist()
            #dc = dc.lower()
            #print(dc)
            movie_data = parent_movies.loc[parent_movies['title'] == search_movie]
            print(movie_data)

            title = movie_data.title.iloc[0]
            print(title)
            year = movie_data.year.iloc[0]
            print(year)
            genre = movie_data.genres.iloc[0]
            genre1 = ""
            for i in genre:
                genre1 = genre1 +"|"+i
          
            urls = []
            for i in movie_data.poster_path:#.iloc[0]:
                url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i)
                for j in url:
                    k = j.replace("'", "")
                    urls.append(k)     
            
            print(urls[0])
            url1 = urls[0]

            

            recomender = improved_content_based_recommender(search_movie)
        
            recomender_title = recomender.title
            recomender_title1 = []
            for dr_mov in recomender_title:
                recomender_title1.append(dr_mov)
            recomender_year = recomender.year
            recomender_year1 = []
            for dr_yea in recomender_year:
                recomender_year1.append(dr_yea)
            recomender_poster = recomender.poster_path
            recomender_urls = []
            for i in recomender_poster:
                url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i)
                for j in url:
                    k = j.replace("'", "")
                    recomender_urls.append(k)
            recomender_urls1 = recomender_urls[0]
            print(recomender_urls1)         
            recomender_id = recomender.movieId
            recomender_id1 = []
            for i in recomender_id:
                recomender_id1.append(i)

            #print(recomender)

            return render(request, 'search_movies.html', {"recomender_title": recomender_title1, "recomender_year": recomender_year1, "recomender_url": recomender_urls, "recomender_id": recomender_id1 , "title": title, "year": year, "url": url1, "genre": genre1})

        else:
            return redirect('signin')

    except:
        messages.error(request, 'This movie is not available in our database' )
        return redirect('home')

    





        
