# This file is adapted from https://git.corp.adobe.com/euclid/python-project-scaffold

import pyessentials.log as base

root_logger = base.root_logger
logger : base.Logger = root_logger.sub_logger('SurrealCollage')
Channel = base.Channel
ScopedLog = base.ScopedLog
