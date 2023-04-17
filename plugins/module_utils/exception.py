#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


class TroubleShootingError(Exception):
    pass


class TrafficNotAllowedError(TroubleShootingError):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class ValidationError(TroubleShootingError):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class MissingRouteError(TroubleShootingError):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class CidrOverlapeError(TroubleShootingError):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class RouteTableAssociationError(TroubleShootingError):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)
