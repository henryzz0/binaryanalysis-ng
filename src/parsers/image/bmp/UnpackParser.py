# Binary Analysis Next Generation (BANG!)
#
# This file is part of BANG.
#
# BANG is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License, version 3,
# as published by the Free Software Foundation.
#
# BANG is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License, version 3, along with BANG.  If not, see
# <http://www.gnu.org/licenses/>
#
# Copyright Armijn Hemel
# Licensed under the terms of the GNU Affero General Public License
# version 3
# SPDX-License-Identifier: AGPL-3.0-only


import os
from UnpackParser import WrappedUnpackParser
from bangmedia import unpack_bmp

from UnpackParser import UnpackParser, check_condition
from UnpackParserException import UnpackParserException
from kaitaistruct import ValidationNotEqualError
from . import bmp


#class BmpUnpackParser(UnpackParser):
class BmpUnpackParser(WrappedUnpackParser):
    extensions = []
    signatures = [
        (0, b'BM')
    ]
    pretty_name = 'bmp'

    def unpack_function(self, fileresult, scan_environment, offset, unpack_dir):
        return unpack_bmp(fileresult, scan_environment, offset, unpack_dir)

    def parse(self):
        self.chunknames = set()
        try:
            self.data = bmp.Bmp.from_io(self.infile)
        except (Exception, ValidationNotEqualError) as e:
            raise UnpackParserException(e.args)

    def calculate_unpacked_size(self):
        self.unpacked_size = self.data.file_hdr.len_file

    def set_metadata_and_labels(self):
        """sets metadata and labels for the unpackresults"""
        labels = [ 'bmp', 'graphics' ]
        metadata = {}

        self.unpack_results.set_metadata(metadata)
        self.unpack_results.set_labels(labels)
