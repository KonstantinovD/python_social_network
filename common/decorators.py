from django.http import HttpResponseBadRequest


# Декоратор ajax_required. В нем определена функция, которая возвращает объект
# HttpResponseBadRequest, если запрос не является AJAX-запросом
# Теперь, если вы обратитесь к URL’у http://127.0.0.1:8000/images/like/ напрямую через браузер, то получите ошибку 400.
def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__ = f.__name__
    return wrap