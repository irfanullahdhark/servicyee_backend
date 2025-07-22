from dj_rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):
    username = None  # remove username if not used

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.pop("username", None)  # make sure to remove username from cleaned_data
        return data

    @property
    def _has_phone_field(self):
        # Tell allauth there is no phone field
        return False
