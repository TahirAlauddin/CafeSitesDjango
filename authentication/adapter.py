from allauth.account.adapter import DefaultAccountAdapter


class CustomUserAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):

        return super(CustomUserAdapter, self).save_user(
            request, user, form, commit
        )
        