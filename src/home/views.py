from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from accounts.models import Registration, YearEnding
from home.backup import BackupDatabase


@login_required(login_url='/account/login/')
def HomePage(request):
	if not request.user.is_authenticated():
		raise Http404
	try:
		current_session_id = request.session['session']
	except:
		currentSession = YearEnding.objects.order_by("-id").first()
		request.session['session'] = currentSession.id
		current_session_id = currentSession.id

	current_session = get_object_or_404(YearEnding, id = current_session_id)
	return render(request, 'home/index.html', {"current_session":current_session})


@login_required(login_url='/account/login/')
def takeBackup(request):
	if request.method == "GET" and request.is_ajax():
		forcefully = request.GET.get("forcefully")
		backup = BackupDatabase()
		response = backup.run(forcefully = int(forcefully))
		if response["code"] == 200:
			return JsonResponse(response, status=200)
		else:
			return JsonResponse(response, status=400)
	else:	
		return JsonResponse({}, status=400)	
