import random
import string
from django.shortcuts import get_object_or_404,render,redirect
from .forms import PostForm
from django.http import JsonResponse
from .models import Post,Participant,FujitaRanking,Reservation
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required

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

def get_ranking_data(request):
    rankings = FujitaRanking.objects.all().values('name', 'score','date')  # 'name'と'score'はモデルのフィールド名に置き換えてください
    return JsonResponse(list(rankings), safe=False)

def post_detail(request,slug):
    post = Post.objects.get(slug=slug)
    return render(request,"page/post_detail.html",{"post": post})

# 予約番号をランダムに生成する関数
def generate_reservation_number():
    return ''.join(random.choices(string.digits, k=3))

def reservation_confirmation(request):
    reservation_number = request.session.get('reservation_number', None)
    
    if reservation_number:
        # セッションから予約番号で予約を取得
        try:
            reservation = Reservation.objects.get(reservation_number=reservation_number)
        except Reservation.DoesNotExist:
            reservation = None
        
        if reservation and not reservation.is_checked_in:
            # 予約が受付済みではない場合、現在の予約状況を表示
            ahead_of_you = Reservation.objects.filter(
                created_at__lt=reservation.created_at,
                is_checked_in=False
            ).count()
            
            return render(request, 'page/reservation_confirmation.html', {
                'reservation': reservation,
                'ahead_of_you': ahead_of_you
            })
        else:
            # 予約が「受付済み」なら再予約を許可するため、セッションをクリア
            request.session.pop('reservation_number', None)
    
    # 新規予約の場合の処理
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        reservation_number = generate_reservation_number()
        reservation = Reservation.objects.create(nickname=nickname, reservation_number=reservation_number)
        
        # 新しい予約番号をセッションに保存
        request.session['reservation_number'] = reservation_number
        return redirect('reservation_confirmation')

    return render(request, 'page/reservation_form.html')

def delete_reservation(request, reservation_number):

    reservation = get_object_or_404(Reservation, reservation_number=reservation_number)
    reservation.delete()
    return redirect('reservation_confirmation')



@staff_member_required
def reservation_management(request):
    if request.method == 'POST':
        reservation_number = request.POST.get('reservation_number')
        action = request.POST.get('action')
        if action == 'accept':
            try:
                reservation = Reservation.objects.get(reservation_number=reservation_number)
                reservation.is_checked_in = True
                reservation.save()
            except Reservation.DoesNotExist:
                pass
        elif action == 'notaccept':
            try:
                reservation = Reservation.objects.get(reservation_number=reservation_number)
                reservation.is_checked_in = False
                reservation.save()
            except Reservation.DoesNotExist:
                pass
        elif action == 'delete':
            reservation = get_object_or_404(Reservation, reservation_number=reservation_number)
            reservation.delete()
        elif action == 'notthere':
            try:
                reservation = Reservation.objects.get(reservation_number=reservation_number)
                reservation.is_not_there = True
                reservation.save()
            except Reservation.DoesNotExist:
                pass
        elif action == 'there':
            try:
                reservation = Reservation.objects.get(reservation_number=reservation_number)
                reservation.is_not_there = False
                reservation.save()
            except Reservation.DoesNotExist:
                pass
            

        # 処理が終わったらリダイレクト（PRGパターン）
        return redirect('reservation_management')

    # GETリクエスト時に表示するデータ
    reserved_reservations = Reservation.objects.filter(is_checked_in=False).order_by('created_at')
    checked_in_reservations = Reservation.objects.filter(is_checked_in=True).order_by('created_at')
    now = timezone.now()
    
    return render(request, 'page/reservation_management.html', {
        'reserved_reservations': reserved_reservations,
        'checked_in_reservations': checked_in_reservations,
        'now': now
    })