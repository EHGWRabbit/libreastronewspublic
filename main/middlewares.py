from .models import SubRubric 

#обработчик контекста
def astron_context_processor(request):
    context = {}
    #список подрубрик хранится в переменной   rubrics
    #keyword для генерирования адресов
    #all для указания на страницы сведений о новостях
    context['rubrics'] = SubRubric.objects.all()
    context['keyword'] = ''
    context['all'] = ''
    if 'keyword' in request.GET:
        keyword = request.GET['keyword'] 
        if keyword:
            context['keyword'] = '?keyword=' + keyword
            context['all'] = context['keyword']
    if 'page' in request.GET:
        page = request.GET['page']
        if page != '1':
            if context['all']:
                context['all'] += '&page=' + page
            else:
                context['all'] = '?page=' + page
    return context