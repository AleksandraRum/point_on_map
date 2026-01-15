from django.contrib.gis.geos import Point as geoPoint
from rest_framework import serializers

from points.models import Message, Point


class PointSerializer(serializers.ModelSerializer):
    longitude = serializers.FloatField(write_only=True)
    latitude = serializers.FloatField(write_only=True)

    class Meta:
        model = Point
        fields = "__all__"
        read_only_fields = (
            "user",
            "location",
        )

    def create(self, validated_data):
        request = self.context.get("request")

        user = request.user

        validated_data["user"] = user

        lon = validated_data.pop("longitude")
        lat = validated_data.pop("latitude")

        if lon is not None and lat is not None:
            location = geoPoint(lon, lat, srid=4326)
            validated_data["location"] = location

        point = Point.objects.create(**validated_data)
        return point

    def validate_latitude(self, data):
        if not -90 <= data <= 90:
            raise serializers.ValidationError(
                "Значение широты должно быть в диапазоне от -90 до 90"
            )
        return data

    def validate_longitude(self, data):
        if not -180 <= data <= 180:
            raise serializers.ValidationError(
                "Значение долготы должно быть в диапазоне от -180 до 180"
            )
        return data


class PointSearchSerializer(serializers.Serializer):
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    radius = serializers.FloatField(min_value=0.0001, max_value=10000)

    def validate_latitude(self, data):
        if not -90 <= data <= 90:
            raise serializers.ValidationError(
                "Значение широты должно быть в диапазоне от -90 до 90"
            )
        return data

    def validate_longitude(self, data):
        if not -180 <= data <= 180:
            raise serializers.ValidationError(
                "Значение долготы должно быть в диапазоне от -180 до 180"
            )
        return data


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ("author",)

    def create(self, validated_data):
        request = self.context.get("request")

        user = request.user

        validated_data["author"] = user

        message = Message.objects.create(**validated_data)
        return message
