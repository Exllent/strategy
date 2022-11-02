from django.views import View

from main.models import Castle, ResourceBuildings
from main.services import MixinHomePage, CastleMixin, CastleProductionMixin


class Home(MixinHomePage, View):
    """Класс отображающий главную страницу"""
    template_name = 'main/index.html'
    model_castle = Castle


class CastleBuilding(CastleMixin, View):
    """Класс отображающий здания замка и их уровень"""
    template_name = 'main/castle.html'
    model_castle = Castle


class CastleProduction(CastleProductionMixin, View):
    """Класс для улучшения ресурсо добывающих зданий замка"""
    template_name = 'main/castle_production.html'
    model_castle = Castle
    model_resource_buildings = ResourceBuildings






































# def castle(request):
#     template_name = 'main/castle.html'
#     castle = Castle.objects.get(pk=1)
#     if request.method == "POST":
#         get_building(request, castle)
#         return redirect(castle)
#     context = {'castle': castle}
#     return render(request=request, template_name=template_name, context=context)


# def home(request):
#     if request.user.is_authenticated:
#         id = getattr(request.user, 'id')
#         castle = Castle.objects.get(player_id=id)
#         template_name = 'main/index.html'
#         context = {'castle': castle}
#         return render(request=request, template_name=template_name, context=context)
#     else:
#         return redirect('register')


# def register2(request):
#     if request.method == 'POST':
#         id = getattr(request.user, 'id')
#         user = Player.objects.get(pk=id)
#         form = PlayerRegisterForm(request.POST)
#         if form.is_valid():
#             user.first_name, user.race_id = form.data['first_name'], form.data['race']
#             login(request, user)
#             user.save()
#             Castle.objects.create(name=f"{user.first_name}_castle_{randrange(5000, 100000)}", player_id=user.pk)
#             return redirect('home')
#     else:
#         form = PlayerRegisterForm()
#     return render(request, 'main/register2.html', {'form': form})


# def authenticated(request):
#     if request.user.is_authenticated:
#         if request.user.race is None:
#             return redirect('register2')
#         return redirect('home')
#     return redirect('register')


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         messages.success(request, message="Регистрация прошла успешно")
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('register2')
#         else:
#             messages.error(request, message='Ошибка регистрации')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'main/register.html', {'form': form})


# def user_login(request):
#     if request.method == "POST":
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserLoginForm()
#     return render(request, template_name='main/login.html', context={'form': form})
