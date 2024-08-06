from rest_framework import serializers
from .models import UnitOfMeasurements


class UOMSerializers(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(requred=True, allow_blank=False)
    field = serializers.ChoiceField(choices={"1": "Float", "2": "Integer"}, default="1")

    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # code = serializers.CharField(style={"base_template": "textarea.html"})
    # linenos = serializers.BooleanField(required=False)
    # language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default="python")
    # style = serializers.ChoiceField(choices=STYLE_CHOICES, default="friendly")

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return UnitOfMeasurements.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.field = validated_data.get("field", instance.field)
        instance.save()
        return instance

        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        # instance.title = validated_data.get("title", instance.title)
        # instance.code = validated_data.get("code", instance.code)
        # instance.linenos = validated_data.get("linenos", instance.linenos)
        # instance.language = validated_data.get("language", instance.language)
        # instance.style = validated_data.get("style", instance.style)
        # instance.save()
        # return instance
