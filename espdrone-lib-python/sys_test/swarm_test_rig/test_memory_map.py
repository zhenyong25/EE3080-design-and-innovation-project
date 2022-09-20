# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2019 Bitcraze AB
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
import time
import unittest

import edlib.crtp
from edlib.espdrone import Espdrone
from edlib.espdrone.log import LogConfig
from edlib.espdrone.mem import MemoryElement
from edlib.espdrone.swarm import CachededFactory
from edlib.espdrone.swarm import Swarm
from edlib.espdrone.syncEspdrone import SyncEspdrone
from edlib.espdrone.syncLogger import SyncLogger
from sys_test.swarm_test_rig.rig_support import RigSupport


class TestMemoryMapping(unittest.TestCase):
    def setUp(self):
        edlib.crtp.init_drivers(enable_debug_driver=False)
        self.test_rig_support = RigSupport()

    def test_memory_mapping_with_one_ed(self):
        # Fixture
        uri = self.test_rig_support.all_uris[0]
        self.test_rig_support.restart_devices([uri])
        ed = Espdrone(rw_cache='./cache')

        # Test and Assert
        with SyncEspdrone(uri, ed=ed) as sed:
            self.assert_memory_mapping(sed)

    def test_memory_mapping_with_all_eds(self):
        # Fixture
        uris = self.test_rig_support.all_uris
        self.test_rig_support.restart_devices(uris)
        factory = CachededFactory(rw_cache='./cache')

        # Test and Assert
        with Swarm(uris, factory=factory) as swarm:
            swarm.parallel_safe(self.assert_memory_mapping)

    def test_memory_mapping_with_reuse_of_ed_object(self):
        # Fixture
        uri = self.test_rig_support.all_uris[0]
        self.test_rig_support.restart_devices([uri])
        ed = Espdrone(rw_cache='./cache')

        # Test and Assert
        for connections in range(10):
            with SyncEspdrone(uri, ed=ed) as sed:
                for mem_ops in range(5):
                    self.assert_memory_mapping(sed)

    # Utils

    def assert_memory_mapping(self, sed):
        mems = sed.ed.mem.get_mems(MemoryElement.TYPE_MEMORY_TESTER)
        count = len(mems)
        self.assertEqual(1, count, 'unexpected number of memories found')

        self.verify_reading_memory_data(mems)
        self.verify_writing_memory_data(mems, sed)

    def verify_writing_memory_data(self, mems, sed):
        self.wrote_data = False
        sed.ed.param.set_value('memTst.resetW', '1')
        time.sleep(0.1)
        mems[0].write_data(5, 1000, self._data_written)
        while not self.wrote_data:
            time.sleep(1)
        log_conf = LogConfig(name='memtester', period_in_ms=100)
        log_conf.add_variable('memTst.errCntW', 'uint32_t')
        with SyncLogger(sed, log_conf) as logger:
            for log_entry in logger:
                errorCount = log_entry[1]['memTst.errCntW']
                self.assertEqual(0, errorCount)
                break

    def verify_reading_memory_data(self, mems):
        self.got_data = False
        mems[0].read_data(5, 1000, self._data_read)
        while not self.got_data:
            time.sleep(1)

    def _data_read(self, mem):
        self.got_data = True

    def _data_written(self, mem, address):
        self.wrote_data = True
