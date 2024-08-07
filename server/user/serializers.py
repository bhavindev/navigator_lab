from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from web3 import Web3


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "password", "password2", "ethereum_wallet_address")
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True}
        }

    def save(self):
        user = get_user_model()(
            email=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            ethereum_wallet_address=self.validated_data["ethereum_wallet_address"],
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError(
                {"password": "Passwords do not match!"})

        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    ethereum_wallet_balance = serializers.SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "is_staff", "first_name", "last_name", "ethereum_wallet_address", "ethereum_wallet_balance")

    def get_ethereum_wallet_balance(self, obj):
        infura_url = 'https://mainnet.infura.io/v3/3b9387b9f0aa45b0ba6b237827bd6a70'
        web3 = Web3(Web3.HTTPProvider(infura_url))
        if not web3.is_connected():
            print("Failed to connect to Ethereum node.")
        else:
            print("Connected to Ethereum node.")
        wallet_address = obj.ethereum_wallet_address
        
        try:
            balance_wei = web3.eth.get_balance(wallet_address)
            balance_eth = web3.from_wei(balance_wei, 'ether')
            return str(balance_eth) + ' ETH'
        except Exception as e:
            return str(e)
