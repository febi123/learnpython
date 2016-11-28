"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from datetime import datetime
import json
from predictapp.classify.modelclassify import Genderclassify
from django.contrib.auth.models import User
from rest_framework import permissions

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework import renderers
from rest_framework.response import Response
import requests


# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
# from predictapp.models import Predictlog
# from predictapp.serializers import PredictlogSerializer

# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from predictapp.models import Predictlog
# from predictapp.serializers import PredictlogSerializer

from predictapp.models import Predictlog
from predictapp.permissions import IsOwnerOrReadOnly
from predictapp.serializers import PredictlogSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from rest_framework import mixins
# from rest_framework import generics

from predictapp.models import Predictlog
from predictapp.serializers import PredictlogSerializer,UserSerializer,PredictgenderSerializer,PredictgenderresultSerializer
# from rest_framework import generics


from rest_framework import viewsets
from rest_framework.decorators import detail_route

from predictapp.predictgender import Predictgender


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'predictapp/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def runmodel(request):
    """Renders the crawl page."""
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        #post_text = request.POST.get('the_post')
        response_data = {}

        gc = Genderclassify()
        res1 = gc.generatemodel()
        res2 = gc.generatemodelbynameandsuku()
        #post = Post(text=post_text, author=request.user)
        #post.save()

        response_data['result1'] = res1
        response_data['result2'] = res2
        #response_data['postpk'] = post.pk
        #response_data['text'] = post.text
        #response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
        #response_data['author'] = post.author.username

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return render(
        request,
        'predictapp/runmodel.html',
        {
            'title':'Generate model',
            'year':datetime.now().year,
        }
    )

def obtain_auth_token(request):
    if request.method == 'POST':
        request.POST.get('username')
        request.POST.get('password')
        response_data = {'token' : 'bla bla'}
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return render(
            request,
            'predictapp/index.html',
            {
                'title': 'Generate model',
                'year': datetime.now().year,
            }
        )


def predictasync(request):
    """Renders the crawl page."""
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        #post_text = request.POST.get('the_post')
        url = "http://"+request.get_host()+"/predictgender/{0}/{1}"
        print(url)
        response_data = {}
        # print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        # # print(request.auth)
        # print(request.user)
        # print(request.user.username)
        # print(request.user.password)
        nama = request.POST.get('nama')
        suku = request.POST.get('suku')
        address = (url .format(nama,suku))
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(address)
        r = requests.get(address)
        res = r.json()

        print(res)
        print('-------------------------------------------------------------')

        response_data['nama'] = nama
        response_data['suku'] = suku
        response_data['jk'] = res['jk']
        response_data['prob'] = res['prob']

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return render(
        request,
        'predictapp/runmodel.html',
        {
            'title':'Generate model',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'predictapp/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'predictapp/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )


# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders its content into JSON.
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)

#
# @csrf_exempt
# def predictlog_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Predictlog.objects.all()
#         serializer = PredictlogSerializer(snippets, many=True)
#         return JSONResponse(serializer.data)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = PredictlogSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data, status=201)
#         return JSONResponse(serializer.errors, status=400)
#
# @csrf_exempt
# def predictlog_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = Predictlog.objects.get(pk=pk)
#     except Predictlog.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = PredictlogSerializer(snippet)
#         return JSONResponse(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = PredictlogSerializer(snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data)
#         return JSONResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return HttpResponse(status=204)


# @api_view(['GET', 'POST'])
# def predictlog_list(request, format=None):
#     """
#     List all snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Predictlog.objects.all()
#         serializer = PredictlogSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = PredictlogSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def predictlog_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     try:
#         snippet = Predictlog.objects.get(pk=pk)
#     except Predictlog.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = PredictlogSerializer(snippet)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = PredictlogSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class PredictlogList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         snippets = Predictlog.objects.all()
#         serializer = PredictlogSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = PredictlogSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class PredictlogDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Predictlog.objects.get(pk=pk)
#         except Predictlog.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = PredictlogSerializer(snippet)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = PredictlogSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# class PredictlogList(generics.ListCreateAPIView):
#     queryset = Predictlog.objects.all()
#     serializer_class = PredictlogSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class PredictlogDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Predictlog.objects.all()
#     serializer_class = PredictlogSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
#
#
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'predictlog': reverse('predictlog-list', request=request, format=format),
        'predictgender': reverse('predictgender-predict', request=request, format=format)
    })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PredictlogViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Predictlog.objects.all()
    serializer_class = PredictlogSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        print('oy.. save')
        serializer.save(owner=self.request.user)

# class PredictlogHighlight(generics.GenericAPIView):
#     queryset = Predictlog.objects.all()
#     renderer_classes = (renderers.StaticHTMLRenderer,)
#
#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)

# Global variable used for the sake of simplicity.
# In real life, you'll be using your own interface to a data store
# of some sort, being caching, NoSQL, LDAP, external API or anything else


# predictgenders = {
# }
#
#
# def get_next_task_id():
#     return max(predictgenders) + 1


class PredictgenderViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = PredictgenderSerializer

    # def list(self, request):
    #     serializer = PredictgenderSerializer(
    #         instance=predictgenders.values(), many=True)
    #     return Response(serializer.data)

    def create(self, request):
        serializer = PredictgenderresultSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            # tasks[task.id] = task
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, nama,suku=None):
        try:
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            print(nama)
            print(suku)
            gc = Genderclassify()
            res = gc.predict(nama,suku)
            print(res)

            validated_data1 = {'nama': nama,
                               'suku': suku,
                               'jk': '1' if res[0][0] > res[0][1] else '2',
                               'prob': res[0][0] if res[0][0] > res[0][1] else res[0][1]
                               }

            serializer = PredictgenderresultSerializer(validated_data1)
            return Response(serializer.data)
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # serializer = PredictgenderresultSerializer({'nama':nama,'suku':suku})
        # return Response(serializer.data)
    #
    # def update(self, request, pk=None):
    #     try:
    #         task = tasks[int(pk)]
    #     except KeyError:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     except ValueError:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     serializer = serializers.TaskSerializer(
    #         data=request.data, instance=task)
    #     if serializer.is_valid():
    #         task = serializer.save()
    #         tasks[task.id] = task
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def partial_update(self, request, pk=None):
    #     try:
    #         task = tasks[int(pk)]
    #     except KeyError:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     except ValueError:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     serializer = serializers.TaskSerializer(
    #         data=request.data,
    #         instance=task,
    #         partial=True)
    #     if serializer.is_valid():
    #         task = serializer.save()
    #         tasks[task.id] = task
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def destroy(self, request, pk=None):
    #     try:
    #         task = tasks[int(pk)]
    #     except KeyError:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     except ValueError:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     del tasks[task.id]
    #     return Response(status=status.HTTP_204_NO_CONTENT)