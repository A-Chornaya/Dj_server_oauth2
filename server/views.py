from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import UserData, Client, ClientForm, Grant, AccessToken, RefreshToken
from .models import UserForm

SCOPE = ('email', 'first_name', 'last_name')


def index(request):
    try:
        id = request.session['user_id']
    except KeyError:
        user_name = 'anonymous user'
    else:
        user = UserData.objects.get(user_id=id)
        user_name = user.login
    return render(request, 'server/index.html', {'user_name': user_name})


def register_app(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            client = Client.objects.latest(field_name='id')
            request.session['client_id'] = client.id
            return HttpResponseRedirect('/server/app')
    elif request.method == 'GET':
        form = ClientForm()
        return render(request, 'server/app_add.html', {'form': form})


def info_app(request):
    client = Client.objects.get(id=request.session['client_id'])
    return render(request, 'server/app_info.html', {'client': client})


def login(request):
    if request.method == 'GET':
        return render(request, 'server/login.html')
    elif request.method == 'POST':
        try:
            user = UserData.objects.get(login=request.POST['login'])
        except ObjectDoesNotExist:
            return HttpResponse("You aren`t registered.")
        if user.password == request.POST['password']:
            request.session['user_id'] = user.user_id
            messages.success(request, 'You are logged in.')
        else:
            messages.success(request, 'Your username and password didn`t match.')
        try:
            type = request.session['type']
        except KeyError:
            return HttpResponseRedirect('/server/')
        else:
            if type == 'authorization':
                request.session['type'] = 'login'
                return render(request, 'server/authorisation.html', {'scope': SCOPE})
            else:
                return HttpResponseRedirect('/server/')


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'A new user added successfully')
        return HttpResponseRedirect('/server/login/')
    else:
        form = UserForm()
        return render(request, 'server/signup.html',
                      {'form': form})


def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    messages.success(request, 'You are logged out.')
    return HttpResponseRedirect('/server/')


def authorize(request):
    if request.method == 'POST':
        redirect_uri = request.session['redirect_uri']
        if '_allow' in request.POST:
            client = Client.objects.get(client_id=request.session['client_id'])
            user = UserData.objects.get(user_id=request.session['user_id'])
            scopes = []
            for s in SCOPE:
                scope = request.POST.get(s, '')
                if scope:
                    scopes.append(scope)
            try:
                grant = Grant.objects.get(client=client, user=user)
            except ObjectDoesNotExist:
                pass
            else:
                grant.delete()
            # Making new grant
            grant = Grant(user=user, client=client,
                          redirect_uri=redirect_uri,
                          scope=','.join(scopes))
            grant.save()
            return redirect(redirect_uri + '?code=' + grant.code)
        elif '_deny' in request.POST:
            messages.error(request, 'User doesn`t allow to use his information.')
            return redirect(redirect_uri)
    elif request.method == 'GET':
        try:
            client = Client.objects.get(client_id=request.GET.get('client_id', ''))
        except ObjectDoesNotExist:
            return render(request, 'server/not_found.html', {'message': 'This client app doesn`t '
                                                                        'registered'})
        else:
            request.session['client_id'] = request.GET.get('client_id')
            request.session['redirect_uri'] = request.GET.get('redirect_uri', '')
            try:
                id = request.session['user_id']
            except KeyError:
                request.session['type'] = 'authorization'
                return HttpResponseRedirect('/server/login')
            else:
                return render(request, 'server/authorisation.html', {'scope': SCOPE})


def token(request):
    if request.method == 'POST':
        grant_type = request.POST.get('grant_type')
        client_id = request.POST.get('client_id')
        client_secret = request.POST.get('client_secret')
        code = request.POST.get('code')
        result_dict = {}
        try:
            user = UserData.objects.get(grant__code=code)
        except ObjectDoesNotExist:
            result_dict['message'] = 'This user doesn`t registered'
        except KeyError:
            result_dict['message'] = 'This user doesn`t login'
        else:
            if grant_type == 'authorization_code':
                try:
                    client = Client.objects.get(client_id=client_id)
                except ObjectDoesNotExist:
                    result_dict['message'] = 'This client app doesn`t registered'
                else:
                    if client_secret == client.client_secret:
                        grant = Grant.objects.get(client=client, user=user)
                        if grant and (code == grant.code):
                            token_obj = AccessToken(user=user, client=client, scope=grant.scope)
                            token_obj.save()
                            refresh_token_obj = RefreshToken(user=user, client=client,
                                                             access_token=token_obj)
                            refresh_token_obj.save()
                            result_dict = {'access_token': token_obj.token,
                                            'token_type': 'Bearer',
                                            'expires_in': token_obj.expires,
                                            'refresh_token': refresh_token_obj.token,
                                            'id': token_obj.pk
                                            }
                            scope_list = token_obj.scope.split(',')
                            result_dict['info'] = {}
                            user_dict = UserData.objects.filter(user_id=user.user_id).values()[0]
                            for s in scope_list:
                                if s in user_dict:
                                    result_dict['info'][s] = user_dict[s]
                        else:
                                result_dict['message'] = 'Code of client app is wrong'
                    else:
                        result_dict['message'] = 'Client_id and client_secret didn`t match'

        return JsonResponse(result_dict)

    elif request.method == 'GET':
        return HttpResponseRedirect('/server/')


def error(request):
    return render(request, 'server/not_found.html', {'message': 'some error'})
