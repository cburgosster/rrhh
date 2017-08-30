# -*- coding: utf-8 -*-
from trytond.report import Report
from trytond.pool import PoolMeta, Pool
from trytond.model import fields, ModelSQL, ModelView, Workflow
from trytond.transaction import Transaction
from datetime import datetime, timedelta, date
from trytond.tools import datetime_strftime
from time import gmtime, strftime, time

__all__ = ['RrhhReport1', 'RrhhReport2','RrhhReport3', 'RrhhReport4', 'RrhhReport5', 'RrhhReport6']
__metaclass__ = PoolMeta

class RrhhReport1(Report):
    'RrhhReport1'
    __name__ = 'rrhh.report1'

    #~ @classmethod
    #~ def parse(cls, report, objects, data, localcontext):
        #~ pool = Pool()
        #~ company = pool.get('company.company')
        #~ party = pool.get('party.party')
        #~ employee = pool.get('company.employee')
        #~ User = pool.get('res.user')
        #~ Translation = pool.get('ir.translation')
        #~ localcontext['fechahora'] = datetime.today()
        #~ localcontext['usuario'] =  lambda: cls.user()
        #~ return super(RrhhReport1, cls).parse(report, objects, data, localcontext)


class RrhhReport2(Report):
    'RrhhReport2'
    __name__ = 'rrhh.report2'

    @classmethod
    def parse(cls, report, objects, data, localcontext):
        pool = Pool()
        User = pool.get('res.user')
        Translation = pool.get('ir.translation')
        localcontext['fechahora'] = datetime.today()
        localcontext['usuario'] = User(Transaction().user).name    
        return super(RrhhReport2, cls).parse(report, objects, data, localcontext)


class RrhhReport3(Report):
    'RrhhReport3'
    __name__ = 'rrhh.report3'

    @classmethod
    def parse(cls, report, objects, data, localcontext):
        pool = Pool()
        User = pool.get('res.user')
        Translation = pool.get('ir.translation')
        localcontext['fechahora'] = datetime.today()
        localcontext['usuario'] = User(Transaction().user).name    
        return super(RrhhReport3, cls).parse(report, objects, data, localcontext)


class RrhhReport4(Report):
    'RrhhReport4'
    __name__ = 'rrhh.report4'

    @classmethod
    def parse(cls, report, objects, data, localcontext):
        pool = Pool()
        User = pool.get('res.user')
        Translation = pool.get('ir.translation')
        localcontext['fechahora'] = datetime.today()
        localcontext['usuario'] = User(Transaction().user).name    
        return super(RrhhReport4, cls).parse(report, objects, data, localcontext)


class RrhhReport5(Report):
    'RrhhReport5'
    __name__ = 'rrhh.report5'

    @classmethod
    def parse(cls, report, objects, data, localcontext):
        pool = Pool()
        User = pool.get('res.user')
        Translation = pool.get('ir.translation')
        localcontext['fechahora'] = datetime.today()
        localcontext['usuario'] = User(Transaction().user).name    
        return super(RrhhReport5, cls).parse(report, objects, data, localcontext)


class RrhhReport6(Report):
    'RrhhReport6'
    __name__ = 'rrhh.report6'

    @classmethod
    def parse(cls, report, objects, data, localcontext):
        pool = Pool()
        User = pool.get('res.user')
        Translation = pool.get('ir.translation')
        localcontext['fechahora'] = datetime.today()
        localcontext['usuario'] = User(Transaction().user).name    
        return super(RrhhReport6, cls).parse(report, objects, data, localcontext)
        
