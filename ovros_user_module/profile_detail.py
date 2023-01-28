from django.conf import settings


class ProfileData(object):
    def __init__(self, request):
        self.session = request.session
        profile_data = self.session.get(settings.PROFILE_DETAIL_SESSION_ID)
        if not profile_data:
            profile_data = self.session[settings.PROFILE_DETAIL_SESSION_ID] = {}
        self.profile_data = profile_data

    def add(self, user, profile, profile_role):
        user_id = str(user)
        profile_id = str(profile)
        profile_role = profile_role

        self.profile_data[settings.PROFILE_DETAIL_SESSION_ID] = {
            'user_id': user_id,
            'profile_id': profile_id,
            'profile_role': profile_role
        }
        self.save()

    def save(self):
        # make the session as "modified" to makesure it gets saved
        self.session.modified = True

    def remove(self):
        if settings.PROFILE_DETAIL_SESSION_ID in self.profile_data:
            del self.profile_data[settings.PROFILE_DETAIL_SESSION_ID]
            self.save()

    def get_user_id(self):
        return self.profile_data[settings.PROFILE_DETAIL_SESSION_ID]['user_id']

    def get_profile_id(self):
        return self.profile_data[settings.PROFILE_DETAIL_SESSION_ID]['profile_id']

    def get_profile_role(self):
        return self.profile_data[settings.PROFILE_DETAIL_SESSION_ID]['profile_role']

