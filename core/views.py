from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *


@login_required(login_url='userauths:sign-in')
def index(request):

    current_user = request.user
    user_tasks = Task.objects.filter(assignee=current_user)
    team_tasks = Task.objects.filter(assignee_team__members=current_user)

    if current_user.is_superuser:
        all_tasks = Task.objects.all()
    else:
        all_tasks = user_tasks | team_tasks

    new_task = all_tasks.filter(category='New')
    progress_task = all_tasks.filter(category='Progress')
    hold_task = all_tasks.filter(category='Hold')
    pending_task = all_tasks.filter(category='Pending')

    for task in all_tasks:
        print(task.title)
    print("User object:", request.user)

    context = {
        'tasks': all_tasks,
        'new_task': new_task,
        'progress_task': progress_task,
        'hold_task': hold_task,
        'pending_task': pending_task,
    }

    return render(request, 'home.html', context)


# def task_view(request, task_id):
#     current_user = request.user
#     current_task = Task.objects.get(id=task_id)
#     error_text = ''
#     comment = None

#     if request.method == 'POST':
#         text = request.POST.get('comment')
#         if text == '':
#             print('Please enter any comment!')
#             error_text = 'Please enter something'
#         else:
#             comment = Comment.objects.create(
#                 user=current_user,
#                 text=text,
#                 task=current_task,
#             )
#             comment.save()  # Move the save() call here

#             return redirect('core:task', task_id=task_id)

#     task = get_object_or_404(Task, pk=task_id)
#     comments = task.comments.all()

#     labels = Label.objects.all()
#     teams = Team.objects.all()
#     categories = Task.CATEGORY_CHOICES
#     all_users = User.objects.all()
#     users = User.objects.filter(is_staff=True)

#     context = {
#         'task': current_task, 
#         'user': current_user,
#         'comments': comments,
#         'error_text': error_text,
#         'labels': labels,
#         'teams': teams,
#         'categories': categories,
#         'all_users': all_users,
#         'users': users,
        
#     }

#     return render(request, 'task.html', context)


def create_task(request):
    labels = Label.objects.all()
    teams = Team.objects.all()
    categories = Task.CATEGORY_CHOICES
    all_users = User.objects.all()
    users = User.objects.filter(is_staff=True)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        get_labels = request.POST.getlist('labels')
        get_category = request.POST.get('category')
        assignee_id = request.POST.get('assignee_id')
        assignee_team_id = request.POST.get('assignee_team_id')
        created_by_id = request.POST.get('created_by_id')

        # Validate the data if necessary

        # Create the task object
        task = Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            category=get_category,
            created_by_id=created_by_id
        )

        # Assign assignee if provided
        if assignee_id:
            task.assignee_id = assignee_id

        # Assign assignee team if provided
        if assignee_team_id:
            task.assignee_team_id = assignee_team_id

        # Assign labels if provided
        if get_labels:
            task.labels.add(*get_labels)

        # Save the task
        task.save()

        # Redirect to a success page or any other appropriate action
        return redirect('core:index')



    context = {
        'labels': labels,
        'teams': teams,
        'categories': categories,
        'users': users,
        'all_users': all_users,
    }
    return render(request, 'create_task.html', context)












from django.db import IntegrityError

def task_view(request, task_id):
    current_user = request.user
    current_task = get_object_or_404(Task, pk=task_id)
    error_text = ''
    comment = None

    if request.method == 'POST':
        if 'edit_task' in request.POST:
            # If the form is for editing the task
            title = request.POST.get('title')
            description = request.POST.get('description')
            due_date = request.POST.get('due_date')
            priority = request.POST.get('priority')
            get_labels = request.POST.getlist('labels')
            get_category = request.POST.get('category')
            assignee_id = request.POST.get('assignee_id')
            assignee_team_id = request.POST.get('assignee_team_id')
            created_by_id = request.POST.get('created_by_id')

            # Update the task object
            current_task.title = title
            current_task.description = description
            current_task.due_date = due_date
            current_task.priority = priority
            current_task.category = get_category
            current_task.created_by_id = created_by_id

            # Assign assignee if provided
            if assignee_id:
                current_task.assignee_id = assignee_id
            else:
                current_task.assignee = None

            # Assign assignee team if provided
            if assignee_team_id:
                current_task.assignee_team_id = assignee_team_id
            else:
                current_task.assignee_team = None

            # Clear existing labels and assign new ones if provided
            current_task.labels.clear()
            if get_labels:
                current_task.labels.add(*get_labels)

            # Save the task
            current_task.save()

            return redirect('core:task', task_id=task_id)
        else:
            # If the form is for adding a comment
            text = request.POST.get('comment')
            if text == '':
                error_text = 'Please enter something for the comment'
            else:
                try:
                    comment = Comment.objects.create(
                        user=current_user,
                        text=text,
                        task=current_task,
                    )
                    # Save the comment
                    comment.save()
                except IntegrityError:
                    error_text = 'An error occurred while saving the comment.'

                return redirect('core:task', task_id=task_id)

    comments = current_task.comments.all()

    labels = Label.objects.all()
    teams = Team.objects.all()
    categories = Task.CATEGORY_CHOICES
    all_users = User.objects.all()
    users = User.objects.filter(is_staff=True)

    context = {
        'task': current_task, 
        'user': current_user,
        'comments': comments,
        'error_text': error_text,
        'labels': labels,
        'teams': teams,
        'categories': categories,
        'all_users': all_users,
        'users': users
    }

    return render(request, 'task.html', context)



# def edit_task(request, task_id):
#     task = get_object_or_404(Task, pk=task_id)
#     labels = Label.objects.all()
#     teams = Team.objects.all()
#     categories = Task.CATEGORY_CHOICES
#     all_users = User.objects.all()
#     users = User.objects.filter(is_staff=True)

#     if request.method == 'POST':
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#         due_date = request.POST.get('due_date')
#         priority = request.POST.get('priority')
#         get_labels = request.POST.getlist('labels')
#         get_category = request.POST.get('category')
#         assignee_id = request.POST.get('assignee_id')
#         assignee_team_id = request.POST.get('assignee_team_id')
#         created_by_id = request.POST.get('created_by_id')

#         # Update the task object
#         task.title = title
#         task.description = description
#         task.due_date = due_date
#         task.priority = priority
#         task.category = get_category
#         task.created_by_id = created_by_id

#         # Assign assignee if provided
#         if assignee_id:
#             task.assignee_id = assignee_id
#         else:
#             task.assignee = None

#         # Assign assignee team if provided
#         if assignee_team_id:
#             task.assignee_team_id = assignee_team_id
#         else:
#             task.assignee_team = None

#         # Clear existing labels and assign new ones if provided
#         task.labels.clear()
#         if get_labels:
#             task.labels.add(*get_labels)

#         # Save the task
#         task.save()

#         # Redirect to a success page or any other appropriate action
#         return redirect('core:index')

#     context = {
#         'task': task,
#         'labels': labels,
#         'teams': teams,
#         'categories': categories,
#         'users': users,
#         'all_users': all_users,
#     }
#     return redirect('core:task', context, task_id=task_id)

# def comment_task(request, task_id):

#     task = get_object_or_404(Task, pk=task_id)
#     comments = task.comments.all()
#     return render(request, )
   

# def task_view(request, task_id):
#     current_user = request.user
#     current_task = Task.objects.get(id=task_id)

#     if request.method == 'POST':
#         text = request.POST.get('comment')

#         comment = Comment.objects.create(
#             user=current_user,
#             text=text,
#             task=current_task,
#             )
#         comment.save()

#         return redirect('core:task', task_id=task_id)

#     task = get_object_or_404(Task, pk=task_id)
#     comments = task.comments.all()

#     context = {
#         'task': current_task, 
#         'user': current_user,
#         'comments': comments,
#     }

#     return render(request, 'task.html', context)
