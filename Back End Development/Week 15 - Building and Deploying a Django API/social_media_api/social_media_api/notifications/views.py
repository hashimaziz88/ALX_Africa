from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications_list(request):
    notifications = request.user.notifications.filter(read=False)
    return render(request, 'notifications/list.html', {'notifications': notifications})

@login_required
def mark_as_read(request, pk):
    notification = Notification.objects.get(id=pk)
    notification.read = True
    notification.save()
    return JsonResponse({'message': 'Notification marked as read.'})
