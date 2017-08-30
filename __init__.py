# -*- coding: utf-8 -*-
from trytond.pool import Pool
from .employee import *
from .report import *

def register():
    Pool.register(
        RrhhCategoria,
        RrhhFamiliares,
        RrhhObrasoc,
        RrhhSindicato,
        RrhhVacaciones,
        RrhhCursos,
        RrhhOfdocu,
        RrhhJustif,
        RrhhHorarios,
        RrhhAsistencia,
        RrhhCv,
        RrhhEvalua,
        RrhhArt,
        RrhhArtevo,
        RrhhPuestos,
        RrhhModdocu,
        RrhhHorariosLegajo,
        RrhhIndumentaria,
        Employee,
        module='rrhh', type_='model')

    Pool.register(
        module='rrhh', type_='wizard')

    Pool.register(
        RrhhReport1,
        RrhhReport2,
        RrhhReport3,
        RrhhReport4,
        RrhhReport5,
        RrhhReport6,
        module='rrhh', type_='report')
