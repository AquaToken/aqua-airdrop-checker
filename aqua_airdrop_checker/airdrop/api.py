from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from constance import config

from aqua_airdrop_checker.airdrop.models import AirdropAccount, AirdropPayment
from aqua_airdrop_checker.airdrop.serializers import AirdropAccountSerializer, AirdropPaymentSerializer
from aqua_airdrop_checker.airdrop.utils import attach_payment_list_state


class AccountCheckView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = AirdropAccountSerializer

    def get_object(self):
        return get_object_or_404(AirdropAccount, public_key=self.request.query_params.get('account'))

    def get_payment_list(self, account):
        payment_list = list(AirdropPayment.objects.filter(account=account).order_by('phase'))

        attach_payment_list_state(account.public_key, payment_list)

        for index in range(6):
            if len(payment_list) < index:
                payment = AirdropPayment(
                    phase=index,
                    account=account,
                )

                payment.state = AirdropPayment.STATE_COMING
                payment.start = getattr(config, f'PHASE_{index}_START')
                payment.end = getattr(config, f'PHASE_{index}_END')

                payment_list.append(payment)

        return payment_list

    def get(self, request, *args, **kwargs):
        instance = self.get_object()

        payment_list = self.get_payment_list(instance)

        serializer = self.get_serializer(instance=instance)

        data = serializer.data
        data['phase'] = AirdropPaymentSerializer(instance=payment_list, many=True).data
        return Response(data)
