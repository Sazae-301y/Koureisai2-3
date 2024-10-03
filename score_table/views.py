from django.shortcuts import render,redirect
from .forms import PostForm
from .models import Post,Participant,FujitaRanking
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.

def frontpage(request):
    posts = Post.objects.all().order_by('-posted_date')
    participants = Participant.objects.all().order_by('-score')
    first_place = participants[0] if len(participants) > 0 else None
    second_place = participants[1] if len(participants) > 1 else None
    third_place = participants[2] if len(participants) > 2 else None

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # commit=Falseで一度保存を保留し、slugを生成
            post.save()  # save()メソッドが呼び出され、slugが自動生成される
            return redirect('frontpage')  # 投稿後にリダイレクト
    else:
        form = PostForm()

    version = request.GET.get('version', 'KodairaTemplate')
    if version == 'KodairaTemplate':
        template = 'page/Kodaira_template.html'
    else:
        template = 'page/Fujita_template.html'


    return render(request,"page/frontpage.html", {"form": form,"posts": posts,'participants':participants,"template":template,"first_place":first_place,"second_place":second_place,"third_place":third_place})

def score_table(request):
    participants = Participant.objects.all().order_by('-score')
    return render(request,"page/score_table.html", {'participants':participants})


def index(request):
    return render(request, 'page/Fujita_template.html')

def post_detail(request,slug):
    post = Post.objects.get(slug=slug)
    return render(request,"page/post_detail.html",{"post": post})

@csrf_exempt
def save_ranking(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        participant = data.get('participant')
        score = data.get('score')
        
        if participant and score is not None:
            ranking = FujitaRanking(participant=participant, score=score)
            ranking.save()
            return JsonResponse({'status': 'success'}, status=201)
        else:
            return JsonResponse({'status': 'error', 'message': '無効なデータです'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': '無効なリクエストメソッドです'}, status=405)