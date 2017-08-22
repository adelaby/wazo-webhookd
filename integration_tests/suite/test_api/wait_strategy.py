# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from hamcrest import (
    assert_that,
    has_entries,
)
from xivo_test_helpers import until


class WaitStrategy:

    def wait(self, webhookd):
        raise NotImplementedError()


class NoWaitStrategy(WaitStrategy):

    def wait(self, webhookd):
        pass


class ConnectedWaitStrategy(WaitStrategy):

    def wait(self, webhookd):

        def webhookd_is_connected():
            status = webhookd.status.get()
            assert_that(status['connections'], has_entries({'bus_consumer': 'ok'}))

        until.assert_(webhookd_is_connected, tries=10)
