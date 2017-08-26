# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Accaccountslog(models.Model):
    vouchermasterid = models.BigIntegerField(blank=True, null=True)
    process = models.CharField(max_length=30, blank=True, null=True)
    empcode = models.CharField(max_length=20, blank=True, null=True)
    ipaddress = models.GenericIPAddressField(blank=True, null=True)
    crdate = models.DateTimeField(blank=True, null=True)
    total = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accAccountsLog'


class Acccompanymaster(models.Model):
    companyid = models.BigAutoField(primary_key=True)
    companycode = models.CharField(max_length=10)
    companyname = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    address3 = models.CharField(max_length=100)
    pin = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'accCompanyMaster'


class Accdefaultaccount(models.Model):
    accountname = models.CharField(primary_key=True, max_length=50)
    accountid = models.ForeignKey('Accgroupandledger', models.DO_NOTHING, db_column='accountid', blank=True, null=True)
    companyid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accDefaultAccount'


class Accdefaultcompanyothermodule(models.Model):
    modulename = models.CharField(primary_key=True, max_length=30)
    companyid = models.ForeignKey(Acccompanymaster, models.DO_NOTHING, db_column='companyid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accDefaultCompanyOtherModule'


class Accdefaultfinancialyear(models.Model):
    companyid = models.ForeignKey(Acccompanymaster, models.DO_NOTHING, db_column='companyid')
    defaultfinancialyear = models.CharField(max_length=9)
    fromdate = models.DateField(blank=True, null=True)
    todate = models.DateField(blank=True, null=True)
    default = models.NullBooleanField()
    finalized = models.NullBooleanField()
    balancesheetdate = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accDefaultFinancialYear'
        unique_together = (('companyid', 'defaultfinancialyear'),)


class Accfeeaccountlink(models.Model):
    referenceid = models.BigIntegerField()
    courseid = models.BigIntegerField()
    feesubtypeid = models.BigIntegerField()
    accountid = models.BigIntegerField()
    companyid = models.ForeignKey(Acccompanymaster, models.DO_NOTHING, db_column='companyid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accFeeAccountLink'


class Accgeneralpost(models.Model):
    postdate = models.DateField(blank=True, null=True)
    staffid = models.BigIntegerField(blank=True, null=True)
    timeofpost = models.DateTimeField(blank=True, null=True)
    ipaddress = models.CharField(max_length=15, blank=True, null=True)
    vouchermasterid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accGeneralPost'


class Accgroupandledger(models.Model):
    accountid = models.BigAutoField(primary_key=True)
    accountname = models.CharField(max_length=100)
    parentid = models.BigIntegerField()
    level = models.BigIntegerField()
    grouporledger = models.CharField(max_length=1)
    currentopeningbalance = models.DecimalField(max_digits=65535, decimal_places=65535)
    currentbalancetype = models.CharField(max_length=2)
    companyid = models.BigIntegerField()
    editable = models.NullBooleanField()
    leveltype = models.CharField(max_length=60, blank=True, null=True)
    displayorder = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accGroupAndLedger'
        unique_together = (('accountname', 'accountid'),)


class Acclastvouchernumber(models.Model):
    vouchertypeid = models.BigIntegerField()
    lastvoucherno = models.BigIntegerField()
    finacialyear = models.BigIntegerField()
    companyid = models.ForeignKey(Acccompanymaster, models.DO_NOTHING, db_column='companyid')

    class Meta:
        managed = False
        db_table = 'accLastVoucherNumber'
        unique_together = (('vouchertypeid', 'finacialyear', 'companyid'),)


class Accopeningbalance(models.Model):
    companyid = models.ForeignKey(Acccompanymaster, models.DO_NOTHING, db_column='companyid')
    accountid = models.BigIntegerField()
    financialyear = models.CharField(max_length=9)
    openingbalance = models.DecimalField(max_digits=65535, decimal_places=65535)
    openingbalancetype = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'accOpeningBalance'
        unique_together = (('accountid', 'financialyear'),)


class Accpettycashdetails(models.Model):
    pettycashid = models.BigAutoField(primary_key=True)
    accountid = models.ForeignKey(Accgroupandledger, models.DO_NOTHING, db_column='accountid', blank=True, null=True)
    amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    pettycashnumber = models.ForeignKey('Accpettycashdetailsmaster', models.DO_NOTHING, db_column='pettycashnumber', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accPettyCashDetails'


class Accpettycashdetailsmaster(models.Model):
    pettycashno = models.BigIntegerField(primary_key=True)
    amountto = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    desc = models.CharField(max_length=100, blank=True, null=True)
    posted = models.BigIntegerField(blank=True, null=True)
    editable = models.BigIntegerField(blank=True, null=True)
    cancelled = models.BigIntegerField(blank=True, null=True)
    pettycashtype = models.CharField(max_length=20, blank=True, null=True)
    pettycashdisplaynumber = models.BigIntegerField(blank=True, null=True)
    financialyear = models.CharField(max_length=-1)

    class Meta:
        managed = False
        db_table = 'accPettyCashDetailsMaster'


class Accpettycashmaster(models.Model):
    pettycashmasterid = models.BigAutoField(primary_key=True)
    dateofposting = models.DateField(blank=True, null=True)
    vouchermasterid = models.ForeignKey('Accvouchermaster', models.DO_NOTHING, db_column='vouchermasterid', blank=True, null=True)
    bankvouchermasterid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accPettyCashMaster'


class Accpostpettycash(models.Model):
    pettycashmasterid = models.ForeignKey(Accpettycashmaster, models.DO_NOTHING, db_column='pettycashmasterid')
    pettycashid = models.ForeignKey(Accpettycashdetails, models.DO_NOTHING, db_column='pettycashid')

    class Meta:
        managed = False
        db_table = 'accPostPettyCash'
        unique_together = (('pettycashmasterid', 'pettycashid'),)


class Acctransactiontype(models.Model):
    referenceid = models.BigIntegerField(primary_key=True)
    transactionname = models.CharField(max_length=30)
    companyid = models.ForeignKey(Acccompanymaster, models.DO_NOTHING, db_column='companyid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accTransactionType'


class Accvoucherdetails(models.Model):
    voucherid = models.BigAutoField(primary_key=True)
    accountid = models.ForeignKey(Accgroupandledger, models.DO_NOTHING, db_column='accountid')
    debitamount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    creditamount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    amounttype = models.CharField(max_length=5)
    narration = models.CharField(max_length=250, blank=True, null=True)
    chequeno = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    bankorbranch = models.CharField(max_length=30, blank=True, null=True)
    vouchermasterid = models.ForeignKey('Accvouchermaster', models.DO_NOTHING, db_column='vouchermasterid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accVoucherDetails'


class Accvoucherdetailsdupli(models.Model):
    voucherid = models.BigIntegerField()
    accountid = models.BigIntegerField()
    debitamount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    creditamount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    amounttype = models.CharField(max_length=5)
    narration = models.CharField(max_length=250, blank=True, null=True)
    chequeno = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    bankorbranch = models.CharField(max_length=30, blank=True, null=True)
    vouchermasterid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accVoucherDetailsDupli'


class Accvouchermaster(models.Model):
    vouchertypeid = models.ForeignKey('Accvouchertype', models.DO_NOTHING, db_column='vouchertypeid')
    vouchernumber = models.BigIntegerField()
    voucherdate = models.DateField()
    referenceid = models.ForeignKey(Acctransactiontype, models.DO_NOTHING, db_column='referenceid', blank=True, null=True)
    refno = models.CharField(max_length=20, blank=True, null=True)
    financialyear = models.BigIntegerField()
    companyid = models.BigIntegerField()
    vouchermasterid = models.BigAutoField(primary_key=True)
    poststatus = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accVoucherMaster'


class Accvouchermasterdupli(models.Model):
    vouchertypeid = models.BigIntegerField()
    vouchernumber = models.BigIntegerField()
    voucherdate = models.DateField()
    referenceid = models.BigIntegerField(blank=True, null=True)
    refno = models.CharField(max_length=20, blank=True, null=True)
    financialyear = models.BigIntegerField()
    companyid = models.BigIntegerField()
    vouchermasterid = models.BigIntegerField()
    poststatus = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accVoucherMasterDupli'


class Accvouchertype(models.Model):
    vouchertypeid = models.BigAutoField(primary_key=True)
    vouchercode = models.CharField(max_length=10)
    vouchername = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'accVoucherType'


class Acdadmissiontype(models.Model):
    admissiontypeid = models.BigIntegerField(primary_key=True)
    admissiontypedesc = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'acdAdmissionType'


class Acdadmissionyear(models.Model):
    ayid = models.BigAutoField(primary_key=True)
    admissionyear = models.IntegerField()
    noofbatchesexists = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdAdmissionYear'


class Acdassignmentmarks(models.Model):
    assignmentid = models.ForeignKey('Acdassignmentmaster', models.DO_NOTHING, db_column='assignmentid')
    studentid = models.ForeignKey('Acdstudentadmissiondetails', models.DO_NOTHING, db_column='studentid')
    mark = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'acdAssignmentMarks'


class Acdassignmentmaster(models.Model):
    assignmentid = models.BigAutoField(primary_key=True)
    assignmenttypeid = models.ForeignKey('Acdassignmenttype', models.DO_NOTHING, db_column='assignmenttypeid')
    batchid = models.ForeignKey('Acdbatches', models.DO_NOTHING, db_column='batchid')
    staffid = models.ForeignKey('Acdstaffdetails', models.DO_NOTHING, db_column='staffid')
    announcementdate = models.DateField()
    submissiondate = models.DateField()
    topic = models.CharField(max_length=200)
    maximummark = models.IntegerField()
    subjectid = models.ForeignKey('Acdsubjects', models.DO_NOTHING, db_column='subjectid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdAssignmentMaster'


class Acdassignmenttype(models.Model):
    assignmenttypeid = models.BigAutoField(primary_key=True)
    assignmenttype = models.CharField(max_length=50)
    includedinsessional = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'acdAssignmentType'


class Acdattendance(models.Model):
    attendanceid = models.ForeignKey('Acdattendancemaster', models.DO_NOTHING, db_column='attendanceid')
    studentid = models.ForeignKey('Acdstudentadmissiondetails', models.DO_NOTHING, db_column='studentid')
    status = models.CharField(max_length=1)
    hourno = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'acdAttendance'
        unique_together = (('attendanceid', 'studentid', 'hourno'),)


class Acdattendancedetails(models.Model):
    attendanceid = models.ForeignKey('Acdattendancemaster', models.DO_NOTHING, db_column='attendanceid')
    subjectid = models.ForeignKey('Acdsubjects', models.DO_NOTHING, db_column='subjectid')
    facultyid = models.ForeignKey('Acdstaffdetails', models.DO_NOTHING, db_column='facultyid')
    hourno = models.IntegerField()
    complete = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdAttendanceDetails'
        unique_together = (('attendanceid', 'hourno'), ('attendanceid', 'subjectid'),)


class Acdattendancelock(models.Model):
    batchid = models.BigIntegerField(blank=True, null=True)
    lockfromdate = models.DateField(blank=True, null=True)
    lockes = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdAttendanceLock'


class Acdattendancemaster(models.Model):
    attendanceid = models.BigAutoField(primary_key=True)
    batchid = models.ForeignKey('Acdbatches', models.DO_NOTHING, db_column='batchid')
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'acdAttendanceMaster'


class Acdattendancescheme(models.Model):
    sessionalparameterdetailsid = models.ForeignKey('Acdsessionalparameterdetails', models.DO_NOTHING, db_column='sessionalparameterdetailsid', blank=True, null=True)
    schemeid = models.ForeignKey('Acdattendanceschememaster', models.DO_NOTHING, db_column='schemeid')

    class Meta:
        managed = False
        db_table = 'acdAttendanceScheme'


class Acdattendanceschemedetails(models.Model):
    schemeid = models.ForeignKey('Acdattendanceschememaster', models.DO_NOTHING, db_column='schemeid', blank=True, null=True)
    attendancefrom = models.FloatField(blank=True, null=True)
    attendanceto = models.FloatField(blank=True, null=True)
    attendancemark = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdAttendanceSchemeDetails'


class Acdattendanceschememaster(models.Model):
    schemeid = models.BigAutoField(primary_key=True)
    schemename = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdAttendanceSchemeMaster'


class Acdbatchstudents(models.Model):
    batchid = models.ForeignKey('Acdbatches', models.DO_NOTHING, db_column='batchid')
    studentid = models.ForeignKey('Acdstudentadmissiondetails', models.DO_NOTHING, db_column='studentid')
    rollno = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'acdBatchStudents'
        unique_together = (('batchid', 'studentid', 'rollno'),)


class Acdbatches(models.Model):
    batchid = models.BigAutoField(primary_key=True)
    batchcode = models.CharField(max_length=25)
    batchname = models.CharField(max_length=150)
    admissionyear = models.IntegerField()
    whethercurrentbatch = models.CharField(max_length=1)
    specializationid = models.ForeignKey('Acdspecialization', models.DO_NOTHING, db_column='specializationid')
    breakid = models.ForeignKey('Acdcoursetypebreaks', models.DO_NOTHING, db_column='breakid')
    active = models.CharField(max_length=1)
    batchstartdate = models.DateField()
    batchclosedate = models.DateField(blank=True, null=True)
    whetherhavesubgroups = models.IntegerField()
    classname = models.CharField(max_length=3, blank=True, null=True)
    cdcode = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdBatches'


class Acdbatchessubjects(models.Model):
    batchsubjectid = models.BigAutoField(primary_key=True)
    batchid = models.ForeignKey(Acdbatches, models.DO_NOTHING, db_column='batchid')
    subjectid = models.ForeignKey('Acdsubjects', models.DO_NOTHING, db_column='subjectid')

    class Meta:
        managed = False
        db_table = 'acdBatchesSubjects'


class Acdcampus(models.Model):
    campusid = models.BigAutoField(primary_key=True)
    campuscode = models.CharField(max_length=20, blank=True, null=True)
    campusname = models.CharField(max_length=100, blank=True, null=True)
    address1 = models.CharField(max_length=50, blank=True, null=True)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    address3 = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    pin = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdCampus'


class Acdcaste(models.Model):
    casteid = models.BigAutoField(primary_key=True)
    caste = models.CharField(max_length=50)
    religionid = models.ForeignKey('Acdreligion', models.DO_NOTHING, db_column='religionid', blank=True, null=True)
    cdcode = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdCaste'


class Acdclassnotes(models.Model):
    noteid = models.BigAutoField(primary_key=True)
    subjectid = models.ForeignKey('Acdsubjects', models.DO_NOTHING, db_column='subjectid', blank=True, null=True)
    staffid = models.ForeignKey('Acdstaffdetails', models.DO_NOTHING, db_column='staffid', blank=True, null=True)
    notelocation = models.CharField(max_length=100)
    filetype = models.CharField(max_length=-1, blank=True, null=True)
    date = models.DateField()
    title = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdClassNotes'


class Acdclassnotesbatches(models.Model):
    noteid = models.ForeignKey(Acdclassnotes, models.DO_NOTHING, db_column='noteid')
    batchid = models.ForeignKey(Acdbatches, models.DO_NOTHING, db_column='batchid')

    class Meta:
        managed = False
        db_table = 'acdClassNotesBatches'
        unique_together = (('noteid', 'batchid'),)


class Acdclasses(models.Model):
    specializationid = models.ForeignKey('Acdspecialization', models.DO_NOTHING, db_column='specializationid')
    serialno = models.IntegerField()
    classname = models.CharField(max_length=-1)
    classstartyear = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdClasses'


class Acdcourse(models.Model):
    courseid = models.BigAutoField(primary_key=True)
    coursecode = models.CharField(max_length=10)
    coursename = models.CharField(max_length=100)
    coursetypeid = models.ForeignKey('Acdcoursetype', models.DO_NOTHING, db_column='coursetypeid')
    courselevelid = models.ForeignKey('Acdcourselevel', models.DO_NOTHING, db_column='courselevelid')
    cdcode = models.IntegerField(blank=True, null=True)
    hour = models.BigIntegerField(blank=True, null=True)
    mindurationyear = models.IntegerField(blank=True, null=True)
    minimumpasspercentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdCourse'


class Acdcourseboard(models.Model):
    boardid = models.BigAutoField(primary_key=True)
    boardname = models.CharField(max_length=100, blank=True, null=True)
    boardlevelid = models.ForeignKey('Acdqualificationlevel', models.DO_NOTHING, db_column='boardlevelid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdCourseBoard'


class Acdcoursechange(models.Model):
    studentid = models.ForeignKey('Acdstudentadmissiondetails', models.DO_NOTHING, db_column='studentid')
    newspecializationid = models.ForeignKey('Acdspecialization', models.DO_NOTHING, db_column='newspecializationid')
    breakid = models.ForeignKey('Acdcoursetypebreaks', models.DO_NOTHING, db_column='breakid')
    changedate = models.DateField()
    oldspecializationid = models.ForeignKey('Acdspecialization', models.DO_NOTHING, db_column='oldspecializationid')
    batchid = models.ForeignKey(Acdbatches, models.DO_NOTHING, db_column='batchid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdCourseChange'
        unique_together = (('studentid', 'newspecializationid', 'breakid', 'changedate', 'oldspecializationid'),)


class Acdcoursedetails(models.Model):
    courseid = models.ForeignKey(Acdcourse, models.DO_NOTHING, db_column='courseid')
    affiliateduniversity = models.CharField(max_length=100)
    universityaddress1 = models.CharField(max_length=100)
    universityaddress2 = models.CharField(max_length=100)
    universityplace = models.CharField(max_length=100)
    pin = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'acdCourseDetails'


class Acdcoursehours(models.Model):
    courseid = models.BigIntegerField()
    hours = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'acdCourseHours'
        unique_together = (('courseid', 'hours'),)


class Acdcourselevel(models.Model):
    courselevelid = models.BigAutoField(primary_key=True)
    courseleveldesc = models.CharField(max_length=100)
    cdcode = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdCourseLevel'


class Acdcoursetype(models.Model):
    coursetypeid = models.BigAutoField(primary_key=True)
    coursetype = models.CharField(max_length=50)
    noofbreaks = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'acdCourseType'


class Acdcoursetypebreaks(models.Model):
    breakid = models.BigAutoField(primary_key=True)
    coursetypeid = models.ForeignKey(Acdcoursetype, models.DO_NOTHING, db_column='coursetypeid')
    breakcode = models.CharField(max_length=10)
    breakname = models.CharField(max_length=50)
    breaknum = models.IntegerField()
    courseid = models.ForeignKey(Acdcourse, models.DO_NOTHING, db_column='courseid')
    sessionalattendanceschemeid = models.ForeignKey(Acdattendanceschememaster, models.DO_NOTHING, db_column='sessionalattendanceschemeid', blank=True, null=True)
    cdcode = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdCourseTypeBreaks'


class Acddays(models.Model):
    dayid = models.BigAutoField(primary_key=True)
    dayname = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'acdDays'


class Acddiscontinuedstudent(models.Model):
    studentid = models.ForeignKey('Acdstudentadmissiondetails', models.DO_NOTHING, db_column='studentid')
    discontinuedbatchid = models.ForeignKey(Acdbatches, models.DO_NOTHING, db_column='discontinuedbatchid')
    reason = models.CharField(max_length=200, blank=True, null=True)
    readmittedbatchid = models.ForeignKey(Acdcoursetypebreaks, models.DO_NOTHING, db_column='readmittedbatchid', blank=True, null=True)
    statustypeid = models.ForeignKey('Acdstudentstatus', models.DO_NOTHING, db_column='statustypeid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdDiscontinuedStudent'


class Acddutyleavedetails(models.Model):
    id = models.ForeignKey('Acddutyleavehistorymaster', models.DO_NOTHING, db_column='id')
    studentid = models.ForeignKey('Acdstudentadmissiondetails', models.DO_NOTHING, db_column='studentid')
    hourno = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'acdDutyLeaveDetails'


class Acddutyleavehistorymaster(models.Model):
    id = models.BigAutoField(primary_key=True)
    staffid = models.ForeignKey('Acdstaffdetails', models.DO_NOTHING, db_column='staffid')
    batchid = models.ForeignKey(Acdbatches, models.DO_NOTHING, db_column='batchid')
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'acdDutyLeaveHistoryMaster'


class Acdentrancetest(models.Model):
    entrancetestid = models.BigAutoField(primary_key=True)
    entrancetestname = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'acdEntranceTest'


class Acdexamtype(models.Model):
    examtypeid = models.BigAutoField(primary_key=True)
    examtype = models.CharField(max_length=100)
    updatefield = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdExamType'


class Acdfboastudents(models.Model):
    studentid = models.ForeignKey('Acdstudentadmissiondetails', models.DO_NOTHING, db_column='studentid')
    pfnumber = models.CharField(max_length=20)
    membershipnumber = models.CharField(max_length=20)
    membername = models.CharField(max_length=100)
    relationshipid = models.ForeignKey('Acdrelationship', models.DO_NOTHING, db_column='relationshipid')
    membershipid = models.ForeignKey('Acdfboamembertype', models.DO_NOTHING, db_column='membershipid')

    class Meta:
        managed = False
        db_table = 'acdFBOAStudents'


class Acdfboamembertype(models.Model):
    membershipid = models.BigAutoField(primary_key=True)
    membershipname = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'acdFBOAmemberType'


class Acdgroupadvisor(models.Model):
    staffid = models.ForeignKey('Acdstaffdetails', models.DO_NOTHING, db_column='staffid')
    batchid = models.ForeignKey(Acdbatches, models.DO_NOTHING, db_column='batchid')

    class Meta:
        managed = False
        db_table = 'acdGroupAdvisor'


class Acdhistory(models.Model):
    studentid = models.ForeignKey('Acdstudentadmissiondetails', models.DO_NOTHING, db_column='studentid')
    admissionnumber = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdHistory'


class Acdinternaltestattendancedetails(models.Model):
    internaltestid = models.ForeignKey('Acdinternaltestmaster', models.DO_NOTHING, db_column='internaltestid')
    internaltestdetailsid = models.ForeignKey('Acdinternaltestdetails', models.DO_NOTHING, db_column='internaltestdetailsid', blank=True, null=True)
    hourno = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdInternalTestAttendanceDetails'


class Acdinternaltestdetails(models.Model):
    internaltestdetailsid = models.BigAutoField(primary_key=True)
    internaltestid = models.ForeignKey('Acdinternaltestmaster', models.DO_NOTHING, db_column='internaltestid')
    subjectid = models.ForeignKey('Acdsubjects', models.DO_NOTHING, db_column='subjectid')
    date = models.DateField()
    attendanceadded = models.CharField(max_length=1)
    maximummark = models.IntegerField()
    passmark = models.IntegerField()
    facultyid = models.ForeignKey('Acdstaffdetails', models.DO_NOTHING, db_column='facultyid')

    class Meta:
        managed = False
        db_table = 'acdInternalTestDetails'


class Acdinternaltestmarks(models.Model):
    internaltestid = models.ForeignKey('Acdinternaltestmaster', models.DO_NOTHING, db_column='internaltestid')
    internaltestdetailsid = models.ForeignKey(Acdinternaltestdetails, models.DO_NOTHING, db_column='internaltestdetailsid')
    studentid = models.ForeignKey('Acdstudentadmissiondetails', models.DO_NOTHING, db_column='studentid')
    mark = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'acdInternalTestMarks'


class Acdinternaltestmaster(models.Model):
    internaltestid = models.BigAutoField(primary_key=True)
    testdesc = models.CharField(max_length=100)
    testtypeid = models.ForeignKey('Acdtesttype', models.DO_NOTHING, db_column='testtypeid')
    batchid = models.ForeignKey(Acdbatches, models.DO_NOTHING, db_column='batchid')
    examno = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'acdInternalTestMaster'


class Acdlogin(models.Model):
    userid = models.ForeignKey('Acdstaffdetails', models.DO_NOTHING, db_column='userid', primary_key=True)
    password = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdLogin'


class Acdmaritalstatus(models.Model):
    statusid = models.BigAutoField(primary_key=True)
    statusname = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdMaritalStatus'


class Acdmonthname(models.Model):
    monthid = models.BigAutoField(primary_key=True)
    monthname = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'acdMonthName'


class Acdnationality(models.Model):
    nationalityid = models.BigAutoField(primary_key=True)
    nationality = models.CharField(max_length=50)
    cdcode = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdNationality'


class Acdnotificationbatches(models.Model):
    batchid = models.ForeignKey(Acdbatches, models.DO_NOTHING, db_column='batchid')
    noticeid = models.ForeignKey('Acdnotifications', models.DO_NOTHING, db_column='noticeid')

    class Meta:
        managed = False
        db_table = 'acdNotificationBatches'
        unique_together = (('batchid', 'noticeid'),)


class Acdnotifications(models.Model):
    noticeid = models.BigAutoField(primary_key=True)
    staffid = models.ForeignKey('Acdstaffdetails', models.DO_NOTHING, db_column='staffid', blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdNotifications'


class Acdproposedresidence(models.Model):
    residenceid = models.BigIntegerField(primary_key=True)
    staytype = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'acdProposedResidence'


class Acdqualificationlevel(models.Model):
    qualificationlevelid = models.AutoField(primary_key=True)
    qualificationlevel = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'acdQualificationLevel'


class Acdqualifications(models.Model):
    qualificationid = models.BigAutoField(primary_key=True)
    qualificationcode = models.CharField(max_length=20)
    qualificationdesc = models.CharField(max_length=100)
    qualificationlevelid = models.ForeignKey(Acdqualificationlevel, models.DO_NOTHING, db_column='qualificationlevelid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdQualifications'


class Acdrelationship(models.Model):
    relationshipid = models.BigIntegerField(primary_key=True)
    relationshipname = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'acdRelationship'


class Acdreligion(models.Model):
    religionid = models.BigAutoField(primary_key=True)
    religion = models.CharField(max_length=40)
    cdcode = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdReligion'


class Acdseatsubtype(models.Model):
    subtypeseatid = models.BigAutoField(primary_key=True)
    subtypeseatdesc = models.CharField(max_length=200)
    seatid = models.ForeignKey('Acdseattype', models.DO_NOTHING, db_column='seatid')

    class Meta:
        managed = False
        db_table = 'acdSeatSubType'


class Acdseattype(models.Model):
    seatid = models.BigAutoField(primary_key=True)
    seatdesc = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'acdSeatType'


class Acdsessionalinputdetails(models.Model):
    sessionalid = models.ForeignKey('Acdsessionalmaster', models.DO_NOTHING, db_column='sessionalid')
    sessionalparameterdescription = models.CharField(max_length=50)
    sessionalinputparameterid = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'acdSessionalInputDetails'


class Acdsessionalmarkdetails(models.Model):
    sessionalid = models.ForeignKey('Acdsessionalmaster', models.DO_NOTHING, db_column='sessionalid', blank=True, null=True)
    studentid = models.BigIntegerField(blank=True, null=True)
    sessionalparameterdetailsid = models.ForeignKey('Acdsessionalparameterdetails', models.DO_NOTHING, db_column='sessionalparameterdetailsid', blank=True, null=True)
    sessionalmark = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdSessionalMarkDetails'


class Acdsessionalmarks(models.Model):
    sessionalid = models.ForeignKey('Acdsessionalmaster', models.DO_NOTHING, db_column='sessionalid', blank=True, null=True)
    studentid = models.ForeignKey('Acdstudentadmissiondetails', models.DO_NOTHING, db_column='studentid', blank=True, null=True)
    totalmark = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gracemark = models.IntegerField(blank=True, null=True)
    calculatedmark = models.IntegerField(blank=True, null=True)
    normalizedmark = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdSessionalMarks'


class Acdsessionalmaster(models.Model):
    sessionalid = models.BigAutoField(primary_key=True)
    batchid = models.ForeignKey(Acdbatches, models.DO_NOTHING, db_column='batchid', blank=True, null=True)
    subjectid = models.ForeignKey('Acdsubjects', models.DO_NOTHING, db_column='subjectid', blank=True, null=True)
    finalized = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdSessionalMaster'


class Acdsessionalparameterdetails(models.Model):
    sessionalparameterdetailsid = models.BigAutoField(primary_key=True)
    sessionalparameterid = models.ForeignKey('Acdsessionalparameters', models.DO_NOTHING, db_column='sessionalparameterid', blank=True, null=True)
    sessionalparametermasterid = models.ForeignKey('Acdsessionalparametermaster', models.DO_NOTHING, db_column='sessionalparametermasterid', blank=True, null=True)
    maximummark = models.DecimalField(max_digits=10, decimal_places=2)
    splitexists = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'acdSessionalParameterDetails'


class Acdsessionalparameterdivisions(models.Model):
    sessionalparameterdivisionid = models.BigAutoField(primary_key=True)
    sessionalparameterdivisionname = models.CharField(max_length=200, blank=True, null=True)
    maximummarkdivision = models.IntegerField(blank=True, null=True)
    sessionalparameterdetailsid = models.ForeignKey(Acdsessionalparameterdetails, models.DO_NOTHING, db_column='sessionalparameterdetailsid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdSessionalParameterDivisions'


class Acdsessionalparametermarkdivisions(models.Model):
    sessionalid = models.ForeignKey(Acdsessionalmaster, models.DO_NOTHING, db_column='sessionalid')
    sessionalparameterdivisionid = models.ForeignKey(Acdsessionalparameterdivisions, models.DO_NOTHING, db_column='sessionalparameterdivisionid')
    mark = models.FloatField(blank=True, null=True)
    studentid = models.ForeignKey('Acdstudentadmissiondetails', models.DO_NOTHING, db_column='studentid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdSessionalParameterMarkDivisions'


class Acdsessionalparametermaster(models.Model):
    sessionalparametermasterid = models.BigAutoField(primary_key=True)
    courseid = models.ForeignKey(Acdcourse, models.DO_NOTHING, db_column='courseid', blank=True, null=True)
    sessionalparameternameid = models.ForeignKey('Acdsessionalparametername', models.DO_NOTHING, db_column='sessionalparameternameid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdSessionalParameterMaster'


class Acdsessionalparametername(models.Model):
    sessionalparameternameid = models.BigAutoField(primary_key=True)
    sessionalparametername = models.CharField(max_length=-1, blank=True, null=True)
    sessionalparameternamemaxmark = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdSessionalParameterName'


class Acdsessionalparameters(models.Model):
    sessionalparameterid = models.BigAutoField(primary_key=True)
    breakid = models.ForeignKey(Acdcoursetypebreaks, models.DO_NOTHING, db_column='breakid', blank=True, null=True)
    specializationid = models.ForeignKey('Acdspecialization', models.DO_NOTHING, db_column='specializationid', blank=True, null=True)
    subjectid = models.ForeignKey('Acdsubjects', models.DO_NOTHING, db_column='subjectid', blank=True, null=True)
    batchid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdSessionalParameters'


class Acdspecialization(models.Model):
    specializationid = models.BigAutoField(primary_key=True)
    specializationcode = models.CharField(max_length=10)
    specializationdesc = models.CharField(max_length=100)
    courseid = models.ForeignKey(Acdcourse, models.DO_NOTHING, db_column='courseid')
    coursestartyear = models.IntegerField()
    cdcode = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdSpecialization'


class Acdstaffdetails(models.Model):
    staffid = models.BigAutoField(primary_key=True)
    staffcode = models.CharField(max_length=10)
    staffname = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'acdStaffDetails'


class Acdstaffphotos(models.Model):
    staffid = models.ForeignKey(Acdstaffdetails, models.DO_NOTHING, db_column='staffid', primary_key=True)
    photo = models.BinaryField(blank=True, null=True)
    medium = models.BinaryField(blank=True, null=True)
    small = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdStaffPhotos'


class Acdstate(models.Model):
    stateid = models.BigAutoField(primary_key=True)
    state = models.CharField(max_length=50)
    nationalityid = models.ForeignKey(Acdnationality, models.DO_NOTHING, db_column='nationalityid')

    class Meta:
        managed = False
        db_table = 'acdState'


class Acdstudentacademichistory(models.Model):
    studentid = models.ForeignKey('Acdstudentadmissiondetails', models.DO_NOTHING, db_column='studentid')
    qualificationid = models.ForeignKey(Acdqualifications, models.DO_NOTHING, db_column='qualificationid')
    nameofinstitution = models.CharField(max_length=100, blank=True, null=True)
    placeofinstitution = models.CharField(max_length=100, blank=True, null=True)
    marksobtained = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    maximunmarks = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    registernumber = models.CharField(max_length=20, blank=True, null=True)
    monthofpassing = models.CharField(max_length=20, blank=True, null=True)
    yearofpassing = models.IntegerField(blank=True, null=True)
    markpercentage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    marksheetnumber = models.CharField(max_length=50, blank=True, null=True)
    boardid = models.ForeignKey(Acdcourseboard, models.DO_NOTHING, db_column='boardid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdStudentAcademicHistory'
        unique_together = (('studentid', 'qualificationid'),)


class Acdstudentadmissiondetails(models.Model):
    studentid = models.BigAutoField(primary_key=True)
    studentname = models.CharField(max_length=100)
    fathersname = models.CharField(max_length=100)
    admissionnumber = models.CharField(unique=True, max_length=20)
    admissiondate = models.DateField()
    admissionyear = models.IntegerField()
    currentspecializationid = models.ForeignKey(Acdspecialization, models.DO_NOTHING, db_column='currentspecializationid', blank=True, null=True)
    currentbreakid = models.ForeignKey(Acdcoursetypebreaks, models.DO_NOTHING, db_column='currentbreakid', blank=True, null=True)
    seatid = models.ForeignKey(Acdseattype, models.DO_NOTHING, db_column='seatid')
    subtypeseatid = models.ForeignKey(Acdseatsubtype, models.DO_NOTHING, db_column='subtypeseatid')
    entrancerank = models.DecimalField(max_digits=65535, decimal_places=65535)
    entrancerollno = models.CharField(max_length=50)
    currentbatch = models.ForeignKey(Acdbatches, models.DO_NOTHING, db_column='currentbatch', blank=True, null=True)
    admissiontypeid = models.ForeignKey(Acdadmissiontype, models.DO_NOTHING, db_column='admissiontypeid', blank=True, null=True)
    whetherfboa = models.CharField(max_length=-1, blank=True, null=True)
    statustypeid = models.ForeignKey('Acdstudentstatus', models.DO_NOTHING, db_column='statustypeid', blank=True, null=True)
    cdcode = models.CharField(max_length=10, blank=True, null=True)
    entrancetestid = models.ForeignKey(Acdentrancetest, models.DO_NOTHING, db_column='entrancetestid', blank=True, null=True)
    entrancetestyear = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdStudentAdmissionDetails'
        unique_together = (('studentname', 'studentid'),)


class Acdstudentcategory(models.Model):
    categoryid = models.BigAutoField(primary_key=True)
    categoryname = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdStudentCategory'


class Acdstudentcondonationdetails(models.Model):
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid')
    batchid = models.ForeignKey(Acdbatches, models.DO_NOTHING, db_column='batchid')
    condonationdate = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdStudentCondonationDetails'
        unique_together = (('studentid', 'batchid'),)


class Acdstudentlocalguardiandetails(models.Model):
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid', primary_key=True)
    localguardianname = models.CharField(max_length=50, blank=True, null=True)
    localguardianaddress1 = models.CharField(max_length=50, blank=True, null=True)
    localguardianaddress2 = models.CharField(max_length=50, blank=True, null=True)
    localguardianaddress3 = models.CharField(max_length=50, blank=True, null=True)
    localguardianplace = models.CharField(max_length=20, blank=True, null=True)
    localguardianpin = models.CharField(max_length=10, blank=True, null=True)
    localguardianphone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdStudentLocalGuardianDetails'


class Acdstudentparentdetails(models.Model):
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid')
    parentname = models.CharField(max_length=100)
    relationshipid = models.ForeignKey(Acdrelationship, models.DO_NOTHING, db_column='relationshipid')
    occupation = models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdStudentParentDetails'
        unique_together = (('studentid', 'relationshipid'),)


class Acdstudentpersonaldetails(models.Model):
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid', primary_key=True)
    permanantaddress1 = models.CharField(max_length=200)
    permanantaddress2 = models.CharField(max_length=200)
    permanantaddress3 = models.CharField(max_length=200)
    place = models.CharField(max_length=100, blank=True, null=True)
    pin = models.CharField(max_length=10)
    landphone = models.CharField(max_length=40)
    presentaddress1 = models.CharField(max_length=200)
    presentaddress2 = models.CharField(max_length=200)
    presentaddress3 = models.CharField(max_length=200)
    place1 = models.CharField(max_length=100, blank=True, null=True)
    pin1 = models.CharField(max_length=10)
    landphone1 = models.CharField(max_length=40)
    communicationaddress1 = models.CharField(max_length=200)
    communicationaddress2 = models.CharField(max_length=200)
    communicationaddress3 = models.CharField(max_length=200)
    place2 = models.CharField(max_length=100, blank=True, null=True)
    pin2 = models.CharField(max_length=10)
    landphone2 = models.CharField(max_length=40)
    studentmobileno = models.CharField(max_length=50, blank=True, null=True)
    studentemail = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField()
    sex = models.CharField(max_length=6)
    maritalstatus = models.CharField(max_length=15)
    religionid = models.ForeignKey(Acdreligion, models.DO_NOTHING, db_column='religionid')
    casteid = models.ForeignKey(Acdcaste, models.DO_NOTHING, db_column='casteid')
    stateid = models.ForeignKey(Acdstate, models.DO_NOTHING, db_column='stateid')
    nationalityid = models.ForeignKey(Acdnationality, models.DO_NOTHING, db_column='nationalityid')
    bloodgroup = models.CharField(max_length=10, blank=True, null=True)
    proposedresidence = models.CharField(max_length=-1, blank=True, null=True)
    hobbies = models.CharField(max_length=200, blank=True, null=True)
    extraactivities = models.CharField(max_length=200, blank=True, null=True)
    economicaly = models.CharField(max_length=1, blank=True, null=True)
    physically = models.CharField(max_length=1, blank=True, null=True)
    categoryid = models.BigIntegerField(blank=True, null=True)
    taluk = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdStudentPersonalDetails'


class Acdstudentphotos(models.Model):
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid', primary_key=True)
    photo = models.BinaryField(blank=True, null=True)
    medium = models.BinaryField(blank=True, null=True)
    small = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdStudentPhotos'


class Acdstudentregisternumber(models.Model):
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid')
    registerno = models.CharField(max_length=50)
    whethercurrent = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdStudentRegisterNumber'


class Acdstudentstatus(models.Model):
    statustypeid = models.AutoField(primary_key=True)
    statustype = models.CharField(max_length=100)
    permanentstatus = models.IntegerField()
    editable = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'acdStudentStatus'


class Acdstudentsubgroupdetails(models.Model):
    subgroupdetailid = models.ForeignKey('Acdstudentsubgroupdetailsmaster', models.DO_NOTHING, db_column='subgroupdetailid', blank=True, null=True)
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdStudentSubGroupDetails'


class Acdstudentsubgroupdetailsmaster(models.Model):
    subgroupdetailid = models.BigAutoField(primary_key=True)
    batchid = models.ForeignKey(Acdbatches, models.DO_NOTHING, db_column='batchid', blank=True, null=True)
    createdby = models.ForeignKey(Acdstaffdetails, models.DO_NOTHING, db_column='createdby', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdStudentSubGroupDetailsMaster'


class Acdstudentsubgroups(models.Model):
    subgroupid = models.BigAutoField(primary_key=True)
    subgroupdesc = models.CharField(max_length=50)
    batchid = models.ForeignKey(Acdbatches, models.DO_NOTHING, db_column='batchid')
    subjectid = models.ForeignKey('Acdsubjects', models.DO_NOTHING, db_column='subjectid')
    facultyid = models.ForeignKey(Acdstaffdetails, models.DO_NOTHING, db_column='facultyid')
    subgrouptypeid = models.ForeignKey('Acdsubgrouptype', models.DO_NOTHING, db_column='subgrouptypeid')
    subgroupdetailid = models.ForeignKey(Acdstudentsubgroupdetailsmaster, models.DO_NOTHING, db_column='subgroupdetailid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdStudentSubgroups'
        unique_together = (('batchid', 'subgroupid'),)


class Acdsubgrouptype(models.Model):
    subgrouptypeid = models.BigAutoField(primary_key=True)
    subgrouptypedesc = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'acdSubgroupType'


class Acdsubjectallocation(models.Model):
    batchsubjectid = models.ForeignKey(Acdbatchessubjects, models.DO_NOTHING, db_column='batchsubjectid')
    staffid = models.ForeignKey(Acdstaffdetails, models.DO_NOTHING, db_column='staffid')

    class Meta:
        managed = False
        db_table = 'acdSubjectAllocation'
        unique_together = (('batchsubjectid', 'staffid'),)


class Acdsubjectsplits(models.Model):
    subjectparentid = models.BigIntegerField(blank=True, null=True)
    subjectchildid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdSubjectSplits'


class Acdsubjecttype(models.Model):
    subjecttypeid = models.BigAutoField(primary_key=True)
    subjecttype = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'acdSubjectType'


class Acdsubjects(models.Model):
    subjectid = models.BigAutoField(primary_key=True)
    subjectcode = models.CharField(max_length=15)
    subjectdesc = models.CharField(max_length=150)
    internalmarkmax = models.DecimalField(max_digits=10, decimal_places=2)
    internalmarkmin = models.DecimalField(max_digits=10, decimal_places=2)
    courseid = models.ForeignKey(Acdcourse, models.DO_NOTHING, db_column='courseid')
    specidifany = models.ForeignKey(Acdspecialization, models.DO_NOTHING, db_column='specidifany', blank=True, null=True)
    breakid = models.ForeignKey(Acdcoursetypebreaks, models.DO_NOTHING, db_column='breakid')
    whetherelectivepaper = models.CharField(max_length=1)
    externalmarkmax = models.DecimalField(max_digits=10, decimal_places=2)
    externalmarkmin = models.DecimalField(max_digits=10, decimal_places=2)
    subjecttypeid = models.BigIntegerField(blank=True, null=True)
    cdcode = models.BigIntegerField(blank=True, null=True)
    live = models.IntegerField(blank=True, null=True)
    subjectorder = models.IntegerField(blank=True, null=True)
    electivenumber = models.IntegerField(blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdSubjects'


class Acdtermination(models.Model):
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid')
    dateoftermination = models.DateField(blank=True, null=True)
    reasonfortermination = models.CharField(max_length=200, blank=True, null=True)
    oldstatustypeid = models.ForeignKey(Acdstudentstatus, models.DO_NOTHING, db_column='oldstatustypeid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdTermination'


class Acdtesttype(models.Model):
    testtypeid = models.BigAutoField(primary_key=True)
    testtype = models.CharField(max_length=50)
    includeforsessional = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'acdTestType'


class Acdtimetable(models.Model):
    staffid = models.ForeignKey(Acdstaffdetails, models.DO_NOTHING, db_column='staffid')
    batchid = models.ForeignKey(Acdbatches, models.DO_NOTHING, db_column='batchid')
    dayid = models.ForeignKey(Acddays, models.DO_NOTHING, db_column='dayid')
    subjectid = models.ForeignKey(Acdsubjects, models.DO_NOTHING, db_column='subjectid')
    timefrom = models.TimeField()
    timeto = models.TimeField()

    class Meta:
        managed = False
        db_table = 'acdTimeTable'


class Acduniversityexamdetails(models.Model):
    examid = models.ForeignKey('Acduniversityexammaster', models.DO_NOTHING, db_column='examid')
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid')
    registerno = models.CharField(max_length=10)
    examtypeid = models.ForeignKey(Acdexamtype, models.DO_NOTHING, db_column='examtypeid')

    class Meta:
        managed = False
        db_table = 'acdUniversityExamDetails'


class Acduniversityexammarks(models.Model):
    examid = models.ForeignKey('Acduniversityexammaster', models.DO_NOTHING, db_column='examid')
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid')
    subjectid = models.ForeignKey(Acdsubjects, models.DO_NOTHING, db_column='subjectid')
    mark = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'acdUniversityExamMarks'


class Acduniversityexammaster(models.Model):
    examid = models.BigAutoField(primary_key=True)
    examname = models.CharField(max_length=200)
    specializationid = models.ForeignKey(Acdspecialization, models.DO_NOTHING, db_column='specializationid')
    breakid = models.ForeignKey(Acdcoursetypebreaks, models.DO_NOTHING, db_column='breakid')
    examyear = models.IntegerField()
    examfrom = models.DateField()
    examto = models.DateField()
    batchidifany = models.BigIntegerField(blank=True, null=True)
    exammonthid = models.ForeignKey(Acdmonthname, models.DO_NOTHING, db_column='exammonthid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdUniversityExamMaster'


class Acduniversityexammaxmark(models.Model):
    examid = models.ForeignKey(Acduniversityexammaster, models.DO_NOTHING, db_column='examid')
    subjectid = models.ForeignKey(Acdsubjects, models.DO_NOTHING, db_column='subjectid')
    maximummark = models.CharField(max_length=20)
    whetherselected = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acdUniversityExamMaxMark'


class Android(models.Model):
    studname = models.CharField(max_length=50)
    enrollid = models.CharField(primary_key=True, max_length=20)
    emailid = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'android'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Breaknumber(models.Model):
    breaknum = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'breaknumber'


class Dbreaknum(models.Model):
    breaknum = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dbreaknum'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Dschemeid(models.Model):
    schemeid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dschemeid'


class Dschemeid1(models.Model):
    schemeid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dschemeid1'


class Dschemeid2(models.Model):
    schemeid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dschemeid2'


class Dschemeid5(models.Model):
    schemeid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dschemeid5'


class Fdbbatchsubjectfaculty(models.Model):
    allocationid = models.AutoField(primary_key=True)
    batchid = models.ForeignKey(Acdbatches, models.DO_NOTHING, db_column='batchid', blank=True, null=True)
    subjectid = models.ForeignKey(Acdsubjects, models.DO_NOTHING, db_column='subjectid', blank=True, null=True)
    staffid = models.ForeignKey(Acdstaffdetails, models.DO_NOTHING, db_column='staffid', blank=True, null=True)
    readyforevaluation = models.IntegerField(blank=True, null=True)
    subjecttypeid = models.ForeignKey(Acdsubjecttype, models.DO_NOTHING, db_column='subjecttypeid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fdbBatchSubjectFaculty'


class Fdbiptable(models.Model):
    ipaddress = models.CharField(unique=True, max_length=20, blank=True, null=True)
    success = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fdbIPTable'


class Fdbpassword(models.Model):
    passwod = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fdbPassword'


class Fdbquestionratingallocation(models.Model):
    questionid = models.ForeignKey('Fdbquestionare', models.DO_NOTHING, db_column='questionid', blank=True, null=True)
    ratingid = models.ForeignKey('Fdbratings', models.DO_NOTHING, db_column='ratingid', blank=True, null=True)
    mark = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fdbQuestionRatingAllocation'


class Fdbquestionare(models.Model):
    questionid = models.AutoField(primary_key=True)
    questionorder = models.IntegerField(blank=True, null=True)
    question = models.CharField(max_length=300, blank=True, null=True)
    maximummark = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    courseid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fdbQuestionare'


class Fdbratings(models.Model):
    ratingid = models.AutoField(primary_key=True)
    rating = models.CharField(max_length=50, blank=True, null=True)
    courseid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fdbRatings'


class Fdbevaluation(models.Model):
    allocationid = models.ForeignKey(Fdbbatchsubjectfaculty, models.DO_NOTHING, db_column='allocationid', blank=True, null=True)
    questionid = models.ForeignKey(Fdbquestionare, models.DO_NOTHING, db_column='questionid', blank=True, null=True)
    ratingid = models.ForeignKey(Fdbratings, models.DO_NOTHING, db_column='ratingid', blank=True, null=True)
    dateofevaluation = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fdbevaluation'


class Fdbtempevaluation(models.Model):
    allocationid = models.ForeignKey(Fdbbatchsubjectfaculty, models.DO_NOTHING, db_column='allocationid', blank=True, null=True)
    questionid = models.ForeignKey(Fdbquestionare, models.DO_NOTHING, db_column='questionid', blank=True, null=True)
    ratingid = models.ForeignKey(Fdbratings, models.DO_NOTHING, db_column='ratingid', blank=True, null=True)
    dateofevaluation = models.DateField(blank=True, null=True)
    ipaddress = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fdbtempevaluation'


class Feeadvancefee(models.Model):
    studentid = models.BigIntegerField()
    advanceamountprevious = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    advanceamountcurrent = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    recieptno = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeAdvanceFee'


class Feeadvancefeehistory(models.Model):
    studentid = models.BigIntegerField(blank=True, null=True)
    advanceamount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    recieptno = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeAdvanceFeeHistory'


class Feebusboardingpoint(models.Model):
    busboardingpointid = models.BigAutoField(primary_key=True)
    busboardingpointdesc = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeBusBoardingPoint'


class Feebusboardingpointamount(models.Model):
    busboardingpointid = models.ForeignKey(Feebusboardingpoint, models.DO_NOTHING, db_column='busboardingpointid')
    busboardingpointamount = models.FloatField()
    busboardingpointdate = models.DateField()
    busboardingpointstatus = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'feeBusBoardingPointAmount'
        unique_together = (('busboardingpointid', 'busboardingpointdate'), ('busboardingpointid', 'busboardingpointdate', 'busboardingpointstatus'),)


class Feebusdirection(models.Model):
    busdirectionid = models.BigAutoField(primary_key=True)
    busdirectiondesc = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeBusDirection'


class Feebusstopdetails(models.Model):
    busboardingpointid = models.ForeignKey(Feebusboardingpoint, models.DO_NOTHING, db_column='busboardingpointid')
    busdirectionid = models.ForeignKey(Feebusdirection, models.DO_NOTHING, db_column='busdirectionid')

    class Meta:
        managed = False
        db_table = 'feeBusStopDetails'
        unique_together = (('busboardingpointid', 'busdirectionid'),)


class Feebusstudentdetails(models.Model):
    bid = models.BigAutoField()
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid')
    amount = models.BigIntegerField()
    busboardingpoint = models.BigIntegerField()
    feesubtypeid = models.BigIntegerField()
    status = models.BigIntegerField(blank=True, null=True)
    receiptno = models.CharField(max_length=25, blank=True, null=True)
    busmasterid = models.ForeignKey('Feebusstudentmaster', models.DO_NOTHING, db_column='busmasterid')

    class Meta:
        managed = False
        db_table = 'feeBusStudentDetails'
        unique_together = (('studentid', 'busmasterid'),)


class Feebusstudentmaster(models.Model):
    id = models.BigAutoField(primary_key=True)
    rentfrom = models.DateField()
    rentto = models.DateField()
    duedate = models.DateField()
    noofdays = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeBusStudentMaster'


class Feechangefeedetails(models.Model):
    studentwisechangefee = models.CharField(max_length=40)
    feesubtypeid = models.ForeignKey('Feefeesubtype', models.DO_NOTHING, db_column='feesubtypeid', primary_key=True)

    class Meta:
        managed = False
        db_table = 'feeChangeFeeDetails'


class Feecommonfeedetails(models.Model):
    feesubtypeid = models.ForeignKey('Feefeesubtype', models.DO_NOTHING, db_column='feesubtypeid')
    feeamount = models.FloatField(blank=True, null=True)
    feesubtypestatus = models.BigIntegerField(blank=True, null=True)
    feesubtypedate = models.DateField()

    class Meta:
        managed = False
        db_table = 'feeCommonFeeDetails'
        unique_together = (('feesubtypeid', 'feesubtypedate'),)


class Feecommonnamefeesubtype(models.Model):
    feesubtypeid = models.ForeignKey('Feefeesubtype', models.DO_NOTHING, db_column='feesubtypeid', blank=True, null=True)
    feenamecommonid = models.ForeignKey('Feenamecommon', models.DO_NOTHING, db_column='feenamecommonid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeCommonNameFeeSubType'


class Feeconcessionamount(models.Model):
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid')
    feesubtypeid = models.BigIntegerField()
    feeamount = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeConcessionAmount'
        unique_together = (('studentid', 'feesubtypeid'),)


class Feeddorchequedetails(models.Model):
    recieptno = models.ForeignKey('Feereciept', models.DO_NOTHING, db_column='recieptno', primary_key=True)
    bankbranch = models.CharField(max_length=50, blank=True, null=True)
    bankname = models.CharField(max_length=50, blank=True, null=True)
    ddorchquedate = models.DateField(blank=True, null=True)
    ddorchequeamount = models.FloatField(blank=True, null=True)
    desc = models.CharField(max_length=100, blank=True, null=True)
    ddorchequeno = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeDDOrChequeDetails'


class Feefeeamount(models.Model):
    studtypeid = models.ForeignKey('Feestudenttypedetails', models.DO_NOTHING, db_column='studtypeid')
    feesubtypeid = models.ForeignKey('Feefeesubtype', models.DO_NOTHING, db_column='feesubtypeid')
    feeamount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeFeeAmount'
        unique_together = (('studtypeid', 'feesubtypeid'),)


class Feefeeindexdetails(models.Model):
    courseid = models.ForeignKey(Acdcourse, models.DO_NOTHING, db_column='courseid')
    feemaintypeid = models.ForeignKey('Feefeemaintype', models.DO_NOTHING, db_column='feemaintypeid')
    index = models.BigIntegerField(blank=True, null=True)
    dueperiod = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeFeeIndexDetails'
        unique_together = (('courseid', 'feemaintypeid'),)


class Feefeemaintype(models.Model):
    feemaintypeid = models.BigAutoField(primary_key=True)
    feemaintypedesc = models.CharField(max_length=50, blank=True, null=True)
    coursewisechangeornot = models.BigIntegerField(blank=True, null=True)
    order = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeFeeMainType'


class Feefeesubtype(models.Model):
    feesubtypeid = models.BigAutoField(primary_key=True)
    feemaintypeid = models.ForeignKey(Feefeemaintype, models.DO_NOTHING, db_column='feemaintypeid', blank=True, null=True)
    feesubtypedesc = models.CharField(max_length=50, blank=True, null=True)
    feesubtypeamountrefundornot = models.BigIntegerField(blank=True, null=True)
    feesubtypeamountsingleornot = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeFeeSubType'


class Feehostel(models.Model):
    hostelid = models.BigAutoField(primary_key=True)
    hostelname = models.CharField(max_length=100, blank=True, null=True)
    capacity = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeHostel'


class Feehostelrent(models.Model):
    hostelid = models.BigIntegerField(blank=True, null=True)
    admissionyear = models.BigIntegerField(blank=True, null=True)
    rentamount = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeHostelRent'


class Feehostelrentdetails(models.Model):
    hostelid = models.ForeignKey(Feehostel, models.DO_NOTHING, db_column='hostelid')
    roomrent = models.FloatField(blank=True, null=True)
    hostelroomrentstatus = models.BigIntegerField()
    hostelroomrentdate = models.DateField()

    class Meta:
        managed = False
        db_table = 'feeHostelRentDetails'
        unique_together = (('hostelid', 'hostelroomrentstatus', 'hostelroomrentdate'),)


class Feehostelstudentdetails(models.Model):
    id = models.ForeignKey('Feehostelstudentmaster', models.DO_NOTHING, db_column='id')
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid')
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    status = models.CharField(max_length=1)
    feesubtypeid = models.BigIntegerField(blank=True, null=True)
    recieptno = models.CharField(max_length=30, blank=True, null=True)
    hid = models.BigAutoField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeHostelStudentDetails'
        unique_together = (('id', 'studentid'),)


class Feehostelstudentmaster(models.Model):
    id = models.BigAutoField(primary_key=True)
    hostelid = models.ForeignKey(Feehostel, models.DO_NOTHING, db_column='hostelid')
    admissionyear = models.BigIntegerField(blank=True, null=True)
    courseid = models.ForeignKey(Acdcourse, models.DO_NOTHING, db_column='courseid')
    duedate = models.DateField()
    rentfrom = models.DateField()
    rentto = models.DateField()
    days = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'feeHostelStudentMaster'


class Feeindexfeemaintypeall(models.Model):
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid', blank=True, null=True)
    recieptno = models.ForeignKey('Feereciept', models.DO_NOTHING, db_column='recieptno', primary_key=True)
    promotstatus = models.BigIntegerField(blank=True, null=True)
    currentindex = models.BigIntegerField(blank=True, null=True)
    nextindex = models.BigIntegerField(blank=True, null=True)
    currentindexstatus = models.BigIntegerField(blank=True, null=True)
    nextindexstatus = models.BigIntegerField(blank=True, null=True)
    exceptionstatus = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeIndexFeeMainTypeAll'


class Feeindexfeemaintypelast(models.Model):
    studentid = models.BigIntegerField(primary_key=True)
    currentindex = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeIndexFeeMainTypeLast'


class Feelog(models.Model):
    recieptno = models.CharField(max_length=30, blank=True, null=True)
    process = models.CharField(max_length=30, blank=True, null=True)
    empcode = models.CharField(max_length=20, blank=True, null=True)
    ipaddress = models.GenericIPAddressField(blank=True, null=True)
    crdate = models.DateTimeField(blank=True, null=True)
    total = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeLog'


class Feenamecommon(models.Model):
    feenamecommon = models.CharField(max_length=50, blank=True, null=True)
    feenamecommonid = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'feeNameCommon'


class Feeprovisionaladmission(models.Model):
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid', primary_key=True)
    number = models.BigIntegerField(blank=True, null=True)
    year = models.BigIntegerField(blank=True, null=True)
    courseid = models.ForeignKey(Acdcourse, models.DO_NOTHING, db_column='courseid', blank=True, null=True)
    applicationnumber = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeProvisionalAdmission'


class Feereciept(models.Model):
    recieptno = models.CharField(primary_key=True, max_length=20)
    transactionid = models.BigAutoField(unique=True)
    reciepter = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='reciepter', blank=True, null=True)
    typeofpaymentid = models.ForeignKey('Feetypeofpayment', models.DO_NOTHING, db_column='typeofpaymentid', blank=True, null=True)
    transactiondate = models.DateField(blank=True, null=True)
    accountid = models.BigIntegerField(blank=True, null=True)
    vouchermasterid = models.BigIntegerField(blank=True, null=True)
    recieptcancelornot = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeReciept'


class Feerecieptreset(models.Model):
    recieptcount = models.BigIntegerField()
    month = models.BigIntegerField()
    year = models.BigIntegerField()
    flagreset = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'feeRecieptReset'
        unique_together = (('month', 'year', 'flagreset'),)


class Feerefund(models.Model):
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid')
    feesubtypeid = models.ForeignKey(Feefeesubtype, models.DO_NOTHING, db_column='feesubtypeid')
    refundeddate = models.DateField(blank=True, null=True)
    refundmasterid = models.ForeignKey('Feerefunddetailsmaster', models.DO_NOTHING, db_column='refundmasterid', blank=True, null=True)
    feeamountrefund = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    feeamounttype = models.CharField(max_length=10, blank=True, null=True)
    refunddesc = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeRefund'
        unique_together = (('studentid', 'feesubtypeid', 'refundmasterid'),)


class Feerefunddetails(models.Model):
    refundid = models.BigAutoField(primary_key=True)
    refundamounttype = models.CharField(max_length=2, blank=True, null=True)
    accountid = models.BigIntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bankbranch = models.CharField(max_length=50, blank=True, null=True)
    chequeno = models.CharField(max_length=30, blank=True, null=True)
    chequedate = models.DateField(blank=True, null=True)
    refundmasterid = models.ForeignKey('Feerefunddetailsmaster', models.DO_NOTHING, db_column='refundmasterid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeRefundDetails'


class Feerefunddetailsmaster(models.Model):
    refundmasterid = models.BigAutoField(primary_key=True)
    refunddate = models.DateField(blank=True, null=True)
    cancelled = models.NullBooleanField()
    posted = models.NullBooleanField()
    refundto = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='refundto', blank=True, null=True)
    refundmodeid = models.ForeignKey('Feerefundmode', models.DO_NOTHING, db_column='refundmodeid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeRefundDetailsMaster'


class Feerefundmode(models.Model):
    refundmodeid = models.BigIntegerField(primary_key=True)
    refundmode = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeRefundMode'


class Feerefundpostdetails(models.Model):
    refundpostmasterid = models.ForeignKey('Feerefundpostmaster', models.DO_NOTHING, db_column='refundpostmasterid')
    refundid = models.ForeignKey(Feerefunddetails, models.DO_NOTHING, db_column='refundid')

    class Meta:
        managed = False
        db_table = 'feeRefundPostDetails'


class Feerefundpostmaster(models.Model):
    refundpostmasterid = models.BigAutoField(primary_key=True)
    refundpostdate = models.DateField(blank=True, null=True)
    vouchermasterid = models.ForeignKey(Accvouchermaster, models.DO_NOTHING, db_column='vouchermasterid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeRefundPostMaster'


class Feestudentbus(models.Model):
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid', primary_key=True)
    busboardingpointid = models.ForeignKey(Feebusboardingpoint, models.DO_NOTHING, db_column='busboardingpointid', blank=True, null=True)
    bususingdays = models.BigIntegerField(blank=True, null=True)
    datefrom = models.DateField(blank=True, null=True)
    busstatus = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeStudentBus'


class Feestudentcommonfeehistory(models.Model):
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid')
    feemaintypeid = models.ForeignKey(Feefeemaintype, models.DO_NOTHING, db_column='feemaintypeid')
    feedate = models.DateField(blank=True, null=True)
    usingdays = models.BigIntegerField(blank=True, null=True)
    recieptno = models.CharField(max_length=20, blank=True, null=True)
    boardingpoint = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeStudentCommonFeeHistory'


class Feestudenthostel(models.Model):
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid', primary_key=True)
    hostelid = models.ForeignKey(Feehostel, models.DO_NOTHING, db_column='hostelid', blank=True, null=True)
    hostelstatus = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeStudentHostel'


class Feestudentjoin(models.Model):
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid')
    feemaintypeid = models.ForeignKey(Feefeemaintype, models.DO_NOTHING, db_column='feemaintypeid')
    feejoindate = models.DateField(blank=True, null=True)
    lastpaiddate = models.DateField(blank=True, null=True)
    noofpaidcount = models.BigIntegerField(blank=True, null=True)
    usingdays = models.BigIntegerField(blank=True, null=True)
    initialrecieptno = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeStudentJoin'
        unique_together = (('studentid', 'feemaintypeid'),)


class Feestudentmess(models.Model):
    studentid = models.BigIntegerField()
    messchargedate = models.DateField()
    messamount = models.FloatField(blank=True, null=True)
    messchargeduedate = models.DateField(blank=True, null=True)
    status = models.BigIntegerField(blank=True, null=True)
    feesubtypeid = models.BigIntegerField(blank=True, null=True)
    recieptno = models.CharField(max_length=20, blank=True, null=True)
    mid = models.BigAutoField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeStudentMess'


class Feestudentpaymentmode(models.Model):
    courseid = models.ForeignKey(Acdcourse, models.DO_NOTHING, db_column='courseid')
    coursefeedesc = models.CharField(max_length=30)
    paymenttime = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeStudentPaymentMode'
        unique_together = (('coursefeedesc', 'courseid'),)


class Feestudenttypedetails(models.Model):
    studtypeid = models.BigAutoField(primary_key=True)
    admissionyear = models.BigIntegerField(blank=True, null=True)
    seattypeid = models.ForeignKey(Acdseatsubtype, models.DO_NOTHING, db_column='seattypeid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeStudentTypeDetails'


class Feetransactions(models.Model):
    transactionid = models.ForeignKey(Feereciept, models.DO_NOTHING, db_column='transactionid')
    feesubtypeid = models.ForeignKey(Feefeesubtype, models.DO_NOTHING, db_column='feesubtypeid')
    feesubtypeamount = models.DecimalField(max_digits=65535, decimal_places=65535)

    class Meta:
        managed = False
        db_table = 'feeTransactions'
        unique_together = (('transactionid', 'feesubtypeid', 'feesubtypeamount'),)


class Feetypeofpayment(models.Model):
    typeofpaymentid = models.BigAutoField(primary_key=True)
    typeofpaymentdesc = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeTypeOfPayment'


class Gengroupdetails(models.Model):
    groupid = models.BigIntegerField(primary_key=True)
    groupcode = models.CharField(max_length=20, blank=True, null=True)
    groupname = models.CharField(max_length=-1, blank=True, null=True)
    maingroup = models.ForeignKey('Gengroups', models.DO_NOTHING, db_column='maingroup', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genGroupDetails'


class Gengroups(models.Model):
    maingroup = models.CharField(primary_key=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'genGroups'


class Genstaffgroup(models.Model):
    staffid = models.ForeignKey(Acdstaffdetails, models.DO_NOTHING, db_column='staffid', blank=True, null=True)
    groupid = models.ForeignKey(Gengroupdetails, models.DO_NOTHING, db_column='groupid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genStaffGroup'
        unique_together = (('staffid', 'groupid'),)


class Hrmacademicdetails(models.Model):
    autoincid = models.BigAutoField(blank=True, null=True)
    id = models.ForeignKey('Hrminterviewdetails', models.DO_NOTHING, db_column='id')
    qid = models.ForeignKey('Hrmqualificationmaster', models.DO_NOTHING, db_column='qid')
    cid = models.BigIntegerField()
    yop = models.CharField(max_length=5)
    marktype = models.CharField(max_length=20)
    mark = models.CharField(max_length=20)
    institute = models.CharField(max_length=500, blank=True, null=True)
    rank = models.CharField(max_length=10)
    university = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmAcademicDetails'
        unique_together = (('id', 'qid', 'cid'),)


class Hrmachievementcategory(models.Model):
    achcategoryid = models.SmallIntegerField(primary_key=True)
    achcategoryname = models.CharField(unique=True, max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmAchievementCategory'


class Hrmachievementdetails(models.Model):
    achid = models.SmallIntegerField(primary_key=True)
    personalid = models.ForeignKey('Hrmbasicinfo', models.DO_NOTHING, db_column='personalid', blank=True, null=True)
    achcategoryid = models.ForeignKey(Hrmachievementcategory, models.DO_NOTHING, db_column='achcategoryid', blank=True, null=True)
    achtypeid = models.ForeignKey('Hrmachievementtype', models.DO_NOTHING, db_column='achtypeid', blank=True, null=True)
    achdate = models.DateField(blank=True, null=True)
    entrydate = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmAchievementDetails'


class Hrmachievementtype(models.Model):
    achtypeid = models.SmallIntegerField(primary_key=True)
    achtype = models.CharField(unique=True, max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmAchievementType'


class Hrmadditionalduty(models.Model):
    adddutyid = models.SmallIntegerField(primary_key=True)
    personalid = models.ForeignKey('Hrmbasicinfo', models.DO_NOTHING, db_column='personalid', blank=True, null=True)
    dutyassigned = models.CharField(max_length=300, blank=True, null=True)
    natureid = models.ForeignKey('Hrmadditionaldutynature', models.DO_NOTHING, db_column='natureid', blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmAdditionalDuty'


class Hrmadditionaldutynature(models.Model):
    natureid = models.SmallIntegerField(primary_key=True)
    nature = models.CharField(unique=True, max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmAdditionalDutyNature'


class Hrmappointmentnature(models.Model):
    appnatureid = models.SmallIntegerField(primary_key=True)
    appnature = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmAppointmentNature'


class Hrmbasicinfo(models.Model):
    personalid = models.BigAutoField(primary_key=True)
    empcode = models.CharField(max_length=15)
    empcategid = models.ForeignKey('Hrmemployeecategory', models.DO_NOTHING, db_column='empcategid', blank=True, null=True)
    did = models.ForeignKey('Hrmdepartment', models.DO_NOTHING, db_column='did')
    desigid = models.ForeignKey('Hrmdesignation', models.DO_NOTHING, db_column='desigid')
    doj = models.DateField()
    appnatureid = models.ForeignKey(Hrmappointmentnature, models.DO_NOTHING, db_column='appnatureid', blank=True, null=True)
    fullname = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=6)
    maritalstatus = models.CharField(max_length=20, blank=True, null=True)
    religionid = models.ForeignKey(Acdreligion, models.DO_NOTHING, db_column='religionid', blank=True, null=True)
    casteid = models.ForeignKey(Acdcaste, models.DO_NOTHING, db_column='casteid', blank=True, null=True)
    scst = models.CharField(max_length=5, blank=True, null=True)
    telephres = models.CharField(max_length=15, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    bloodgroup = models.CharField(max_length=20, blank=True, null=True)
    bankacno = models.CharField(max_length=30, blank=True, null=True)
    bankname = models.CharField(max_length=300, blank=True, null=True)
    pancardno = models.CharField(max_length=30, blank=True, null=True)
    permaddr1 = models.CharField(max_length=500, blank=True, null=True)
    permaddr2 = models.CharField(max_length=300, blank=True, null=True)
    permaddr3 = models.CharField(max_length=300, blank=True, null=True)
    permpin = models.CharField(max_length=10, blank=True, null=True)
    tempaddr1 = models.CharField(max_length=500, blank=True, null=True)
    tempaddr2 = models.CharField(max_length=300, blank=True, null=True)
    tempaddr3 = models.CharField(max_length=300, blank=True, null=True)
    temppin = models.CharField(max_length=10, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    entrystatus = models.CharField(max_length=30, blank=True, null=True)
    whetheractive = models.CharField(max_length=5, blank=True, null=True)
    currentstafflevel = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmBasicInfo'


class Hrmcertificates(models.Model):
    certifid = models.BigAutoField(primary_key=True)
    personalid = models.ForeignKey(Hrmbasicinfo, models.DO_NOTHING, db_column='personalid', blank=True, null=True)
    qid = models.ForeignKey('Hrmqualificationmaster', models.DO_NOTHING, db_column='qid', blank=True, null=True)
    issuedate = models.DateField(blank=True, null=True)
    receiveddate = models.DateField(blank=True, null=True)
    issuedby = models.ForeignKey(Hrmbasicinfo, models.DO_NOTHING, db_column='issuedby', blank=True, null=True)
    receivedby = models.ForeignKey(Hrmbasicinfo, models.DO_NOTHING, db_column='receivedby', blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmCertificates'


class Hrmcoursetypemaster(models.Model):
    coursetypeid = models.SmallIntegerField(primary_key=True)
    coursetypename = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmCourseTypeMaster'


class Hrmdepartment(models.Model):
    did = models.SmallIntegerField(primary_key=True)
    department = models.CharField(unique=True, max_length=100)
    deptcode = models.CharField(unique=True, max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmDepartment'


class Hrmdesciplinaryactions(models.Model):
    descid = models.SmallIntegerField(primary_key=True)
    personalid = models.ForeignKey(Hrmbasicinfo, models.DO_NOTHING, db_column='personalid', blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmDesciplinaryActions'


class Hrmdesignation(models.Model):
    desigid = models.AutoField(primary_key=True)
    desig = models.CharField(unique=True, max_length=200)
    dimendesigcode = models.CharField(max_length=20, blank=True, null=True)
    payrollcode = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmDesignation'


class Hrmeducationalqualifications(models.Model):
    personalid = models.ForeignKey(Hrmbasicinfo, models.DO_NOTHING, db_column='personalid')
    qid = models.ForeignKey('Hrmqualificationmaster', models.DO_NOTHING, db_column='qid')
    cid = models.BigIntegerField()
    coursetypeid = models.ForeignKey(Hrmcoursetypemaster, models.DO_NOTHING, db_column='coursetypeid', blank=True, null=True)
    yop = models.CharField(max_length=5)
    marktype = models.CharField(max_length=20)
    mark = models.CharField(max_length=20)
    institute = models.CharField(max_length=500, blank=True, null=True)
    rank = models.CharField(max_length=5)
    university = models.CharField(max_length=300, blank=True, null=True)
    certificate = models.CharField(max_length=5, blank=True, null=True)
    qualified = models.CharField(max_length=10, blank=True, null=True)
    qualifieddate = models.DateField(blank=True, null=True)
    certificatestatus = models.CharField(max_length=20, blank=True, null=True)
    certificatelastupdateid = models.ForeignKey(Hrmcertificates, models.DO_NOTHING, db_column='certificatelastupdateid', blank=True, null=True)
    autoincid = models.BigAutoField(blank=True, null=True)
    periodmonthfrom = models.CharField(max_length=20, blank=True, null=True)
    periodyearfrom = models.CharField(max_length=5, blank=True, null=True)
    periodmonthto = models.CharField(max_length=20, blank=True, null=True)
    periodyearto = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmEducationalQualifications'
        unique_together = (('personalid', 'qid', 'cid'),)


class Hrmemployeecategory(models.Model):
    categid = models.SmallIntegerField(primary_key=True)
    categname = models.CharField(unique=True, max_length=150)
    leaveapplicable = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmEmployeeCategory'


class Hrmexperience(models.Model):
    autoincid = models.AutoField(blank=True, null=True)
    id = models.ForeignKey('Hrminterviewdetails', models.DO_NOTHING, db_column='id')
    organization = models.CharField(max_length=500)
    orgaddr1 = models.CharField(max_length=300, blank=True, null=True)
    orgaddr2 = models.CharField(max_length=300, blank=True, null=True)
    designation = models.CharField(max_length=200)
    expfrom = models.DateField()
    expto = models.DateField()
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmExperience'
        unique_together = (('id', 'organization', 'designation'),)


class Hrmexperiencetypemaster(models.Model):
    exptypeid = models.SmallIntegerField(primary_key=True)
    exptypename = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmExperienceTypeMaster'


class Hrmfamilydetails(models.Model):
    personalid = models.BigAutoField()
    employeecode = models.CharField(max_length=15)
    familymember = models.CharField(max_length=60)
    relationshipid = models.ForeignKey(Acdrelationship, models.DO_NOTHING, db_column='relationshipid', blank=True, null=True)
    dateofbirth = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmFamilyDetails'


class Hrminterviewdetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    cname = models.CharField(max_length=200)
    gender = models.CharField(max_length=3)
    dob = models.DateField()
    paddr1 = models.CharField(max_length=500)
    paddr2 = models.CharField(max_length=300, blank=True, null=True)
    paddr3 = models.CharField(max_length=300, blank=True, null=True)
    ppin = models.CharField(max_length=6)
    caddr1 = models.CharField(max_length=500)
    caddr2 = models.CharField(max_length=300, blank=True, null=True)
    caddr3 = models.CharField(max_length=300, blank=True, null=True)
    cpin = models.CharField(max_length=6)
    landphone = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=50)
    email = models.CharField(max_length=150, blank=True, null=True)
    postapplied = models.CharField(max_length=150)
    dept = models.CharField(max_length=150)
    doj = models.DateField(blank=True, null=True)
    interviewrank = models.IntegerField(blank=True, null=True)
    interviewdate = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=30)
    remarks = models.TextField(blank=True, null=True)
    dateofapply = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmInterviewDetails'


class Hrmleaveactionmaster(models.Model):
    actionid = models.SmallIntegerField(primary_key=True)
    actionname = models.CharField(unique=True, max_length=100, blank=True, null=True)
    whethereffectonleave = models.CharField(max_length=5, blank=True, null=True)
    suffixtext = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmLeaveActionMaster'


class Hrmleavealtarrangements(models.Model):
    altarrangementid = models.BigAutoField(primary_key=True)
    leaveapplicationid = models.ForeignKey('Hrmleaveapplications', models.DO_NOTHING, db_column='leaveapplicationid', blank=True, null=True)
    datearranged = models.DateField(blank=True, null=True)
    period = models.SmallIntegerField(blank=True, null=True)
    branchid = models.BigIntegerField(blank=True, null=True)
    substituentid = models.BigIntegerField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmLeaveAltArrangements'


class Hrmleaveapplications(models.Model):
    leaveapplicationid = models.BigAutoField(primary_key=True)
    personalid = models.ForeignKey(Hrmbasicinfo, models.DO_NOTHING, db_column='personalid', blank=True, null=True)
    leavetypeid = models.ForeignKey('Hrmleavetypemaster', models.DO_NOTHING, db_column='leavetypeid', blank=True, null=True)
    leavefrom = models.DateField(blank=True, null=True)
    leaveto = models.DateField(blank=True, null=True)
    leavedays = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    halfdayleave = models.CharField(max_length=5, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    applydate = models.DateField(blank=True, null=True)
    process_statusid = models.ForeignKey('Hrmleaveprocessing', models.DO_NOTHING, db_column='process_statusid', blank=True, null=True)
    whichyears = models.SmallIntegerField(blank=True, null=True)
    processingtype = models.CharField(max_length=30, blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)
    rejoindate = models.DateField(blank=True, null=True)
    alternatearrangement = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmLeaveApplications'


class Hrmleavecompensatory(models.Model):
    compensatoryid = models.BigIntegerField(primary_key=True)
    leaveapplicationid = models.ForeignKey(Hrmleaveapplications, models.DO_NOTHING, db_column='leaveapplicationid', blank=True, null=True)
    fromdate = models.DateField(blank=True, null=True)
    todate = models.DateField(blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmLeaveCompensatory'


class Hrmleaveemployeewise(models.Model):
    leaveempwiseid = models.BigAutoField(primary_key=True)
    personalid = models.ForeignKey(Hrmbasicinfo, models.DO_NOTHING, db_column='personalid', blank=True, null=True)
    totleaves = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    leavetypeid = models.ForeignKey('Hrmleavetypemaster', models.DO_NOTHING, db_column='leavetypeid', blank=True, null=True)
    leaveyear = models.SmallIntegerField(blank=True, null=True)
    categid = models.ForeignKey(Hrmemployeecategory, models.DO_NOTHING, db_column='categid', blank=True, null=True)
    leavesetupid = models.ForeignKey('Hrmleavesetup', models.DO_NOTHING, db_column='leavesetupid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmLeaveEmployeeWise'


class Hrmleaveprocessing(models.Model):
    processid = models.BigAutoField(primary_key=True)
    leaveapplicationid = models.ForeignKey(Hrmleaveapplications, models.DO_NOTHING, db_column='leaveapplicationid', blank=True, null=True)
    fromstaffid = models.ForeignKey(Hrmbasicinfo, models.DO_NOTHING, db_column='fromstaffid', blank=True, null=True)
    tostaffid = models.ForeignKey(Hrmbasicinfo, models.DO_NOTHING, db_column='tostaffid', blank=True, null=True)
    actionid = models.ForeignKey(Hrmleaveactionmaster, models.DO_NOTHING, db_column='actionid', blank=True, null=True)
    remark = models.CharField(max_length=500, blank=True, null=True)
    whethercurrent = models.IntegerField(blank=True, null=True)
    dateofprocessing = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmLeaveProcessing'


class Hrmleavesetup(models.Model):
    leavesetupid = models.SmallIntegerField(primary_key=True)
    leavetypeid = models.ForeignKey('Hrmleavetypemaster', models.DO_NOTHING, db_column='leavetypeid', blank=True, null=True)
    categid = models.ForeignKey(Hrmemployeecategory, models.DO_NOTHING, db_column='categid', blank=True, null=True)
    totalleaves = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setupyear = models.SmallIntegerField(blank=True, null=True)
    setupdate = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmLeaveSetup'
        unique_together = (('leavetypeid', 'categid', 'setupyear'),)


class Hrmleavetypemaster(models.Model):
    leavetypeid = models.SmallIntegerField(primary_key=True)
    leavetype = models.CharField(unique=True, max_length=200, blank=True, null=True)
    whethercumulative = models.CharField(max_length=5, blank=True, null=True)
    cumulativeyears = models.SmallIntegerField(blank=True, null=True)
    listingorder = models.SmallIntegerField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmLeaveTypeMaster'


class Hrmotherinfo(models.Model):
    personalid = models.BigIntegerField(primary_key=True)
    exserviceman = models.TextField(blank=True, null=True)
    handicapped = models.TextField(blank=True, null=True)
    trainingknowlede = models.TextField(blank=True, null=True)
    careerinfo = models.TextField(blank=True, null=True)
    dissmissals = models.TextField(blank=True, null=True)
    illness = models.TextField(blank=True, null=True)
    offence = models.TextField(blank=True, null=True)
    fathersinfo = models.TextField(blank=True, null=True)
    spouseinfo = models.TextField(blank=True, null=True)
    siblingsinfo = models.TextField(blank=True, null=True)
    relations = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmOtherInfo'


class Hrmpreviousexperience(models.Model):
    autoincid = models.AutoField(primary_key=True)
    exppersonid = models.BigIntegerField()
    organization = models.CharField(max_length=500)
    orgaddr1 = models.CharField(max_length=300, blank=True, null=True)
    orgaddr2 = models.CharField(max_length=300, blank=True, null=True)
    designation = models.CharField(max_length=300)
    emoluments = models.CharField(max_length=100, blank=True, null=True)
    expfrom = models.DateField()
    expto = models.DateField()
    remarks = models.TextField(blank=True, null=True)
    enclosed = models.CharField(max_length=15, blank=True, null=True)
    exptypeid = models.ForeignKey(Hrmexperiencetypemaster, models.DO_NOTHING, db_column='exptypeid', blank=True, null=True)
    coursetaught = models.CharField(max_length=150, blank=True, null=True)
    subjecttaught = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmPreviousExperience'
        unique_together = (('exppersonid', 'organization', 'designation'),)


class Hrmpromotiondetails(models.Model):
    promotionid = models.AutoField(primary_key=True)
    personalid = models.ForeignKey(Hrmbasicinfo, models.DO_NOTHING, db_column='personalid', blank=True, null=True)
    deptbeforeid = models.ForeignKey(Hrmdepartment, models.DO_NOTHING, db_column='deptbeforeid', blank=True, null=True)
    desigbeforeid = models.ForeignKey(Hrmdesignation, models.DO_NOTHING, db_column='desigbeforeid', blank=True, null=True)
    deptafterid = models.ForeignKey(Hrmdepartment, models.DO_NOTHING, db_column='deptafterid', blank=True, null=True)
    desigafterid = models.ForeignKey(Hrmdesignation, models.DO_NOTHING, db_column='desigafterid', blank=True, null=True)
    dateofpromo = models.DateField(blank=True, null=True)
    remarks = models.CharField(max_length=500, blank=True, null=True)
    payrollconfirmation = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmPromotionDetails'


class Hrmqualificationlevelmaster(models.Model):
    qualilevelid = models.BigAutoField(primary_key=True)
    levelname = models.CharField(unique=True, max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmQualificationLevelMaster'


class Hrmqualificationmaster(models.Model):
    qid = models.SmallIntegerField(primary_key=True)
    qualification = models.CharField(unique=True, max_length=200)
    qualilevelid = models.ForeignKey(Hrmqualificationlevelmaster, models.DO_NOTHING, db_column='qualilevelid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmQualificationMaster'


class Hrmresignation(models.Model):
    resignationid = models.SmallIntegerField(primary_key=True)
    leavingtype = models.CharField(max_length=47, blank=True, null=True)
    dues = models.CharField(max_length=5, blank=True, null=True)
    dueremarks = models.CharField(max_length=500, blank=True, null=True)
    resignationdate = models.DateField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    personalid = models.ForeignKey(Hrmbasicinfo, models.DO_NOTHING, db_column='personalid', blank=True, null=True)
    dateofentry = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmResignation'


class Hrmsalarydetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    personalid = models.ForeignKey(Hrmbasicinfo, models.DO_NOTHING, db_column='personalid', blank=True, null=True)
    joindesignationid = models.ForeignKey(Hrmdesignation, models.DO_NOTHING, db_column='joindesignationid', blank=True, null=True)
    jointotalsalary = models.CharField(max_length=15, blank=True, null=True)
    joinscaleofpay = models.CharField(max_length=50, blank=True, null=True)
    presentscaleofpay = models.CharField(max_length=50, blank=True, null=True)
    presentbasic = models.CharField(max_length=15, blank=True, null=True)
    presenttotal = models.CharField(max_length=15, blank=True, null=True)
    lwatotalcount = models.IntegerField(blank=True, null=True)
    lwauptodate = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmSalaryDetails'


class Hrmspecialization(models.Model):
    sid = models.SmallIntegerField(primary_key=True)
    specialization = models.CharField(max_length=200)
    qid = models.ForeignKey(Hrmqualificationmaster, models.DO_NOTHING, db_column='qid')

    class Meta:
        managed = False
        db_table = 'hrmSpecialization'


class Hrmstafflevelassignment(models.Model):
    levelassignid = models.BigAutoField(primary_key=True)
    personalid = models.ForeignKey(Hrmbasicinfo, models.DO_NOTHING, db_column='personalid', blank=True, null=True)
    did = models.SmallIntegerField(blank=True, null=True)
    leveltypeid = models.ForeignKey('Hrmstaffleveltype', models.DO_NOTHING, db_column='leveltypeid', blank=True, null=True)
    fromdate = models.DateField(blank=True, null=True)
    todate = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    whetheravailable = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmStaffLevelAssignment'


class Hrmstaffleveltype(models.Model):
    leveltypeid = models.SmallIntegerField(primary_key=True)
    leveltype = models.CharField(unique=True, max_length=150, blank=True, null=True)
    levelno = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hrmStaffLevelType'


class Itnachievement(models.Model):
    acheivementid = models.BigAutoField(primary_key=True)
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid')
    achievementtypeid = models.ForeignKey('Itnachievementtype', models.DO_NOTHING, db_column='achievementtypeid')
    dateofachievement = models.DateField()
    description = models.TextField(blank=True, null=True)
    achievementfrom = models.CharField(max_length=200, blank=True, null=True)
    enteredby = models.BigIntegerField()
    teamornot = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'itnAchievement'


class Itnachievementtype(models.Model):
    achievementtypeid = models.BigAutoField(primary_key=True)
    achievementtypedesc = models.CharField(unique=True, max_length=200)

    class Meta:
        managed = False
        db_table = 'itnAchievementType'


class Itndesciplinaryaction(models.Model):
    actionid = models.BigAutoField(primary_key=True)
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid')
    actiontypeid = models.ForeignKey('Itndesciplinaryactiontype', models.DO_NOTHING, db_column='actiontypeid')
    description = models.TextField()
    actiondate = models.DateField()
    actionfrom = models.DateField(blank=True, null=True)
    actionto = models.DateField(blank=True, null=True)
    actiontakenby = models.CharField(max_length=100)
    enteredby = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'itnDesciplinaryAction'


class Itndesciplinaryactiontype(models.Model):
    actiontypeid = models.BigAutoField(primary_key=True)
    actiondesc = models.CharField(unique=True, max_length=200)

    class Meta:
        managed = False
        db_table = 'itnDesciplinaryActionType'


class Itnnews(models.Model):
    newsid = models.BigAutoField(primary_key=True)
    newsdate = models.DateField()
    newscontent = models.TextField()
    expirydate = models.DateField()
    priority = models.SmallIntegerField(blank=True, null=True)
    postedby = models.ForeignKey(Acdstaffdetails, models.DO_NOTHING, db_column='postedby', blank=True, null=True)
    users = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'itnNews'


class Itnnewsfile(models.Model):
    newsid = models.ForeignKey(Itnnews, models.DO_NOTHING, db_column='newsid')
    location = models.CharField(max_length=200)
    filetype = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'itnNewsFile'


class Logerrorfindcode(models.Model):
    errorcode = models.CharField(primary_key=True, max_length=20)
    errordetails = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logErrorFindCode'


class Maximummark1(models.Model):
    maximummark = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maximummark1'


class Maximummark2(models.Model):
    maximummark = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maximummark2'


class Maxmarkassignments(models.Model):
    max = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maxmarkassignments'


class Plcactivities(models.Model):
    activityid = models.BigIntegerField(primary_key=True)
    activityname = models.CharField(db_column='activityName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    activitydesc = models.CharField(db_column='activityDesc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    regstartdate = models.DateField(blank=True, null=True)
    regenddate = models.DateField(blank=True, null=True)
    passingyear = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plcActivities'


class Plcactivitybatches(models.Model):
    activityid = models.BigIntegerField(blank=True, null=True)
    activityspecializationid = models.ForeignKey(Acdspecialization, models.DO_NOTHING, db_column='activityspecializationid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plcActivityBatches'


class Plcactivitystudents(models.Model):
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid')
    activityid = models.ForeignKey(Plcactivities, models.DO_NOTHING, db_column='activityid')
    registrationdate = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plcActivityStudents'
        unique_together = (('studentid', 'activityid'),)


class Plcagencies(models.Model):
    agencyid = models.BigIntegerField(primary_key=True)
    agencyname = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plcAgencies'


class Plccompanies(models.Model):
    companyid = models.BigIntegerField(primary_key=True)
    companyname = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plcCompanies'


class Plcplacedstudents(models.Model):
    studentid = models.BigIntegerField()
    companyid = models.ForeignKey(Plccompanies, models.DO_NOTHING, db_column='companyid')
    ctc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    placeddate = models.DateField(blank=True, null=True)
    agencyid = models.ForeignKey(Plcagencies, models.DO_NOTHING, db_column='agencyid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plcPlacedStudents'
        unique_together = (('studentid', 'companyid'),)


class Plcuniversityaggmarkdetails(models.Model):
    studentid = models.BigIntegerField(primary_key=True)
    aggregatemarkpercentage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currentbacklogcount = models.IntegerField(blank=True, null=True)
    historybacklogcount = models.IntegerField(blank=True, null=True)
    markuptosemester = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plcUniversityAggMarkDetails'


class Plcuniversitymarkdetails(models.Model):
    studentid = models.ForeignKey(Acdstudentadmissiondetails, models.DO_NOTHING, db_column='studentid')
    breakid = models.ForeignKey(Acdcoursetypebreaks, models.DO_NOTHING, db_column='breakid')
    maxmark = models.IntegerField(blank=True, null=True)
    markobtained = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plcUniversityMarkDetails'
        unique_together = (('studentid', 'breakid'),)


class Recieptprintdetails(models.Model):
    recieptno = models.CharField(max_length=20, blank=True, null=True)
    printcount = models.IntegerField(blank=True, null=True)
    lastprintdate = models.DateField(blank=True, null=True)
    printedby = models.CharField(max_length=20, blank=True, null=True)
    printedsystem = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recieptPrintDetails'


class StkSample(models.Model):
    samplefield = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'stk_sample'


class Stksample2(models.Model):
    sampleid = models.IntegerField(blank=True, null=True)
    samplefield = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stksample2'


class Studentcount(models.Model):
    count = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'studentcount'


class Temp(models.Model):
    admissionnumber = models.CharField(max_length=20, blank=True, null=True)
    studentname = models.CharField(max_length=100, blank=True, null=True)
    vchmasterida = models.BigIntegerField(blank=True, null=True)
    vchmasteridb = models.BigIntegerField(blank=True, null=True)
    vouchernumber = models.BigIntegerField(blank=True, null=True)
    refno = models.CharField(max_length=20, blank=True, null=True)
    financialyear = models.BigIntegerField(blank=True, null=True)
    accountid = models.BigIntegerField(blank=True, null=True)
    debitamount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    creditamount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    narration = models.CharField(max_length=250, blank=True, null=True)
    current = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'temp'


class Tempatt(models.Model):
    dt = models.DateField(blank=True, null=True)
    studentid = models.IntegerField(blank=True, null=True)
    cnttot = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tempatt'


class Tempattpre(models.Model):
    dt = models.DateField(blank=True, null=True)
    studentid = models.IntegerField(blank=True, null=True)
    cntpre = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tempattpre'


class Tempmathews(models.Model):
    studentname = models.CharField(max_length=50, blank=True, null=True)
    fathersname = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tempmathews'
