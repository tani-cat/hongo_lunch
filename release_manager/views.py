from django.http import Http404
from django.shortcuts import get_object_or_404, render


from . import models


def release_log(request, id=0):
    """リリースログを表示する

    """
    if id == 0:
        # 最新を取得する
        if models.ReleaseLog.objects.count() > 0:
            instance = models.ReleaseLog.objects.last()
        else:
            raise Http404()
    else:
        instance = get_object_or_404(models.ReleaseLog, pk=id)

    context = {
        'ReleaseLog': instance,
        'previousId': None,
        'nextId': None,
    }
    # 前後のリリースへのリンク用
    prev_qs = models.ReleaseLog.objects.filter(id__lt=instance.id)
    if prev_qs.count():
        context.update({
            'previousId': prev_qs.last().id,
        })
    next_qs = models.ReleaseLog.objects.filter(id__gt=instance.id)
    if next_qs.count():
        context.update({
            'nextId': next_qs.first().id,
        })

    return render(request, 'release_manager/release_log.html', context)
