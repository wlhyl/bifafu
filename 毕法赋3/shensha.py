from ganzhiwuxin import *


@checkValue(valueType=支)
def 获取驿马(a):
    sanHe = 获取三合(a)
    return 获取六冲(sanHe[0])
