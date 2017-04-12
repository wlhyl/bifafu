from prettytable import PrettyTable
from ganzhiwuxin import *
from shensha import *


class NoSanchuan(Exception):
    def __init__(self, msg):
        super().__init__()
        self.__msg = msg

    def __str__(self):
        return self.__msg


def 寄宫(g):
    寄宫映射 = [0, 1, 3, 4, 6, 4, 6, 7, 9, 10, 12]
    if not isinstance(g, 干):
        raise ValueError('只有干才有寄宫')
    return 支(寄宫映射[g.num])


class 天盘():
    '''
以寅上支标示天盘，方便__str__输出
a = 天盘(支(2), 支(1))
a[支(4)] 获取巳上神
    '''
    def __init__(self, 月将, 时辰):
        if not isinstance(月将, 支):
            raise ValueError("月将需要是地支class")

        if not isinstance(时辰, 支):
            raise ValueError("时辰需要是地支class")
        self.__天盘 = 月将 + ((时辰 - 支(1))*-1)
        self.__月将 = 月将
        self.__占时 = 时辰

    def __str__(self):
        x = PrettyTable()

        x.header = False
        x.padding_width = 0
        x.border = 0

        line = []
        for i in range(3, 7):
            line.append(self.__天盘 + i)
        x.add_row(line)

        line = [self.__天盘 + 2, '', '', self.__天盘 + 7]
        x.add_row(line)

        line = [self.__天盘 + 1, '', '', self.__天盘 + 8]
        x.add_row(line)

        line = []
        for i in range(9, 13):
            line.append(self.__天盘 + i)
        line.reverse()
        x.add_row(line)
        return x.get_string()

    def __getitem__(self, key):
        '''
        用于取得支上神
        '''
        if not isinstance(key, 支):
            raise ValueError('{0} 不是地支'.format(key))

        return self.__天盘 + (key - 支(1))


class 栻盘():
    def __init__(self, t, r):
        if not isinstance(t, 天盘):
            raise ValueError("{0} 不是天盘".format(t))
        if not isinstance(r, 干支):
            raise ValueError("{0} 不是干支表示的日".format(t))

        self.__天盘 = t
        self.__四课 = 四课(t, r)
        self.__三传 = 三传(self.__天盘, self.__四课)
        self.__天将 = None
        self.__获取三传()

    def __获取三传(self):
        pass

    def __str__(self):
        shipanPrint = [str(self.__天盘), str(self.__四课), str(self.__三传)]
        return "{0[0]}\n\n{0[1]}\n\n{0[2]}".format(shipanPrint)

    def __getitem__(self, key):
        if key not in ['天盘', '四课', '三传']:
            raise ValueError('{0} 不是“天盘”或“四课”或"三传"'.format(key))
        if key == '天盘':
            return self.__天盘
        elif key == '四课':
            return self.__四课
        else:
            return self.__三传


class 四课():
    def __init__(self, t, r):
        if not isinstance(t, 天盘):
            raise ValueError("{0} 不是天盘".format(t))
        if not isinstance(r, 干支):
            raise ValueError("{0} 不是干支表示的日".format(t))

        self.__天盘 = t
        self.__日 = r
        self.__干 = self.__日['干']
        self.__干阳神 = self.__天盘[寄宫(self.__干)]
        self.__干阴神 = self.__天盘[self.__干阳神]

        self.__支 = self.__日['支']
        self.__支阳神 = self.__天盘[self.__支]
        self.__支阴神 = self.__天盘[self.__支阳神]

    def __getitem__(self, key):
        '''
        a = 四课(天盘, 日)
        a['干'] 获取干
        a['干阳神'] 获取干阳神
        a['干阴神'] 获取干阴神
        a['支'] 获取支
        a['支阳神'] 获取支阳神
        a['支阴神'] 获取支阴神
        a[1] == (干阳神, 干)第一课
        a[2] == (干阴神, 干阳神)第二课
        a[3] == (支阳神, 支)第三课
        a[4] == (支阴神, 支阳神)第四课
        '''
        keys = ('干', '干阳神', '干阴神', '支', '支阳神', '支阴神', 1, 2, 3, 4)
        if key not in keys:
            msg = '{0} 只能是干, 干阳神, 干阴神, 支, 支阳神, 支阴神, 1, 2, 3, 4'
            raise ValueError(msg.format(key))

        if key == '干':
            return self.__干
        if key == '干阳神':
            return self.__干阳神
        if key == '干阴神':
            return self.__干阴神

        if key == '支':
            return self.__支
        if key == '支阳神':
            return self.__支阳神
        if key == '支阴神':
            return self.__支阴神

        if key == 1:
            return (self.__干阳神, self.__干)
        if key == 2:
            return (self.__干阴神, self.__干阳神)
        if key == 3:
            return (self.__支阳神, self.__支)
        if key == 4:
            return (self.__支阴神, self.__支阳神)

    def __str__(self):
        x = PrettyTable()

        x.header = False
        x.padding_width = 0
        x.border = 0

        x.add_row([self.__支阴神, self.__支阳神, self.__干阴神, self.__干阳神])
        x.add_row([self.__支阳神, self.__支, self.__干阳神, self.__干])

        return x.get_string()


class 三传():
    bazhuan = (干支(干(1), 支(1)), 干支(干(7), 支(7)), 干支(干(4), 支(6)), 干支(干(6), 支(6)))

    def __init__(self, t, s):
        if not isinstance(t, 天盘):
            raise ValueError("{0} 不是天盘".format(t))
        if not isinstance(s, 四课):
            raise ValueError("{0} 不是四课".format(s))
        self.__天盘 = t
        self.__四课 = s
        self.__初 = None
        self.__中 = None
        self.__末 = None
        self.__初, self.__中, self.__末 = self.__获取三传()

    def __获取三传(self):
        if self.__四课['支阳神'] == self.__四课['支']:
            return self.__伏呤()
        if 六冲(self.__四课['支阳神'], self.__四课['支']):
            return self.__返呤()
        try:
            return self.__贼克()
        except NoSanchuan as err:
            pass

        try:
            return self.__遥克()
        except NoSanchuan as err:
            pass

        try:
            return self.__昂星()
        except NoSanchuan as err:
            pass
        try:
            return self.__别责()
        except NoSanchuan as err:
            pass
        try:
            return self.__八专()
        except NoSanchuan as err:
            pass

    def __有贼(self):
        ke = []
        for i in range(1, 5):
            __课 = self.__四课[i]
            if 克(__课[1]['五行'], __课[0]['五行']):
                ke.append(__课)

        if len(ke) == 0:
            return ke
        # 删除重复课
        list_tmp = []
        ke_tmp = []
        for i in ke:
            if i[0] not in list_tmp:
                list_tmp.append(i[0])
                ke_tmp.append(i)
        return ke_tmp

    def __有克(self):
        ke = []
        for i in range(1, 5):
            __课 = self.__四课[i]
            if 克(__课[0]['五行'], __课[1]['五行']):
                ke.append(__课)
        if len(ke) == 0:
            return ke
        # 删除重复课
        list_tmp = []
        ke_tmp = []
        for i in ke:
            if i[0] not in list_tmp:
                list_tmp.append(i[0])
                ke_tmp.append(i)
        return ke_tmp

    def __贼克(self):
        __贼 = self.__有贼()
        if len(__贼) != 0:
            if len(__贼) == 1:
                __初 = __贼[0][0]
                __中 = self.__天盘[__初]
                __末 = self.__天盘[__中]
                return (__初, __中, __末)
            else:
                return self.__比用(__贼)

        __克 = self.__有克()
        if len(__克) != 0:
            if len(__克) == 1:
                __初 = __克[0][0]
                __中 = self.__天盘[__初]
                __末 = self.__天盘[__中]
                return (__初, __中, __末)
            else:
                return self.__比用(__克)
        raise NoSanchuan('不能用贼克取三传')

    def __比用(self, ke):
        # le(results) ==1, >1, ==0
        result = []
        for i in ke:
            if 阴阳相同(i[0], self.__四课['干']):
                result.append(i)
        if len(result) == 1:
            __初 = result[0][0]
            __中 = self.__天盘[__初]
            __末 = self.__天盘[__中]
            return (__初, __中, __末)
        elif len(result) == 0:
            return self.__涉害(ke)  # 俱不比
        else:
            return self.__涉害(result)  # 多个俱比

    def __涉害(self, ke):
        __ke = []
        for i in ke:
            jijie = i[1]  # 季节
            if isinstance(jijie, 干):
                jijie = 寄宫(jijie)
            if jijie in [支(1), 支(4), 支(7), 支(10)]:  # 四孟
                __ke.append(i)
        if len(__ke) == 1:
            __初 = __ke[0][0]
            __中 = self.__天盘[__初]
            __末 = self.__天盘[__中]
            return (__初, __中, __末)
        if len(__ke) >= 1:
            if self.__四课['干'].属阳:
                __初 = self.__四课['干阳神']
                __中 = self.__天盘[__初]
                __末 = self.__天盘[__中]
                return (__初, __中, __末)
            else:
                __初 = self.__四课['支阳神']
                __中 = self.__天盘[__初]
                __末 = self.__天盘[__中]
                return (__初, __中, __末)

        # if len(__ke) >= 1 无孟，取仲
        __ke = []
        for i in ke:
            jijie = i[1]  # 季节
            if isinstance(jijie, 干):
                jijie = 寄宫(jijie)
            if jijie in [支(2), 支(5), 支(8), 支(11)]:  # 四仲
                __ke.append(i)
        if len(__ke) == 1:
            __初 = __ke[0][0]
            __中 = self.__天盘[__初]
            __末 = self.__天盘[__中]
            return (__初, __中, __末)
        if len(__ke) >= 1:
            if self.__四课['干'].属阳:
                __初 = self.__四课['干阳神']
                __中 = self.__天盘[__初]
                __末 = self.__天盘[__中]
                return (__初, __中, __末)
            else:
                __初 = self.__四课['支阳神']
                __中 = self.__天盘[__初]
                __末 = self.__天盘[__中]
                return (__初, __中, __末)
        # 俱是季
        raise NoSanchuan('所临皆四季，不能用涉害取三传')

    def __遥克(self):
        if 干支(self.__四课['干'], self.__四课['支']) in self.bazhuan:
            raise NoSanchuan('八传日不用遥克')
        ke = []
        for i in range(2, 5):
            if 克(self.__四课[i][0]['五行'], self.__四课['干']['五行']):
                ke.append(self.__四课[i])
        if len(ke) == 0:
            for i in range(2, 5):
                if 克(self.__四课['干']['五行'], self.__四课[i][0]['五行']):
                    ke.append(self.__四课[i])
        if len(ke) == 0:
            raise NoSanchuan('无遥克，不能用遥克取三传')

        # 删除重复课
        list_tmp = []
        ke_tmp = []
        for i in ke:
            if i[0] not in list_tmp:
                list_tmp.append(i[0])
                ke_tmp.append(i)
        ke = ke_tmp
        if len(ke) == 1:
            __初 = ke[0][0]
            __中 = self.__天盘[__初]
            __末 = self.__天盘[__中]
            return (__初, __中, __末)
        else:
            return self.__比用(ke)

    def __昂星(self):
        ke = []
        list_tmp = []
        for i in range(1, 5):
            if self.__四课[i][0] not in list_tmp:
                list_tmp.append(self.__四课[i][0])
                ke.append(self.__四课[i])
        if len(ke) != 4:
            raise NoSanchuan('课不备，不能用昂星取三传')
        if self.__四课['干'].属阳:
            chu = self.__天盘[支(8)]
            zhong = self.__四课['支阳神']
            mo = self.__四课['干阳神']
            return (chu, zhong, mo)
        else:
            for i in range(1, 13):
                if self.__天盘[支(i)] == 支(8):
                    chu = 支(i)
            zhong = self.__四课['干阳神']
            mo = self.__四课['支阳神']
            return (chu, zhong, mo)

    def __别责(self):
        ke = []
        list_tmp = []
        for i in range(1, 5):
            if self.__四课[i][0] not in list_tmp:
                list_tmp.append(self.__四课[i][0])
                ke.append(self.__四课[i])
        if len(ke) == 4:
            raise NoSanchuan('四课全备，不能用别责取三传')
        if len(ke) != 3:
            raise NoSanchuan('用别责用于三课备取三传')
        if self.__四课['干'].属阳:
            for i in range(1, 11):
                if 五合(self.__四课['干'], 干(i)):
                    chu = self.__天盘[寄宫(干(i))]
                    break
            zhong = self.__四课['干阳神']
            mo = zhong
            return (chu, zhong, mo)
        else:
            all_sanhe = []
            for i in range(1, 13):
                for j in range(1, 13):
                    for k in range(1, 13):
                        if 三合(支(i), 支(j), 支(k)):
                            all_sanhe.append((支(i), 支(j), 支(k)))
            tmp_san_sanhe = []
            for i in all_sanhe:
                if i[0] in [支(1), 支(4), 支(7), 支(10)] and \
                   i[1] in [支(2), 支(5), 支(8), 支(11)]:
                    tmp_san_sanhe.append(i)
            all_sanhe = tmp_san_sanhe
            for i in all_sanhe:
                if self.__四课['支'] in i:
                    zhi_index = i.index(self.__四课['支'])
                    zhi_qian_sanhe_index = (zhi_index + 1) % 3
                    chu = i[zhi_qian_sanhe_index]
                    break
            zhong = self.__四课['干阳神']
            mo = zhong
            return (chu, zhong, mo)

    def __八专(self):
        if 干支(self.__四课['干'], self.__四课['支']) not in self.bazhuan:
            raise NoSanchuan('不是八传日')
        if self.__四课['干'].属阳:
            chu = self.__四课['干阳神'] + 2
            return (chu, self.__四课['干阳神'], self.__四课['干阳神'])
        else:
            chu = self.__四课['支阴神'] + (-2)
            return (chu, self.__四课['干阳神'], self.__四课['干阳神'])

    def __伏呤(self):
        # 六乙、六癸日
        if self.__四课['干'] in (干(2), 干(10)) or self.__四课['干'].属阳:
            chu = self.__四课['干阳神']
        else:
            # 阴日，非六乙日、六癸
            chu = self.__四课['支阳神']
        for i in range(1, 13):
            if 刑(chu, 支(i)):
                zhong = 支(i)
                break

        # 初为自刑，阳日、六乙日、六癸日取支上神为中传
        if chu == zhong:
            if self.__四课['干'] in (干(2), 干(10)) or self.__四课['干'].属阳:
                zhong = self.__四课['支阳神']
            else:
                zhong = self.__四课['干阳神']

        for i in range(1, 13):
            if 刑(zhong, 支(i)):
                mo = 支(i)
                break
        # 中传自刑，取中所冲之神
        if zhong == mo:
            for i in range(1, 13):
                if 六冲(zhong, 支(i)):
                    mo = 支(i)
                    break
        # 初、中互刑，如：子、卯，末取中所冲之神
        if 刑(zhong, chu):
            for i in range(1, 13):
                if 六冲(zhong, 支(i)):
                    mo = 支(i)
                    break
        return (chu, zhong, mo)

    def __返呤(self):
        try:
            return self.__贼克()
        except NoSanchuan as err:
            chu = 获取驿马(self.__四课['支'])
            zhong = self.__四课['支阳神']
            mo = self.__四课['干阳神']
            return (chu, zhong, mo)

    def __str__(self):
        x = PrettyTable()

        x.header = False
        x.padding_width = 0
        x.border = 0

        x.add_row(['', '', self.__初, ''])
        x.add_row(['', '', self.__中, ''])
        x.add_row(['', '', self.__末, ''])

        return x.get_string()
