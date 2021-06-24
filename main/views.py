from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin#примесь для зарегистрированных пользователей
from django.views.generic.edit import UpdateView 
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import AstroUser
from .forms import ChangeUserInfoForm
from django.contrib.auth.views import PasswordChangeView 
from django.views.generic.edit import CreateView 
from .forms import RegisterUserForm
from django.views.generic.base import TemplateView  
from django.core.signing import BadSignature 
from .utilities import signer 
from django.views.generic.edit import DeleteView 
from django.contrib.auth import logout 
from django.contrib import messages 
#from django.contrib.auth.views import PasswordResetView
#from django.contrib.auth.views import PasswordResetDoneView
#from django.contrib.auth.views import PasswordResetConfirmView
#from django.contrib.auth.views import PasswordResetCompleteView
from django.core.paginator import Paginator 
from django.db.models import Q 
from .models import SubRubric, Bb
from .forms import SearchForm 
from django.shortcuts import redirect 
from .forms import BbForm
from .forms import AIFormSet
from .models import Comment 
from .forms import UserCommentForm 
from .forms import GuestCommentForm


#реализация контроллера главной страницы с помощью функции
def index(request):
    bbs = Bb.objects.filter(is_active=True)[:10]
    context = {'bbs': bbs}
    return render(request, 'main/index.html', context)

#генератор адресов
def other_page(request, page):
    try:
        template = get_template('main/' + page + 'html')
        #поднятие исключения
    except TemplateDoesNotExist:
        #перехват исключения и вывод http404
        raise Http404
    return HttpResponse(template.render(request=request))

#контроллер страницы входа - расширение класа loginView
class AstroLoginView(LoginView):
    template_name = 'main/login.html'

#контролер профиля пользователя
@login_required#декоратор функции, подтверждающий, что пользователь вошел
def profile(request):
    bbs = Bb.objects.filter(author=request.user.pk)
    context = {'bbs': bbs}
    return render(request, 'main/profile.html', context)


#раелизация контроллера выхода через класс LogoutView
class AstroLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


#используем класс UpdateView для изменения пользовательских данных
class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AstroUser
    template_name = 'main/ch_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя успешно изменены'
    
    #получаем ключ текущего пользователя
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk 
        return super().setup(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


#онтроллер изменения пароля создаем, расширяя класс PasswordChangeView
class AstroPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_ch.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль успешно изменен'

#контроллеро регистрации пользователя
class RegisterUserView(CreateView):
    model = AstroUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')


#вывод сообщения о регистрации пользователя
class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


#контроллер активации
def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad.html')
    user = get_object_or_404(AstroUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True 
        user.is_activated = True 
        user.save()
    return render(request, template)

#удаление профиля
class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AstroUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post (self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


#
def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    bbs = Bb.objects.filter(is_active=True, rubric=pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''

    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1 
    page = paginator.get_page(page_num)
    context = {'rubric': rubric, 'page': page, 'bbs': page.object_list, 'form': form} 
    return render(request, 'main/by_rubric.html', context) 


#функция детального рассмотрения новости и комментариев
def detail(request, rubric_pk, pk):
    #bb = get_object_or_404(Bb, pk=pk)
    bb = Bb.objects.get(pk=pk)
    ais = bb.additionalimage_set.all()
    comments = Comment.objects.filter(bb=pk, is_active=True)
    initial = {'bb': bb.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_class = UserCommentForm
    else:
        form_class = GuestCommentForm
    form = form_class(initial=initial)
    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Комментарий успешно добавлен')
        else:
            form = c_form
            messages.add_message(request, messages.WARNING, 'Комментарий не добавлен')
    context = {'bb': bb, 'ais': ais, 'comments': comments, 'form': form}
    return render(request, 'main/detail.html', context)
    #context = {'bb': bb, 'ais': ais}
    #return render(request, 'main/profile_detail.html', context)

#контроллер для просмотра сведений о новостях добавленных одним пользователем
@login_required
def profile_bb_detail(request, rubric_pk, pk):
    bb = get_object_or_404(Bb, pk=pk)
    ais = bb.additionalimage_set.all()
    context = {'bb': bb, 'ais': ais}
    return render(request, 'main/detail.html', context)


#контроллер добавления новостей 
@login_required
def profile_bb_add(request):
    if request.method == 'POST':
        form = BbForm(request.POST, request.FILES)
        if form.is_valid():
            bb = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=bb)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Новость успешно добавлена') 
                return redirect('main:profile')
    else:
        form = BbForm(initial={'author': request.user.pk})
        formset = AIFormSet()
    context = {'form': form, 'formset': formset}
    return render(request, 'main/profile_bb_add.html', context)
'''
при создании формы перед выводом страницы 
охранения мы заносим в поле author формы ключ текущего
пользователя, который станет автором объявления.
во время сохранения введенного объявления, при создании объектов
формы и набора форм, мы должны передать конструкторам их классов вторым по­
зиционным параметром словарь со всеми полученными файлами (он хранится
в атрибуте FILES объекта запроса). Если мы не сделаем этого, то отправленные
пользователем иллюстрации окажутся потерянными
при сохранении мы сначала выполняем валидацию и сохранение формы
самого объявления. Метод s ave ( ) в качестве результата возвращает сохраненную
запись, и эту запись мы должны передать через параметр instance конструктору
класса набора форм. Это нужно для того, чтобы все дополнительные иллюстрации
после сохранения оказались связанными с объявлением.
'''
#контроллер удаления и редактирования новости
@login_required
def profile_bb_change(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    if request.method == 'POST':
        form = BbForm(request.POST, request.FILES, instance=bb)
        if form.is_valid():
            bb = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=bb)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Новость отредактирована')
                return redirect('main:profile')
    else:
        form = BbForm(instance=bb)
        formset = AIFormSet(instance=bb)
    context = {'form': form, 'formset': formset}
    return render(request, 'main/profile_bb_change.html', context)

@login_required
def profile_bb_delete(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    if request.method == 'POST':
        bb.delete()
        messages.add_message(request, messages.SUCCESS, 'Новость удалена')
        return redirect('main:profile')
    else:
        context = {'bb': bb}
        return render(request, 'main/profile_bb_delete.html', context)



'''
#сброс пароля
class ResetPasswordView(PasswordResetView):
    model = AstroUser
    template_name = 'main/reset.html'
    #success_url = reverse_lazy('main:login')
    success_message = 'Cброс пароля'
    #
class ResetPasswordConfirmView(PasswordResetConfirmView):
    model = AstroUser
    template_name = 'main/reset_confirm.html'
    #success_url = reverse_lazy('main:login')


class ResetPasswordDoneView(PasswordResetDoneView):
    model = AstroUser
    template_name = 'main/reset_done.html'
    #success_url = reverse_lazy('main: ')
class ResetPasswordCompleteView(PasswordResetCompleteView):
    model = AstroUser
    template_name = 'main/reset_complete.html'
    '''

