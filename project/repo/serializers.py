from rest_framework import serializers
from .models import Tasks

class TasksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tasks
        fields = [ 'name','id', 'title', 'description','task', 'uploaded_at']

