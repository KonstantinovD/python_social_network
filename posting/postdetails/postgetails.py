from django.http import HttpResponseRedirect

from posting.forms import CommentForm


def process_post_request(request, post_detail):
    if 'create_comment' in request.POST:
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            cd = comment_form.cleaned_data
            new_comment = comment_form.save(commit=False)
            new_comment = fill_new_comment_data(request, new_comment, post_detail)
            new_comment.save()
            return HttpResponseRedirect(request.path.replace('/comment', ''))
        else:
            return HttpResponseRedirect(request.path.replace('/comment', ''))
    if 'create_like_value' in request.POST:
        pass
    return HttpResponseRedirect(request.path)


def fill_new_comment_data(request, new_comment, post_detail):
    new_comment.user = request.user
    new_comment.post = post_detail

    try:
        latest_comment = post_detail.comments.order_by("-num_related_to_article")[0]
    except IndexError:
        latest_comment = None

    if latest_comment is None:
        related_index = 1
    else:
        related_index = latest_comment.num_related_to_article + 1

    new_comment.num_related_to_article = related_index

    return new_comment