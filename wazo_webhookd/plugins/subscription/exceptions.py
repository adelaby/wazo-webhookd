# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo.rest_api_helpers import APIException


class NoSuchSubscription(APIException):
    def __init__(self, subscription_uuid):
        super().__init__(
            status_code=404,
            message='No such subscription: {}'.format(subscription_uuid),
            error_id='no-such-subscription',
            details={
                'subscription_uuid': subscription_uuid
            }
        )
