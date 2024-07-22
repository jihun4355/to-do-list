# posts/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from datetime import datetime, timedelta
from .models import Post
from django.utils import timezone
from django.http import JsonResponse

# 유효한 todo를 불러온다.
def post_list(request):
    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)

    posts = Post.objects.filter(due_date__gte=today).order_by('id')

    for post in posts:
        if post.due_date == today:
            post.due_date_display = '오늘'
        elif post.due_date == tomorrow:
            post.due_date_display = '내일'
        else:
            post.due_date_display = post.due_date.strftime('%Y-%m-%d')
    
    return render(request, 'posts/post_list.html', {'posts': posts})

# todo 중 priority가 True인 것만 불러온다.
def important_view(request):
    today = datetime.today().date()

    posts = Post.objects.filter(priority=True, is_completed=False, due_date__gte=today).order_by('id')

    for post in posts:
        if post.due_date == today:
            post.due_date_display = '오늘'
        elif post.due_date == today + timedelta(days=1):
            post.due_date_display = '내일'
        else:
            post.due_date_display = post.due_date.strftime('%Y-%m-%d')
            
    return render(request, 'posts/important.html', {'posts': posts})

# todo를 추가한다.
def add_todo(request):
    if request.method == "POST":
        content = request.POST.get('content')
        due_date = request.POST.get('due_date')
        is_completed = request.POST.get('is_completed') == 'on'
        priority = request.POST.get('priority') == 'on'

        if due_date:
            due_date = timezone.datetime.strptime(due_date, '%Y-%m-%d')
        else:
            due_date = timezone.now().date()

        post = Post.objects.create(content=content, due_date=due_date, is_completed=is_completed, priority=priority)
        
        print(f"Content: {post.content}")
        print(f"Due Date: {post.due_date}")
        print(f"Is Completed: {post.is_completed}")
        print(f"Priority: {post.priority}")

        return redirect('post_list')
    
    return render(request, 'posts/add_todo.html')

# priority가 True인 todo를 추가한다.
def important_add_todo(request):
    if request.method == "POST":
        content = request.POST.get('content')
        due_date = request.POST.get('due_date')
        is_completed = request.POST.get('is_completed') == 'on'
        priority = True

        if due_date:
            due_date = timezone.datetime.strptime(due_date, '%Y-%m-%d')
        else:
            due_date = timezone.now().date()

        post = Post.objects.create(content=content, due_date=due_date, is_completed=is_completed, priority=priority)
        
        print(f"Content: {post.content}")
        print(f"Due Date: {post.due_date}")
        print(f"Is Completed: {post.is_completed}")
        print(f"Priority: {post.priority}")

        return redirect('important')
    
    return render(request, 'posts/important_add_todo.html')

# priority의 상태를 업데이트한다.
def priority_update(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        post.priority = not post.priority
        post.save()
        return JsonResponse({'priority': post.priority})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# is_completed의 상태를 업데이트한다.
def completed_update(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        post.is_completed = not post.is_completed
        post.save()
        return JsonResponse({'is_completed': post.is_completed})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# 선택한 todo의 상세 정보를 불러온다.
def post_details(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        data = {
            'id': post_id,
            'content': post.content,
            'due_date': post.due_date,
            'is_completed': post.is_completed,
            'priority': post.priority,
        }
        return JsonResponse(data)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

# 선택한 todo를 삭제한다.
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return JsonResponse({'status': 'success', 'message': 'Post deleted successfully'}, status=200)

# todo의 content와 due_date를 업데이트한다.
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    content = request.POST.get('content')
    due_date = request.POST.get('due_date')

    if content:
        post.content = content
    if due_date:
        post.due_date = due_date

    post.save()
    return JsonResponse({'status': 'success'})

# todo를 검색한다.
def search(request, query=None):
    today = datetime.today().date()
    
    if query:
        posts = Post.objects.filter(content__icontains=query, due_date__gte=today)
    else:
        posts = Post.objects.filter(due_date__gte=today)
    
    incomplete_posts = posts.filter(is_completed=False)
    completed_posts = posts.filter(is_completed=True)

    posts_data = {
        'incomplete_posts': list(incomplete_posts.values('id', 'content', 'due_date', 'priority', 'is_completed')),
        'completed_posts': list(completed_posts.values('id', 'content', 'due_date', 'priority', 'is_completed'))
    }

    return JsonResponse(posts_data)

# priority가 True인 todo 중에서 검색한다.
def important_search(request, query=None):
    today = datetime.today().date()
    
    posts = Post.objects.filter(priority=True, due_date__gte=today)
    
    if query:
        posts = posts.filter(content__icontains=query)
    
    incomplete_posts = posts.filter(is_completed=False)
    completed_posts = posts.filter(is_completed=True)

    posts_data = {
        'incomplete_posts': list(incomplete_posts.values('id', 'content', 'due_date', 'priority', 'is_completed')),
        'completed_posts': list(completed_posts.values('id', 'content', 'due_date', 'priority', 'is_completed'))
    }

    return JsonResponse(posts_data)
