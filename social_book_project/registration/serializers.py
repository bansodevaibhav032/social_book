from rest_framework import serializers
from .models import CustomUser


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id','address','email','password']
        extra_kwargs={
            'password':{"write_only":True}
        }
    #for hash password
    def create(self,validated_data):
        password=validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance