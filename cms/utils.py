


# test the request object to see if we're in edit mode
def is_editing(request):
    return ('cms-edit_mode' in request.COOKIES) and request.user.has_module_perms("cms")


def page_is_authorised(request, page):
    if page.authorisation == 'staff':
        return request.user.is_staff
    elif page.authorisation == 'active':
        return request.user.is_authenticated()
    else:
        return True