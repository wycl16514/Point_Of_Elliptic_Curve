class EllipticPoint:
    def __init__(self, x, y, a, b):
        '''
        x, y, a, b 分别对应椭圆曲线公式上的参数
        '''
        self.x = x
        self.y = y
        self.a = int(a)
        self.b = int(b)
        if x is None and y is None:
            return
        #验证x,y是否在曲线上，也就是将x,y带入公式后左右两边要想等
        if self.y ** 2 != self.x ** 3 + self.a * self.x + self.b:
            raise ValueError(f"x:{self.x}, y:{self.y} is no a elliptic point")

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y or self.a != other.a or self.b != other.b

    def __repr__(self):
        return f"x:{self.x}, y:{self.y}, a:{self.a}, b:{self.b}"

    def __add__(self, other):
        #首先判断给定点在该椭圆曲线上
        if self.a != other.a or self.b != other.b:
            raise ValueError(f"given point is no on the samve elliptic curve")

        # 如果本身是零元，那么实现I + A = A
        if self.x is None and self.y is None:
            return other

        # 如果输入点是零元，那么加法结果就是本身：
        if other.x is None and other.y is None:
            return self

        # 如果输入点与当前点互为相反数，也就是关于x轴对称，那么返回无限远交点I
        if self.x == other.x and self.y == -other.y:
            return EllipticPoint(None, None, self.a, self.b)

        '''
        如果当前点与给定点形成的直线与椭圆曲线有三个交点，首先我们要计算A(x1,y1),B(x2,y2)所形成直线的斜率
        s = (y2-y1)/(x2-x1), 于是A,B所形成的直线方程就是 y = s * (x-x1) + y1,
        由于椭圆曲线的方程为 y^2 = x^2 + a*x + b，由于直线与曲线相交，假设叫点的坐标为x', y'
        由于交点在直线上，因此满足 y' = s * (x' - x1) + y1, 同时又满足y' ^ 2 = x' ^ 3 + a * x' + b,
        将左边带入到右边就有：
        (s * (x' - x1)) ^ 2 = x' ^ 3 + a * x' + b
        把公式左边挪到右边然后进行化简后就有：
        x ^3 - (s^2) * (x^2) + (a + 2*(s^2)*x1 - 2*s*y1)*x + b - (s^2)*(x1^2)+2*s*x1*y1-(y1 ^2) = 0  (公式1）
        如果我们把第三个交点C的坐标设置为(x3, y3)，于是A，B,C显然能满足如下公式：
        (x-x1)*(x-x2)*(x-x3) = 0
        将其展开后为：
        x^3 - (x1 + x2 + x3) * (x^2) + (x1*x2 + x1*x3 + x2+x3)*x - x1*x2*x3 = 0  （公式2）
        我们把公式1 和公式2中对应项的系数一一对应起来，也就是两个公式中x^3的系数是1，公式1中x^2的系数是(s^2)，
        公式2中x^2的系数为(x1 + x2 + x3)，于是对应起来：
        s^2 <-> (x1 + x2 + x3)  （#1）
        公式1中x对应系数为(a + 2*(s^2)*x1 - 2*s*y1), 公式2中x对应系数为(x1*x2 + x1*x3 + x2+x3)，于是对应起来：
        (a + 2*(s^2)*x1 - 2*s*y1) <-> (x1*x2 + x1*x3 + x2+x3)
        公式1中常数项为b - (s^2)*(x1^2)+2*s*x1*y1-(y1 ^2), 公式2中常数项为 x1*x2*x3，对应起来就是：
        b - (s^2)*(x1^2)+2*s*x1*y1-(y1 ^2) <-> x1*x2*x3
        
        根据代数理论中中的Vieta定律，如果如果两个多项式的根要相同，他们对应项的系数必须相等，于是有：
        s^2 = (x1 + x2 + x3)  （#1）
        (a + 2*(s^2)*x1 - 2*s*y1) = (x1*x2 + x1*x3 + x2+x3)
        b - (s^2)*(x1^2)+2*s*x1*y1-(y1 ^2) = x1*x2*x3
        于是我们可以从(#1)中把x3 解出来：
        x3 = s^2 - x1 - x2 
        然后把x3放入直线方程将y3解出来：
        y3 = -(s(x3-x1)+y1) = s * (x1 - x3) - y1
        '''
        if self.x != other.x:
            s = (other.y - self.y) / (other.x - self.x)
            x3 = s ** 2 - self.x - other.x
            y3 = s * (self.x - x3) - self.y
            return EllipticPoint(x3, y3, self.a, self.b)
        '''
        如果self.x == other.x and self.y == other.y ,这种情况下对应椭圆曲线上一点的切线，这时
        我们要计算切线与曲线的另一个交点。根据微积分，函数f(x)在给定点x处的切线对应斜率就是f'(x)，
        椭圆曲线函数为y^2 = x^3 + a*x + b, 左右两步对x求导有：
        2y*(d(y)/d(x)) = 3x^2 + a, d(y)/d(x)就是f'(x),我们需要将其计算出来，也就有:
        s = d(y)/d(x) = (3*x^2+a)/(2*y),接下来的计算跟上面一样，只不过把x2换成x1,于是有：
        x3 = s^2 - 2*x1, y3 = s * (x1 - x3) - y1
        '''
        if self == other and self.y != 0:
            s = (3 * self.x ** 2 + self.a) / 2 * self.y
            x3 = s ** 2 - 2 * self.x
            y3 = s * (self.x - x3) - self.y
            return EllipticPoint(x3, y3, self.a, self.b)

        '''
        还有最后一种情况，直线不但与y轴平行，而且还是曲线的切线，有就是一根竖直线与曲线在圆头出相切，
        这个点也是y坐标为0的点
        '''
        if self == other and self.y == 0:
            return EllipticPoint(None, None, self.a, self.b)

#曲线上一点的切线与曲线交点
a = EllipticPoint(-1, -1, 5, 7)
print(a + a)

#曲线上两点形成的连线与曲线相交于第3点
a = EllipticPoint(2, 5, 5, 7)
b = EllipticPoint(-1, -1, 5, 7)
print(a + b)

#曲线上两点在一条竖直线上
a = EllipticPoint(2, 5, 5, 7)
b = EllipticPoint(2, -5, 5, 7)
print(a + b)
