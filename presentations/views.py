from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Group, Presentation
from .forms import LoginForm, GroupForm, PresentationForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.username}!")
            return redirect('dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'presentations/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из системы")
    return redirect('login')

@login_required
def dashboard(request):
    groups = Group.objects.filter(teacher=request.user)
    return render(request, 'presentations/dashboard.html', {'groups': groups})

@login_required
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.teacher = request.user
            group.save()
            messages.success(request, f"Группа '{group.name}' создана!")
            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupForm()
    
    return render(request, 'presentations/group_form.html', {
        'form': form, 
        'title': 'Создать группу'
    })

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id, teacher=request.user)
    presentations = group.presentations.all()
    
    if request.method == 'POST':
        form = PresentationForm(request.POST, request.FILES)
        if form.is_valid():
            presentation = form.save(commit=False)
            presentation.group = group
            presentation.save()
            messages.success(request, f"Презентация '{presentation.title}' загружена!")
            return redirect('group_detail', group_id=group.id)
    else:
        form = PresentationForm()
    
    return render(request, 'presentations/group_detail.html', {
        'group': group,
        'presentations': presentations,
        'form': form
    })

@login_required
def group_edit(request, group_id):
    group = get_object_or_404(Group, id=group_id, teacher=request.user)
    
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, f"Группа '{group.name}' обновлена!")
            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupForm(instance=group)
    
    return render(request, 'presentations/group_form.html', {
        'form': form, 
        'title': 'Редактировать группу'
    })

@login_required
def group_delete(request, group_id):
    group = get_object_or_404(Group, id=group_id, teacher=request.user)
    
    if request.method == 'POST':
        group.delete()
        messages.success(request, f"Группа '{group.name}' удалена!")
        return redirect('dashboard')
    
    return render(request, 'presentations/group_confirm_delete.html', {
        'group': group,
        'type': 'group'
    })

@login_required
def presentation_delete(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id, group__teacher=request.user)
    group_id = presentation.group.id
    
    if request.method == 'POST':
        presentation.delete()
        messages.success(request, f"Презентация '{presentation.title}' удалена!")
        return redirect('group_detail', group_id=group_id)
    
    return render(request, 'presentations/group_confirm_delete.html', {
        'object': presentation,
        'type': 'presentation'
    })