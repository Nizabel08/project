import time

class CarMiddleware :
    # current time - last time
    # last time - current time - time.time()
    def __init__(self, get_response): # საჭიროა ყველა middleware-ში, ნიციალიზაციის ნაწილია.
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        if request.path.startswith('/Cars') :
            print(f'[car] request to {request.path} took {duration:.3f} seconds')
        return response 

