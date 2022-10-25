
class BaseModel(object):
    _fields_ = ()

    @classmethod
    def fields(cls):
        return cls._fields_

    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return getattr(self, key)


class PlacePaperModel(BaseModel):

    _fields_ = ('id', 'bmh', 'ksbh', 'bkdwdm', 'bkdwmc', 'xm', 'kch', 'zch', 'kmdm', 'kmmc', 'unit', 'number')

    def __init__(self, id, bmh, ksbh, bkdwdm, bkdwmc, xm, kch, zch, kmdm, kmmc, unit, number):
        self.id = id
        self.bmh = bmh
        self.ksbh = ksbh
        self.bkdwdm = bkdwdm
        self.bkdwmc = bkdwmc
        self.xm = xm
        self.kch = kch
        self.zch = zch
        self.kmdm = kmdm
        self.kmmc = kmmc
        self.unit = unit
        self.number = number

    @property
    def group_id(self):
        return self.bkdwdm

    @property
    def sort_id(self):
        return self.bkdwdm + str(self.unit) + self.kmdm + self.ksbh

    def set_number(self, number):
        self.number = number
