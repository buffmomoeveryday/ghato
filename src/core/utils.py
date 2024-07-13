

def require_htmx(view_func):
    def wrapper(request, *args, **kwargs):
        if request.headers.get("HX-Request"):
            pass
        else:
            raise 
        response = view_func(request, *args, **kwargs)
        # code to be executed after the view
        return response

    return wrapper
