from . import models

def RequestObjectMiddleware(get_response):
    # one-time configuration and initialization
    
    def middleware(request):
        #code to be executed for each request
        #the view (and later middleware) are called.
        
        models.request_object = request
        
        response = get_response(request)
        
        #code to be executed for each reaquest/response after
        #the view is called.
        
        return response
    
    return middleware