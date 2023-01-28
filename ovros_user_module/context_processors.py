from .profile_detail import ProfileData


def profile_data(request):
    return {'profile_data': ProfileData(request)}

