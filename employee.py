# -*- coding: utf-8 -*-
import urllib
from trytond.model import ModelView, fields, ModelSQL, ModelSingleton, Workflow
from trytond.transaction import Transaction
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval
from dateutil import rrule
from datetime import datetime, timedelta, date, time
from trytond.tools import datetime_strftime
from time import gmtime, strftime, time

#~ import smtplib
#~ from email.mime.multipart import MIMEMultipart  # , MIMEBase
#~ from email.mime.text import MIMEText

__metaclass__ = PoolMeta
__all__ = ["Employee","RrhhFamiliares",'RrhhCategoria','RrhhObrasoc','RrhhAsistencia','RrhhJustif',
        'RrhhSindicato','RrhhCursos','RrhhOfdocu','RrhhVacaciones','RrhhHorarios','RrhhCv','RrhhEvalua',
        'RrhhPuestos','RrhhModdocu','RrhhHorariosLegajo','RrhhIndumentaria','RrhhArt','RrhhArtevo']

STATES = {'readonly': ~Eval('active'), }
DEPENDS = ['active']

class Employee:
    'Employee'
    __name__ = 'company.employee'

    convenio = fields.Char("Convenio",20)
    legajo = fields.Char('Legajo',10)
    
    #~ datos en solapa Personales ***********************************************************
    nombre = fields.Function(fields.Char('Nombres',20), 'get_empleado_nombre')
    apellido = fields.Function(fields.Char('Nombres',20), 'get_empleado_apellido')    
    documents = fields.Function(
        fields.One2Many('party.document', None, 'Documento',
        on_change_with=['party', 'documents']), 'on_change_with_documents')
    photo = fields.Function(fields.Binary('Picture'), 'get_empleado_photo')
    nationality = fields.Many2One('country.country','Nacionalidad', required=True)    
    date_nac = fields.Function(fields.Date('Fecha Nac.'), 'get_empleado_dob')

    #~ --------------- Calculo de edad del empleado  ----------------    
    edad_emple = fields.Function(fields.Char('Edad hoy',7, 
        on_change_with=['date_nac']),"on_change_with_date_age")

    def on_change_with_date_age(self,name=None):
        import datetime
        fecha1=datetime.date.today().year        
        fecha2= self.date_nac.year
        diff =  fecha1 - fecha2 
        years = str(diff)
        return years + ' años'
    #~ -----------------------------------------------------------------------

    cuil = fields.Function(fields.Char('Cuil',15), 'get_empleado_cuil')
    sex = fields.Function(fields.Selection([
        ('m', 'Masculino'),
        ('f', 'Femenino'),
        ], 'Sexo'), 'get_empleado_sex')
    marital_status = fields.Selection([
        (None, ''),
        ('SOLTERO', 'Soltero'),
        ('CASADO', 'Casado'),
        ('CONCUBINO', 'Concubinato'),
        ('VIUDO', 'Viudo'),
        ('DIVORCIADO', 'Divorciado'),
        ('SEPARADO', 'Separado'),
        ], 'Estado Civil',sort=False, required=True)
    matri_prof = fields.Char("Matricula Profesional",20)
    mala_praxi = fields.Char("S/Mala Praxis",10)
    libreta_sani =  fields.Char("Libreta Sanitaria",10)
    curso_mani =  fields.Char("Curso Maniplacion",10)
    hepatitib =  fields.Char("Hepatitis B",5)
    email1 = fields.Char('E-Mail part.')
    email2 = fields.Char('E-Mail ALPI')

    #~ datos en solapa Domicilio *************************************************************
    calle = fields.Char('Calle', states=STATES, depends=DEPENDS)
    altura = fields.Integer('Numero')
    calle2 = fields.Char(' y Calle', states=STATES, depends=DEPENDS)
    piso = fields.Char('Piso', 10)
    departamento = fields.Char('Departamento', 10)
    codpost = fields.Char('Cod.Postal', 10)
    localidad = fields.Char('Localidad', states=STATES, depends=DEPENDS)
    pais = fields.Many2One(
        'country.country', 'Pais', help='Seleccione Pais')
    provincia = fields.Many2One(
        'country.subdivision', 'Provincia',
        domain=[('country', '=', Eval('pais'))],
        depends=['pais'])    
    ciudad = fields.Char('Ciudad',40)
    telefono = fields.Char('Telefono Particular',30)
    celular =  fields.Char('Celular',30)    
    telefcontacto = fields.Char('Telefono Contacto',30)        
    active = fields.Boolean('Active', select=True)
    google_maps_url = fields.Function(fields.Char('Google Maps',
            on_change_with=['calle','calle2','codpost','localidad','pais',
                'provincia']), 'on_change_with_google_maps_url')
    party_addresses = fields.Function(fields.One2Many('party.address', None,
            'Direccion'), 'get_addresses')
        
    def get_addresses(self, name):
        lines = []
        if self.party:
            for line in self.party.addresses:
                    lines.append(line)
        return [x.id for x in lines]

    def on_change_with_google_maps_url(self, name=None):
        lang = Transaction().language[:2]
        url = ''
        for value in (
                self.calle,
                self.calle2bis,
                self.codpost,
                self.localidad,
                self.pais.name if self.pais else None,
                self.provincia.name if self.provincia else None,
                ):
            if value:
                if isinstance(value, str):
                    url += ' ' + value.decode('utf-8')
                else:
                    url += ' ' + value
        if url.strip():
            return 'http://maps.google.com/maps?hl=%s&q=%s' % \
                (lang, urllib.quote(url.strip().encode('utf-8')))
        return ''

    #~ datos en solapa Laborales *************************************************************
    edificio = fields.Many2One('gnuhealth.hospital.building', 'Edificio')
    contrato = fields.Selection([
        ('EVENTUAL', 'Eventual'),
        ('TEMPORAL', 'Temporal'),
        ('INDETERMINADO', 'Indeterminado'),
        ('PASANTIA', 'Pasantia'),        
        ], 'Tipo Contrato', sort=False, required=True)        
    date_in = fields.Date('Fecha Ingreso', required=True)
    date_in_rec = fields.Date('Fecha Ingreso Recibo')
    date_eg = fields.Date('Fecha Egreso')
    motivo_eg = fields.Char('Motivo Egreso',40)
    date_pr = fields.Date('Fecha Preaviso')
    certi_serv = fields.Boolean('Certif.Serv.', select=False)    
    fecha_certi_serv = fields.Date('Fecha Entrega Certif.')
    ret_certi_serv = fields.Boolean('Retiro Certifi. Serv.', select=False)    
    cs_photo1 = fields.Binary('Imagen1', states = STATES)    
    
    #~ --------------- 90 dias de la Fecha de Ingreso ---------------
    date_prueba = fields.Function(fields.Date('Fin Periodo Prueba',
            on_change_with=['date_in']),"on_change_with_date_prueba")

    def on_change_with_date_prueba(self, name=None):
        prueba  = datetime.now().date()
        if self.date_in:
            prueba = self.date_in + timedelta(days=90)
        return prueba
     #~ -------------------------------------------------------------------
 
    #~ datos en solapa Agrupacion ************************************************************
    ccosto = fields.Many2One('gnuhealth.hospital.building', 'Edificio')
    categoria = fields.Many2One('rrhh.categoria', 'Categoria')
    puesto = fields.Many2One('rrhh.puestos', 'Puesto')    
    convenio = fields.Selection([
        ('SANIDAD', 'Convenio Sanidad'),
        ('COMERCIO', 'Convenio de Comercio'),
        ('GASTRONOMICO', 'Convenio Gastronomico'),
        (None, ''),        
        ], 'Convenio', sort=False, required=True)
    sueldo = fields.Numeric('Sueldo', digits=(10,2))
    tliqui = fields.Selection([
        ('M', 'Mensual'),
        ('Q', 'Quincena'),
        ], 'Tipo Liquidacion', sort=False, required=True)
    horariosleg =  fields.One2Many('rrhh.horarioslegajo','name','Horario')
         
    #~ datos en solapa Cobertura *************************************************************
    tipojub = fields.Selection([
        (None, ''),
        ('SIPA Ley 26425', 'Sipa Ley 26425'),
        ('JUBILADO', 'Jubilado'),
        ('SIN DECLARAR', 'Sin Declarar'),
        ], 'Tipo Jubilacion', sort=False, required=True)
    cuil = fields.Function(fields.Char('Cuil'), 'get_empleado_cuil')

    obrasoci = fields.One2Many('rrhh.obrasoc', 'name','Cobertura')
    sindicato = fields.One2Many('rrhh.sindicato', 'name','Sindicato')
    
    #~ datos en solapa Forma de Pago ********************************************************
    formapago = fields.Selection([
        ('CAJA AHORRO', 'Cja de Ahorro'),
        ('CHEQUE', 'Cheque'),
        ('EFECTIVO', 'Efectivo'),
        ('SIN DETERMINAR', 'Sin determinar'),        
        ], 'Forma de Pago', sort=False, required=True)
    bank = fields.Many2One('account.bank', 'Banco', required=False)
    bank_suc = fields.Char('Sucursal',20)
    bank_caja = fields.Char('Nro. Caja de Ahorro',20)
    bank2 = fields.Many2One('account.bank', 'Banco', required=False)
    bank_suc2 = fields.Char('Sucursal',20)
    bank_caja2 = fields.Char('Nro. Caja de Ahorro',20)    
    bank3 = fields.Many2One('account.bank', 'Banco', required=False)
    bank_suc3 = fields.Char('Sucursal',20)
    bank_caja3 = fields.Char('Nro. Caja de Ahorro',20)
    
        #~ datos en solapa Indumentaria *****************************************************
    Indumentar = fields.One2Many('rrhh.indumentaria', 'name','Indumentaria')
    
    #~ datos en solapa Familiares ************************************************************
    familiar = fields.One2Many('rrhh.familiares', 'name','Familiares')
            
    #~ datos en solapa Vacaciones ***********************************************************
    dias_equi = fields.Function(fields.Char('Dias Vacaciones/Proporcionales',10),'get_dlaboral')
    dias_antig = fields.Function(fields.Char('Antiguedad'),'get_antiguedad')
    curvac = fields.One2Many('rrhh.vacaciones', 'name','Vacaciones')

    def get_dlaboral(self, name=None):
        from dateutil.relativedelta import relativedelta
        import datetime
        dingr=self.date_in
        today = datetime.date.today()
        dhoy=datetime.date(year=today.year , month=12, day=31)
        delta = relativedelta(dhoy, dingr)
        totalanos = delta.years
        totaldias = delta.days
        totalvaca = 0
        if totalvaca < 1:
            vardias = dhoy - dingr
            candias = vardias.days
            if candias <= 180:
                totaldias = int(round(candias/20))
            else:
                totaldias = 14
        if totalvaca >= 1 and totalvaca <= 5:
            totaldias = 14
        if totalvaca >5  and totalvaca <= 10:
            totaldias = 21
        if totalvaca >10  and totalvaca <=20 :
            totaldias = 28
        if totalvaca>20:
            totaldias = 35
        return str(totaldias) + ' Dia(s)'

    def get_antiguedad(self, name=None):
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        import datetime
        dingr=self.date_in
        dhoy=datetime.date.today()
        delta = relativedelta(dhoy, dingr)
        years_months_days = str(delta.years) + ' Año(s) ' \
                + str(delta.months) + ' Mes(es) ' \
                + str(delta.days) + ' Dia(s)'
        return years_months_days

    #~ datos en solapa Cursos y Capacitacion ***********************************************
    curcap = fields.One2Many('rrhh.cursos', 'name','Cursos')
    photo1 = fields.Binary('Imagen1', states = STATES)
    photo2 = fields.Binary('Imagen2', states = STATES)
    photo3 = fields.Binary('Imagen3', states = STATES)
    photo4 = fields.Binary('Imagen4', states = STATES)

    #~ datos en solapa Oficio y C.Documento ************************************************
    ofdocu = fields.One2Many('rrhh.ofdocu', 'name','Oficios')
    
    @staticmethod
    def default_active():
        return True

    def on_change_with_documents(self, name=None):
        if self.party:
            return [d.id for d in self.party.documents]
        return None

    def get_empleado_legajo(self, name):
        return self.party.vat_number
        
    def get_empleado_nombre(self, name):
        return self.party.name

    def get_empleado_apellido(self, name):
        return self.party.lastname
        
    def get_empleado_sex(self, name):
        return self.party.sex

    def get_empleado_dob(self, name):
        return self.party.dob

    def get_empleado_cuil(self, name):
        return self.party.vat_number

    def get_mechanism(self, name):
        for mechanism in self.party.contact_mechanisms:
            if mechanism.type == name:
                return mechanism.value
        return ''

    def get_patient_sex(self, name):
        return self.name.sex
        
    def get_empleado_photo(self,party):
        return self.party.photo 

    def on_change_with_google_maps_url(self, name=None):
        lang = Transaction().language[:2]
        url = ''
        for value in (
                self.calle,
                self.altura,
                self.codpost,
                self.localidad,
                self.pais.name if self.pais else None,
                self.provincia.name if self.provincia else None,
                ):
            if value:
                if isinstance(value, str):
                    url += ' ' + value.decode('utf-8')
                else:
                    url += ' ' + value
        if url.strip():
            return 'http://maps.google.com/maps?hl=%s&q=%s' % \
                (lang, urllib.quote(url.strip().encode('utf-8')))
        return ''               


class RrhhIndumentaria(ModelSQL, ModelView):
    'Indumentaria'
    __name__ = 'rrhh.indumentaria'
    
    name = fields.Many2One('company.employee', 'Empleado', required=True)
    tarje_magne = fields.Char('Tarjeta Magnetica',25)
    tarje_alpimas = fields.Char('Tarjeta ALPI Mas',10)
    calzado = fields.Char('Numero Calzado', 3)
    camisa = fields.Char('Talle Camisa', 3)
    pantalon = fields.Char('Talle Pantalon', 3)
    remera = fields.Char('Talle Remera', 3)
    delantal = fields.Char('Talle Delantal', 3)
    chaleco = fields.Char('Talle Chaleco', 3)
    faja = fields.Char('Faja',3)
            

class RrhhFamiliares(ModelSQL, ModelView):
    'Familiares'
    __name__ = 'rrhh.familiares'
    
    name = fields.Many2One('company.employee', 'Empleado', required=True)
    name1 = fields.Char('Apellido',15)
    name2 = fields.Char('Nombre',25)
    parentezco = fields.Selection([
        ('ESPOSA', 'Esposa/o'), 
        ('CONCUBINA', 'Concubina/o'),
        ('HIJO', 'Hijo'),
        ('PADRE', 'Padre'),        
        ('MADRE', 'Madre')],
        'Parentesco', sort=False, required=False)
    sexo = fields.Selection([
        ('MASCULINO', 'Masculino'), ('FEMENINO', 'Femenino')],
        'Sexo Biologico', sort=False, required=False)
    tdoc = fields.Selection([
        ('DNI' ,'DNI'),('PAS', 'Pasaporte')], 
        'Documento', sort=False, required=False)
    ndoc = fields.Char('NumDoc',10)
    falta = fields.Date('FechaAlta')    
    fbaja = fields.Date('FechaBaja')        
    fnac = fields.Date('FechaNac.')        
    telefono = fields.Char('Telefono',30)
          
        
class RrhhCategoria(ModelSQL, ModelView):
    'Categoria'
    __name__ = 'rrhh.categoria'
    _rec_name = 'categoria'

    cod_ca = fields.Char('Codigo',help='Codigo Categoria', size=10, required=False)
    categoria = fields.Char('Categorias', help='Descripcion de Categorias', size=40, required=True)
    
    
class RrhhPuestos(ModelSQL, ModelView):
    'Puestos'
    __name__ = 'rrhh.puestos'
    _rec_name = 'puesto'

    cod_pu = fields.Char('Codigo',help='Codigo Puesto', size=10, required=False)
    puesto = fields.Char('Puesto', help='Descripcion de Puesto', size=40, required=True)
    
    
class RrhhModdocu(ModelSQL, ModelView):
    'Documentos'
    __name__ = 'rrhh.moddocu'
    _rec_name = 'des_docu'

    cod_doc = fields.Char('Codigo',help='Codigo Documento', size=10, required=False)
    des_doc = fields.Text('Descripcion')
    

class RrhhHorarios(ModelSQL, ModelView):
    'Horarios'
    __name__ = 'rrhh.horarios'

    #~ name = fields.Many2One('company.employee', 'Empleado', required=True)
    cod_hor = fields.Char('Codigo',help='Codigo Horario', size=10, required=False)
    des_hor = fields.Char('Descripcion', help='Descripcion del Horario', size=40, required=False)
    tip_tur = fields.Selection([
        ('Dia' ,'Dia'),('Tarde', 'Tarde'),('Noche', 'Noche'),('Mixto', 'Mixto')], 
        'Turno', sort=False, required=False)
    entrada = fields.Time('Hor.Entrada')
    salida = fields.Time('Hor.Salida')


class RrhhHorariosLegajo(ModelSQL, ModelView):
    'Horarios de Empleados'
    __name__ = 'rrhh.horarioslegajo'

    name = fields.Many2One('company.employee', 'Empleado', required=True)
    #~ cod_hor = fields.Char('Codigo',help='Codigo Horario', size=10, required=False)
    #~ des_hor = fields.Char('Descripcion', help='Descripcion del Horario', size=20, required=False)    
    fecha_horario = fields.Date('Fecha Actualizacion')
    tip_tur = fields.Selection([
        ('Dia' ,'Dia'),('Tarde', 'Tarde'),('Noche', 'Noche'),('Mixto', 'Mixto')], 
        'Turno', sort=False, required=False)
    entrada = fields.Time('Entrada')
    salida = fields.Time('Salida')

    def get_horario_des(self, name):
        return self.horario.des_hor
    
    def get_horario_turno(self, name):
        return self.horario.tip_tur

    def get_horario_entrada(self, name):
        return self.horario.entrada
        
    def get_horario_salida(self, name):
        return self.horario.salida
                
        
class RrhhJustif(ModelSQL, ModelView):
    'Justificaciones'
    __name__ = 'rrhh.justif'
    _rec_name = 'descripcion'

    descripcion = fields.Char('Concepto', help='Descripcion de la Justificacion', size=50, required=True)    


class RrhhAsistencia(ModelSQL, ModelView):
    'Asistencias'
    __name__ = 'rrhh.asistencia'

    #~ legajo = fields.Many2One('company.employee', 'Empleado', required=True)
    name = fields.Many2One('company.employee', 'Empleado', required=True)
    modaviso = fields.Selection([
        ('JEFE SECTOR' ,'Jefe Sector'),
        ('SUPERVISOR', 'Supervisor'),
        ('PERSONAL' ,'Personal'),
        ('TELEFONICO', 'Telefonico'),
        ('MAIL', 'Mail')], 
        'Modo de Aviso', sort=False, required=False)
    tipo = fields.Selection([
        ('MENSUAL' ,'Mensual'),('TECNICO', 'Tecnico'),('FUERA CONVENIO', 'Fuera Convenio')], 
        'Tipo', sort=False, required=False)
    descripcion = fields.Many2One('rrhh.justif',
            'Concepto', required=True)
    fecha_aviso = fields.Date('Fecha de Aviso')
    fecha_desde = fields.Date('Justificado Desde')     
    fecha_hasta = fields.Date('Justificado Hasta')        
    dias = fields.Integer('Dias')
    justif_s = fields.Boolean('Justifica')
    fecha_justif = fields.Date('Fecha Pres.  Justificacion')    
    justif_n = fields.Boolean('Se Descuenta')
    observaciones = fields.Text('Observaciones')
    justif_photo1 = fields.Binary('Imagen1', states = STATES)
    justif_photo2 = fields.Binary('Imagen2', states = STATES)
    justif_photo3 = fields.Binary('Imagen3', states = STATES)    


class RrhhCv(ModelSQL, ModelView):
    'Curriculum Vitae'
    __name__ = 'rrhh.cv'

    estado_cv = fields.Selection([
        ('CITADO', 'Citado'),
        ('ANULADO', 'Anulado'),
        ('PENDIENTE', 'Pendiente'),        
        (None, ''),        
        ], 'Estado CV', sort=False, required=True)
    nombre = fields.Char('Apellido y Nombre',40)    
    photo1 = fields.Binary('Foto', states = STATES)
    fecha_presen = fields.Date('Fecha de Presentacion')
    fecha_nac = fields.Date('Fecha Nac.')
    cuil = fields.Char('Cuil',13)
    telefono = fields.Char('Telefono',30)
    celular = fields.Char('Celular',20)    
     
    direccion = fields.Char('Calle',20)
    altura = fields.Char('Altura',10)
    piso = fields.Char('Piso',5)
    dto = fields.Char('Dto.',5)
    entrecalle = fields.Char('Entre Calle',20)
    localidad = fields.Char('Localidad',20)
    
    ccosto = fields.Many2One('gnuhealth.hospital.building', 'Edificio')
    categoria = fields.Many2One('rrhh.categoria', 'Categoria')    
    convenio = fields.Selection([
        ('SI', 'Si'),
        ('NO', 'No'),
        ], 'Convenio', sort=False, required=True)
    sueldo = fields.Numeric('Sueldo', digits=(10,2))
    tliqui = fields.Selection([
        ('M', 'Mensual'),
        ('Q', 'Quincena'),
        ], 'Tipo Liquidacion', sort=False, required=True)
    tip_tur = fields.Selection([
        ('Dia' ,'Dia'),('Tarde', 'Tarde'),('Noche', 'Noche'),('Mixto', 'Mixto')], 
        'Turno', sort=False, required=False)
    entrada = fields.Time('Hor.Entrada')
    salida = fields.Time('Hor.Salida')
    observaciones = fields.Text('Observaciones')
    evaluacion = fields.Text('Evaluacion')
    otros = fields.Text('Otros')
    cv_photo1 = fields.Binary('Imagen1', states = STATES)
    cv_photo2 = fields.Binary('Imagen2', states = STATES)
    cv_photo3 = fields.Binary('Imagen3', states = STATES)
    email = fields.Char('E-Mail',40)
    #~ --------------- Calculo de edad del empleado  ----------------    
    edad_emple = fields.Function(fields.Char('Edad de Postulante',7, 
        on_change_with=['date_nac']),"on_change_with_date_agecv")

    def on_change_with_date_agecv(self,name=None):
        import datetime
        fecha_1=datetime.date.today().year        
        fecha_2= self.date_nac.year
        diff =  fecha_1 - fecha_2 
        years = str(diff)
        return years + ' años'
    #~ -----------------------------------------------------------------------    


class RrhhEvalua(ModelSQL, ModelView):
    'Evaluacion Desempeno'
    __name__ = 'rrhh.evalua'

    name = fields.Many2One('company.employee', 'Empleado', required=True)
    

class RrhhArt(ModelSQL, ModelView):
    'Seguro Art'
    __name__ = 'rrhh.art'

    name = fields.Many2One('company.employee', 'Empleado', required=True)
    siniestro = fields.Char('Numero Siniestro',size=15, required=True)
    fechaacc = fields.DateTime('Fecha/Hora Accidente', required=True)
    fechaalta = fields.DateTime('Fecha /Hora de Alta')    
    informo = fields.Char('Quien Informo',size=30, required=False)
    telefalter = fields.Char('Telefono Alternativo',30)
    testigo1 = fields.Char('Testigo 1',size=20, required=False)    
    testigo2 = fields.Char('Testigo 2',size=20, required=False)        
    tipoacc = fields.Selection([
        ('Accidente Trabajo', 'Accidente Trabajo'),
        ('Acc In Itinere', 'Acc In Itinere')],
        'Tipo Accidente', sort=False, required=True)
    hospital = fields.Char('Primera Atencion',40)
    refacc = fields.Text('Descrip Accidente', size=100)
    causa = fields.Text('Causas Accidente', size=100)
    medida = fields.Text('Medidas Corrrectivas', size=100)
    observ = fields.Text('Observacion', size=100)
    seguroart_photo1 = fields.Binary('Imagen1')
    seguroart_photo2 = fields.Binary('Imagen2')
    seguroart_photo3 = fields.Binary('Imagen3')    
    dias_acc = fields.Function(fields.Char('Dias Ausente por Accidente',10),'get_dlasacc')
    legajo = fields.Function(fields.Char('Legajo',10), 'get_emple_legajo')
    ingreso = fields.Function(fields.Date('Fecha Ingreso'),'get_emple_ingreso')
    nacimie = fields.Function(fields.Date('Fecha Nac.'), 'get_emple_dob')
    evolucion = fields.One2Many('rrhh.artevo', 'name','Evolucion')

    def get_emple_legajo(self, name):
        return self.name.legajo

    def get_emple_ingreso(self,name):
        return self.name.date_in
        
    def get_emple_dob(self,party):
        return self.party.dob        

    def get_dlasacc(self, name=None):
        from datetime import datetime
        accini=self.fechaacc
        #~ *** Si no tuviera fecha alta, tomar la fecha del dia como alta ***
        #~ *** esto es para determinar los dias de accidente **************
        if self.fechaalta == "":
            accfin=datetime.now()
        else:
            accfin=self.fechaalta
         #~ *******************************************************************
        vardias = accfin - accini
        candias = vardias.days
        totaldias = int(round(candias))
        return str(totaldias) + ' Dia(s)'


class RrhhArtevo(ModelSQL, ModelView):
    'RrhhArtevo'
    __name__ = 'rrhh.artevo'
    
    name = fields.Many2One('rrhh.art', 'Empleado', required=True)
    fcontrol = fields.DateTime('Fecha/Hora Control', required=False)
    cmedico = fields.Char('Centro Medico',25)
    especialidad = fields.Char('Especialidad',25)
    medico = fields.Char('Medico',25)
    reposo = fields.Numeric('Ds Reposo', digits=(3,0))


class RrhhObrasoc(ModelSQL, ModelView):
    'ObraSocial'
    __name__ = 'rrhh.obrasoc'

    name = fields.Many2One('company.employee', 'Empleado', required=True)
    cod_ob = fields.Char('Codigo / Nomenclatura',help='Codigo Obra Social ante AFIP', size=10, required=True)
    descripcion = fields.Char('descripcion', size=50, readonly=False, select=True)    

    
class RrhhSindicato(ModelSQL, ModelView):
    'Sindicato'
    __name__ = 'rrhh.sindicato'

    name = fields.Many2One('company.employee', 'Empleado', required=True)
    cod_si = fields.Char('Codigo / Nomenclatura',help='Codigo Sindicato', size=10, required=True)
    descripcion = fields.Char('descripcion', size=50, readonly=False, select=True)    


class RrhhCursos(ModelSQL, ModelView):
    'Cursos y Capacitacion'
    __name__ = 'rrhh.cursos'
   
    name = fields.Many2One('company.employee', 'Empleado', required=True)
    tcurso = fields.Selection([
        ('CURSO', 'Curso'), 
        ('CAPACITACION', 'Capacitacion'),
        ('CONCIENTIZACION','Concientizacion')],
        'Tipo', sort=False, required=False)
    ncurso = fields.Char('Descripcion',30)
    name2 = fields.Char('Nombre',25)
    fini = fields.Date('Fecha Inicio')
    ffin = fields.Date('Fecha Fin')
    jus = fields.Selection([
        ('SI', 'Si'), ('NO', 'No')],
        'Justifica', sort=False, required=False)
    dias = fields.Integer('Dias')
    jusdes = fields.Char('Descripcion',25)
    ncertif = fields.Char('Certificado',25)
    notas = fields.Text('Observaciones')


class RrhhOfdocu(ModelSQL, ModelView):
    'Oficios y C.Documentos'
    __name__ = 'rrhh.ofdocu'
    
    name = fields.Many2One('company.employee', 'Empleado', required=True)
    fecha = fields.Date('Fecha')
    toficio = fields.Selection([
        ('TELEGRAMA', 'Telegrama'),
        ('CARTA DOCUMENTO', 'Carta Documento')],
        'Tipo Oficio', sort=False, required=False)
    observ = fields.Char('Observacion',100)
    texto = fields.Text('Contenido')

    
class RrhhVacaciones(ModelSQL, ModelView):
    'Vacaciones'
    __name__ = 'rrhh.vacaciones'
    
    name = fields.Many2One('company.employee', 'Empleado', required=True)
    vano = fields.Numeric('Anio', digits=(4,0))
    vinicio = fields.Date('Fecha Inicio')
    vfin = fields.Date('Fecha Fin')
    vretoma = fields.Date('Retoma')
    vdias = fields.Numeric('Dias', digits=(2,0))
    vplus = fields.Numeric('Plus Vac', digits=(2,0))
    vcredito = fields.Numeric('Dias Credito', digits=(2,0))

   
def diasLaborales(fechaInicio, fechaFin, festivos=0, vacaciones=None):
    #~ >>> diasLaborales(datetime.date(2004, 9, 1), datetime.date(2004, 11, 14), 2)
    #~ 51
    #~ >>> diasLaborales(datetime.date(2011,1,11), datetime.date(2011, 11, 25),5)
    #~ 224
    if vacaciones is None:
        vacaciones= 5, 6         # si no tienes vacaciones no trabajas sab y dom
    laborales = [dia for dia in range(7) if dia not in vacaciones]
    totalDias= rrule.rrule(rrule.DAILY, dtstart=fechaInicio, until=fechaFin,byweekday=laborales)
    return totalDias.count() - festivos
