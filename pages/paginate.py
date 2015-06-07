from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate(results, page):
    paginator = Paginator(results, 10)
    try:
        result_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result_page = paginator.page(paginator.num_pages)
    return result_page