from functools import wraps


def checkValue(valueType=None):
    def __deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in args:
                if not isinstance(i, valueType):
                    msg = '{0} 不是“{1}”'.format(i, valueType.__name__)
                    raise ValueError(msg)
            return func(*args, **kwargs)
        return wrapper
    return __deco


class Base:

    数字映射名字=[]

    def __init__(self, num):
        self.__num = num

    @property
    def name(self):
        return self.数字映射名字[self.__num]

    @property
    def num(self):
        return self.__num

    def __str__(self):
        return self.name


class 五行(Base):

    数字映射名字=[0, '木', '火', '土', '金', '水']

    def __init__(self, num):
        if num <= 0 or num >= 6:
            raise ValueError('输入的值为%s，输入值必是大于等于1小于等于5间的整数' % num)
        if not isinstance(num, int):
            raise ValueError('输入的值为%s，输入值必是大于等于1小于等于5间的整数' % num)
        super().__init__(num)


class 干(Base):

    数字映射名字 = [0, '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

    def __init__(self, num):
        if num <= 0 or num >= 11:
            raise ValueError('输入的值为%s，输入值必是大于等于1小于等于11间的整数' % num)
        if not isinstance(num, int):
            raise ValueError('输入的值为%s，输入值必是大于等于1小于等于11间的整数' % num)
        super().__init__(num)

    def __add__(self, other):
        if not isinstance(other, int):
            raise ValueError('%s 必须是整数' % other)
        tmp = (self.num + other + 10) % 10
        tmp = 10 if tmp == 0 else tmp
        return 干(tmp)

    def __sub__(self, other):
        if not isinstance(other, 干):
            raise ValueError('只能用于干与干间')
        return self.num - other.num

    def __eq__(self, other):
        if not isinstance(other, 干):
            raise ValueError('只能用于干与干间')
        return self.num == other.num

    def __ne__(self, other):
        if not isinstance(other, 干):
            raise ValueError('只能用于干与干间')
        return self.num != other.num

    def __getitem__(self, key):
        if key not in ['五行']:
            raise ValueError('{0} 不是“五行”'.format(key))
        return 五行((self.num + 1)//2)

    @property
    def wuxing(self):
        return 五行((self.num + 1)//2)

    @property
    def 属阳(self):
        return self.num % 2 != 0


class 支(Base):

    数字映射名字 = [0, '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑']

    def __init__(self, num):
        if num <= 0 or num >= 13:
            raise ValueError('输入的值为%s，输入值必是大于等于1小于等于12间的整数' % num)
        if not isinstance(num, int):
            raise ValueError('输入的值为%s，输入值必是大于等于1小于等于12间的整数' % num)
        super().__init__(num)

    def __add__(self, other):
        if not isinstance(other, int):
            raise ValueError('%s 必须是整数' % other)
        tmp = (self.num + other + 12) % 12
        tmp = 12 if tmp == 0 else tmp
        return 支(tmp)

    def __sub__(self, other):
        if not isinstance(other, 支):
            raise ValueError('只能用于支与支间')
        return self.num - other.num

    def __eq__(self, other):
        if not isinstance(other, 支):
            raise ValueError('只能用于支与支间')
        return self.num == other.num

    def __ne__(self, other):
        if not isinstance(other, 支):
            raise ValueError('只能用于支与支间')
        return self.num != other.num

    def __getitem__(self, key):
        if key not in ['五行']:
            raise ValueError('{0} 不是“五行”'.format(key))
        if self.num % 3 == 0:
            return 五行(3)
        return 五行(self.num//3 + self.num//7 + 1)

    @property
    def wuxing(self):
        if self.num % 3 == 0:
            return 五行(3)
        return 五行(self.num//3 + self.num//7 + 1)

    @property
    def 属阳(self):
        return self.num % 2 != 0


def 阴阳相同(a, b):
    '''
    可用于与干、支与支、干与支
    '''
    return (a.num - b.num) % 2 == 0


@checkValue(valueType=五行)
def 生(a, b):
    return (a.num - b.num - 4) % 5 == 0


@checkValue(valueType=五行)
def 克(a, b):
    return (a.num - b.num - 3) % 5 == 0


class 干支():
    '''
    a = 干支(干(2), 支(2))
    a['干'] == 干(2)
    a['支'] == 支(2)
    '''
    def __init__(self, a, b):
        if not isinstance(a, 干):
            raise ValueError('干支由干、支组，提供的不是干')
        if not isinstance(b, 支):
            raise ValueError('干支由干、支组，提供的不是支')

        if not 阴阳相同(a, b):
            raise ValueError('{0} {1}不配置'.format(a, b))

        self.__干 = a
        self.__支 = b

    def __str__(self):
        return '{0}{1}'.format(self.__干, self.__支)

    def __getitem__(self, key):
        if key not in ['干', '支']:
            raise ValueError('{0} 不是“干”或“支”'.format(key))
        return self.__干 if key == '干' else self.__支

    def __eq__(self, other):
        if not isinstance(other, 干支):
            raise ValueError('只能用于支与干支间')
        return self.__干 == other['干'] and self.__支 == other['支']

    def __ne__(self, other):
        if not isinstance(other, 干支):
            raise ValueError('只能用于支与干支间')
        return self.__干 != other['干'] or self.__支 != other['支']


@checkValue(valueType=干)
def 五合(a, b):
    if a == b:
        return False
    return (a.num - b.num) % 5 == 0


@checkValue(valueType=支)
def 三合(a, b, c):
    if 0 in (a.num - b.num, a.num - c.num, b.num - c.num):
        return False
    return (a.num - b.num) % 4 == 0 and (b.num - c.num) % 4 == 0


@checkValue(valueType=支)
def 获取三合(a):
    allSanhe = []
    for i in range(1, 13):
        for j in range(1, 13):
            for k in range(1, 13):
                if 三合(支(i), 支(j), 支(k)):
                    allSanhe.append((支(i), 支(j), 支(k)))
    tmpSanhe = []
    for i in allSanhe:
        if i[0] in [支(1), 支(4), 支(7), 支(10)] and \
           i[1] in [支(2), 支(5), 支(8), 支(11)]:
            tmpSanhe.append(i)
    allSanhe = tmpSanhe
    for i in allSanhe:
        if a in i:
            return i


@checkValue(valueType=支)
def 六合(a, b):
    return (a.num + b.num - 11) % 12 == 0


@checkValue(valueType=支)
def 六冲(a, b):
    if a == b:
        return False
    return (a.num - b.num) % 6 == 0


@checkValue(valueType=支)
def 获取六冲(a):
    for i in range(1, 13):
        if 六冲(a, 支(i)):
            return 支(i)


@checkValue(valueType=支)
def 刑(a, b):
    xin_group = []
    # 寅 巳 申
    xin_group.append((支(1), 支(4)))
    xin_group.append((支(4), 支(7)))
    xin_group.append((支(7), 支(1)))
    # 未 丑 戌
    xin_group.append((支(6), 支(12)))
    xin_group.append((支(12), 支(9)))
    xin_group.append((支(9), 支(6)))

    # 子 卯
    xin_group.append((支(2), 支(11)))
    xin_group.append((支(11), 支(2)))

    # 辰 午 酉 亥
    xin_group.append((支(3), 支(3)))
    xin_group.append((支(5), 支(5)))
    xin_group.append((支(8), 支(8)))
    xin_group.append((支(10), 支(10)))

    return (a, b) in xin_group
