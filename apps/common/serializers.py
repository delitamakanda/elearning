"""
Custom taggit serializer field and mixin to replace the abandoned
django-taggit-serializer package.

Usage
-----
    from apps.common.serializers import TaggitSerializer, TagListSerializerField

    class MySerializer(TaggitSerializer, serializers.ModelSerializer):
        tags = TagListSerializerField()

        class Meta:
            model = MyModel
            fields = ('id', 'tags', ...)
"""

from rest_framework import serializers


class TagListSerializerField(serializers.Field):
    """Serializes a django-taggit ``TaggableManager`` as a flat list of tag names."""

    child = serializers.CharField()

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("default", list)
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if isinstance(data, str):
            data = [tag.strip() for tag in data.split(",") if tag.strip()]
        if not isinstance(data, list):
            raise serializers.ValidationError("Expected a list of tag strings.")
        errors = []
        for item in data:
            try:
                self.child.run_validation(item)
            except serializers.ValidationError as e:
                errors.append(e.detail)
            else:
                errors.append({})
        if any(errors):
            raise serializers.ValidationError(errors)
        return data

    def to_representation(self, value):
        if not value:
            return []
        if hasattr(value, "all"):
            return [tag.name for tag in value.all()]
        return list(value)


class TaggitSerializer(serializers.Serializer):
    """
    Mixin for ModelSerializer classes that include one or more
    ``TagListSerializerField`` fields backed by a ``TaggableManager``.

    Handles saving tags after the instance is created or updated.
    """

    def _get_tag_fields(self):
        return {
            field_name: field
            for field_name, field in self.fields.items()
            if isinstance(field, TagListSerializerField)
        }

    def create(self, validated_data):
        tag_fields = self._get_tag_fields()
        tag_data = {name: validated_data.pop(name, []) for name in tag_fields}
        instance = super().create(validated_data)
        for field_name, tags in tag_data.items():
            getattr(instance, field_name).set(tags)
        return instance

    def update(self, instance, validated_data):
        tag_fields = self._get_tag_fields()
        tag_data = {name: validated_data.pop(name, None) for name in tag_fields}
        instance = super().update(instance, validated_data)
        for field_name, tags in tag_data.items():
            if tags is not None:
                getattr(instance, field_name).set(tags)
        return instance
