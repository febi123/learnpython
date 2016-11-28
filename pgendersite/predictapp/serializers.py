from rest_framework import serializers
from predictapp.models import Predictlog
from predictapp.predictgender import Predictgender,Predictgenderresult
from django.contrib.auth.models import User
from predictapp.classify.modelclassify import Genderclassify

class PredictlogSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='predictlog-highlight', format='html')

    class Meta:
        model = Predictlog
        fields = field = ('url','id', 'highlight', 'owner',
                          'name', 'suku', 'prob_men', 'prob_women', 'feedback', 'feedback_reason', 'api_consumer', 'client_ip')
            # ('url', 'id', 'highlight', 'owner',
            #       'title', 'code', 'linenos', 'language', 'style')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    predictlog = serializers.HyperlinkedRelatedField(many=True, view_name='predictlog-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'predictlog')

class PredictgenderSerializer(serializers.Serializer):
    nama = serializers.CharField(max_length=250)
    suku = serializers.CharField(max_length=250)

    def create(self, validated_data):
        # print(validated_data['nama'])
        # gc = Genderclassify()
        # res = gc.predict({validated_data['nama']})
        # create serializs baru buat yg result
        return Predictgender( **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance

class PredictgenderresultSerializer(serializers.Serializer):
    nama = serializers.CharField(max_length=250)
    suku = serializers.CharField(max_length=250,allow_blank=True, required=False)
    jk = serializers.CharField(max_length=1,allow_blank=True, allow_null=True, required=False)
    prob = serializers.DecimalField(11,8,None ,None,None,None,allow_null=True, required=False)

    def create(self, validated_data):
        # print(validated_data['nama'])
        gc = Genderclassify()
        res = gc.predict({validated_data['nama']})

        validated_data1 = {'nama' : validated_data['nama'],
                           'suku': validated_data['suku'],
                           'jk': '1' if res[0][0]>res[0][1] else '2',
                           'prob' : res[0][0] if res[0][0] > res[0][1] else res[0][1]
                           }
        # validated_data1['nama'] = validated_data['nama']
        # validated_data1['suku'] = validated_data['suku']
        # validated_data1['jk'] = '1'#'''1' if res[0][0]>res[0][1] else '2'
        # validated_data1['prob'] = 0.0#res[0][0] if res[0][0] > res[0][1] else res[0][1]
        # create serializs baru buat yg result
        return Predictgenderresult(**validated_data1)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance

# class PredictlogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Predictlog
#         owner = serializers.ReadOnlyField(source='owner.username')
#         fields = '__all__'
#         # field = ('id', 'name', 'suku', 'prob_men', 'prob_women', 'feedback', 'feedback_reason', 'api_consumer', 'client_api')
#
#
# class UserSerializer(serializers.ModelSerializer):
#     predictlog = serializers.PrimaryKeyRelatedField(many=True, queryset=Predictlog.objects.all())
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'predictlog')

# class PredictlogSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(required=True, max_length=250)
#     suku = serializers.CharField(required=False, allow_blank=True, max_length=250)
#     prob_men = serializers.DecimalField(max_digits=11, decimal_places=8, allow_null=True)
#     prob_women = serializers.DecimalField(max_digits=11, decimal_places=8, allow_null=True)
#     feedback = serializers.CharField(required=False, allow_blank=True, max_length=1)
#     feedback_reason = serializers.CharField(required=False, allow_blank=True, max_length=500)
#     api_consumer = serializers.CharField(required=False, allow_blank=True, max_length=1000)
#     client_ip = serializers.CharField(required=False, allow_blank=True, max_length=50)
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Predictlog` instance, given the validated data.
#         """
#         return Predictlog.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.name = validated_data.get('name', instance.name)
#         instance.suku = validated_data.get('suku', instance.suku)
#         instance.prob_men = validated_data.get('prob_men', instance.prob_men)
#         instance.prob_women = validated_data.get('prob_women', instance.prob_women)
#
#         instance.feedback = validated_data.get('feedback', instance.feedback)
#         instance.feedback_reason = validated_data.get('feedback_reason', instance.feedback_reason)
#         instance.api_consumer = validated_data.get('api_consumer', instance.api_consumer)
#         instance.client_ip = validated_data.get('prob_women', instance.client_ip)
#         instance.save()
#         return instance