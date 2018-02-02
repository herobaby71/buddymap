
def update_user(backend, user, request, response, *args, **kwargs):
    if backend.name == 'facebook':
        print("User Requesting:",user)
        print("Facebook Respond:",response)
        faceboookAvatar = 'https://graph.facebook.com/%s/picture?type=large' % response.get('id')
        user.faceboookAvatar = faceboookAvatar
        if(response.get("name")):
            name = response.get("name").strip().split()
            if(len(name) == 1):
                user.firstName = name[0]
            elif(len(name) > 1):
                user.firstName = name[0]
                user.lastName = name[len(name)-1]
        if(response.get("first_name")):
            user.firstName = response.get("first_name")
        if(response.get("last_name")):
            user.lastName = response.get("last_name")
        user.save()
