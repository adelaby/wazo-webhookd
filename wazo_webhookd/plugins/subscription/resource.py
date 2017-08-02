# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import uuid
from flask import request
from wazo_webhookd.core.rest_api import AuthResource
from xivo.auth_verifier import required_acl

from .schema import subscription_schema


class SubscriptionsResource(AuthResource):

    def __init__(self, service):
        self._service = service

    @required_acl('webhookd.subscriptions.read')
    def get(self):
        subscriptions = list(self._service.list())
        return {'items': subscription_schema.dump(subscriptions, many=True).data,
                'total': len(subscriptions)}

    @required_acl('webhookd.subscriptions.create')
    def post(self):
        subscription = subscription_schema.load(request.json).data
        subscription['uuid'] = str(uuid.uuid4())
        self._service.create(subscription)
        return subscription, 201


class SubscriptionResource(AuthResource):

    def __init__(self, service):
        self._service = service

    @required_acl('webhookd.subscriptions.{subscription_uuid}.read')
    def get(self, subscription_uuid):
        subscription = self._service.get(subscription_uuid)
        return subscription_schema.dump(subscription).data

    @required_acl('webhookd.subscriptions.{subscription_uuid}.update')
    def put(self, subscription_uuid):
        subscription = subscription_schema.load(request.json).data
        subscription = self._service.edit(subscription_uuid, subscription)
        return subscription_schema.dump(subscription).data

    @required_acl('webhookd.subscriptions.{subscription_uuid}.delete')
    def delete(self, subscription_uuid):
        self._service.delete(subscription_uuid)
        return '', 204