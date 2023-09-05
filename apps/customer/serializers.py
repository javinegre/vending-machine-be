from rest_framework import serializers


class WalletSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    balance = serializers.DecimalField(max_digits=6, decimal_places=2)


class CustomerSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    user_name = serializers.CharField()
    profile = serializers.SerializerMethodField()
    wallet = WalletSerializer()

    def get_profile(self, instance) -> dict[str, str]:
        return {'first_name': instance.first_name, 'last_name': instance.last_name}
