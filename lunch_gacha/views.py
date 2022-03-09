import json
import random
import traceback

import requests

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from django.views.decorators.csrf import requires_csrf_token

from . import forms, models


@requires_csrf_token
def notice_slack_handler500(request, *args, **kwargs):
    """本番環境の500エラーをSlack通知するハンドラ

    """
    _data = {
        'attachments': [
            {
                'color': '#ff4444',
                'author_name': '500 Error has thrown',
                'fields': [
                    {
                        'title': 'Request URI',
                        'value': request.build_absolute_uri(),
                        'short': False,
                    },
                    {
                        'title': 'Traceback',
                        'value': traceback.format_exc(),
                        'short': False,
                    },
                ],
            }
        ]
    }
    _url = getattr(settings, 'ERROR_WEBHOOK_URL', None)
    if _url is not None:
        requests.post(_url, data=json.dumps(_data))
    return HttpResponseServerError('<html><body><h1>Server Error(500)</h1></body></html>')


@requires_csrf_token
def custom_handler500(request, *args, **kwargs):
    """本場環境で不具合チェックするためのハンドラ

    """
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)


class GachaView(generic.FormView):
    """ガチャ実行画面

    """

    template_name = 'lunch_gacha/gacha.html'
    form_class = forms.GachaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            q_data = self.request.session.get('query', '')
            form = self.form_class(initial=q_data)
            context.update({
                'form': form,
            })
        return context

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            raise HttpResponseBadRequest()

        conditions = form.cleaned_data

        search_key = {
            'is_valid': True,
        }
        if conditions['district']:
            search_key['district__in'] = conditions['district']
        if conditions['genre']:
            search_key['genre__in'] = conditions['genre']

        queryset = models.LunchPlace.objects.filter(**search_key)
        if queryset.count() == 0:
            # 対象がない
            messages.error(request, '条件に一致するランチが見つかりませんでした。')
            return self.get(request, **kwargs)

        index = random.randint(0, len(queryset) - 1)
        answer = queryset[index].id
        q_data = dict(request.POST)
        del q_data['csrfmiddlewaretoken']
        request.session.update({
            'answer': answer,
            'query': q_data,
        })
        return redirect('lunch_gacha:result')


class GachaResultView(generic.TemplateView):
    """ガチャ結果画面

    """

    template_name = 'lunch_gacha/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _answer = None
        if 'answer' in self.request.session:
            # GachaViewから遷移している場合
            _answer = self.request.session['answer']

        context.update({
            'LunchPlace': get_object_or_404(models.LunchPlace, pk=_answer),
        })

        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        if context['LunchPlace'] is None:
            # ガチャ結果がない場合はガチャ画面に遷移
            messages.error(request, 'まずはガチャを引いてください')
            return redirect('lunch_gacha:gacha')

        return render(request, self.template_name, context)


class GachaListView(generic.ListView):
    """ガチャの出力結果一覧画面

    """

    model = models.LunchPlace
    template_name = 'lunch_gacha/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_valid=True)
        queryset = queryset.select_related('district')
        queryset = queryset.prefetch_related('genre')
        queryset = queryset.order_by('district', 'name')
        return queryset
