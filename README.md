大概了解区块链底层加密算法的同学都会听到一个名词叫”椭圆曲线“，它是抽象代数和数论中一个非常重要的概念，同时也是数学研究领域的一个重要分支，在理论研究上，英国数学家正是借助椭圆曲线证明了费马大定理，在应用上它则在加解密上发挥重大作用。

椭圆曲线表面上看起来似乎没有那么复杂，任何满足如下形式的方程都称为椭圆曲线：
y^2 = x ^3 + a.x + b

它跟一般多项式不同在于，它左边y是取平方。正是因为这个特性，所以椭圆曲线具有x轴对称的特点，这些曲线的图形类似如下形状：
![请添加图片描述](https://img-blog.csdnimg.cn/effae13a4be74297b2003ef64c30bcad.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAdHlsZXJfZG93bmxvYWQ=,size_20,color_FFFFFF,t_70,g_se,x_16)
在比特币中，使用的椭圆曲线有个”不明觉厉“的名称叫secp256k1,其实就是将上面公式中的a取0，b取7，也就是：
y ^ 2   =   x ^ 3 + 7

在椭圆曲线上，有一些特定点所形成的集合在加解密上能发挥重大作用，因此我们先用代码定义椭圆曲线的点：
```
class EllipticPoint:
    def __init__(self, x, y, a, b):
        '''
        x, y, a, b 分别对应椭圆曲线公式上的参数
        '''
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        #验证x,y是否在曲线上，也就是将x,y带入公式后左右两边要想等
        if self.y ** 2 != x ** 3 + a * x + b:
            raise ValueError(f"x:{x}, y:{y} is no a elliptic point")

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b
        
    def __ne__(self, other):
        return self.x != other.x or self.y != other.y or self.a != other.a or self.b != other.b
```
接下来我们要定义椭圆曲线上点的”加法“，显然这里的加法绝对不是普通四则运算上的加法，根据椭圆曲线的图形特征，任意一条直线与它相交的情况只有三种可能，一种是只有一个交点：
![请添加图片描述](https://img-blog.csdnimg.cn/9926109eefdc46c681448d7bad6259c3.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAdHlsZXJfZG93bmxvYWQ=,size_20,color_FFFFFF,t_70,g_se,x_16)
一种是有三个交点：
![请添加图片描述](https://img-blog.csdnimg.cn/d92fa1b2b14042c2851551d445429d61.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAdHlsZXJfZG93bmxvYWQ=,size_20,color_FFFFFF,t_70,g_se,x_16)
还有一种是有两个交点，这种情况又分为两种情形，分别为：
![请添加图片描述](https://img-blog.csdnimg.cn/0f53281395fa4db2994fd130108a13ef.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAdHlsZXJfZG93bmxvYWQ=,size_20,color_FFFFFF,t_70,g_se,x_16)
这种情形是直线与x轴平行，还有一种情形如下：
![请添加图片描述](https://img-blog.csdnimg.cn/be5d5e1561c14c10ab21a8db50e189e7.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAdHlsZXJfZG93bmxvYWQ=,size_20,color_FFFFFF,t_70,g_se,x_16)
这种情形为直线为椭圆曲线的切线。由此椭圆曲线上点的”加法“定义如下，假设有两个在椭圆曲线上的点A, B，它们所形成直线如果与椭圆曲线有三个交点C，那么将c点沿着x轴对称后所得的点就是A"+"B的结果，情形如下：![请添加图片描述](https://img-blog.csdnimg.cn/72d1f80a7c2449858d9883d3f3df5182.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAdHlsZXJfZG93bmxvYWQ=,size_20,color_FFFFFF,t_70,g_se,x_16)

显然这样的定义会带来困惑，例如当A,B所形成的直线与x轴平行，那么这条直线只会与椭圆曲线形成两个交点，于是就不会像前面描述的那样通过第三个交点来找到A "+" B对应的点。这种情况的处理方法显示出了数学的抽象性，虽然没有第三个交点，但我们可以定义出这个不存在的点，我们认为在这种情况下，A,B所形成的直线与椭圆曲线在”无限远“处相交，我们用I来表示这个定义中的第三个交点，同时我们把这次情况下称A和B互为相反数，也就是 A = -B, B = -A, 眼尖的同学可能从这里联想到了前面描述有限群时的”零元“，其实我们这里就能把这个无限远处的交点I与有限群中的”零元“关联起来。

我们这么定义的加法就存在若干特性：
1，对任意一个点A，存在-A，使得 A + -A = I, 所谓-A就是将A根据x轴做对称
2，A "+" B = "B" + "A", 这个不难理解，因为A,B两点形成的直线跟椭圆曲线第三个交点都是固定的
3，(A "+" B) "+" C = A "+" (B "+" C)这个叫结合性，这个就不好理解，我们必须结合图形来看，首先看等式左边的情形：
![请添加图片描述](https://img-blog.csdnimg.cn/b603062176a643c281dfd3898e9733b2.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAdHlsZXJfZG93bmxvYWQ=,size_20,color_FFFFFF,t_70,g_se,x_16)
接下来看等式右边的情形：![请添加图片描述](https://img-blog.csdnimg.cn/9e97e37ce64c4f67aefbe8c4539f03e8.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAdHlsZXJfZG93bmxvYWQ=,size_20,color_FFFFFF,t_70,g_se,x_16)
可以看到等式左边和右边在计算后，结果都对应右上角的黄色实心点。现在我们可以对点的”加法“进行代码实现，首先我们需要定义点I的坐标，由于改点在无限远处，因此它的x和y坐标都在无穷大出，我们在代码中用None来表示这个点的坐标，于是如果椭圆曲线参数a,b分别取值7，11，那么I的表示为：
```
EllipticPoint(None, None, 7, 11)
```
于是我们希望”加法操作要满足如下情况:
```
A = EliipticPoint(-1, -1,7, 11)
B = EllipticPoint(-1, 1,7, 11)
I = EllipticPoint(None, None, 7, 11)
A + B == I
A + I == A
B + I == B 
```
要实现EllipticPoint(None, None, 7, 11)，我们需要修改前面的初始化函数，如果x,y取值为None，那么就不用判断点是否在曲线上，于是__init__修改为：
```
 def __init__(self, x, y, a, b):
        '''
        x, y, a, b 分别对应椭圆曲线公式上的参数
        '''
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        if x is None and y is None:
            return
        #验证x,y是否在曲线上，也就是将x,y带入公式后左右两边要想等
        if self.y ** 2 != x ** 3 + a * x + b:
            raise ValueError(f"x:{x}, y:{y} is no a elliptic point")
```
接下来我们实现加法操作：
```
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
```
在两点的"加法“操作中有一些数学推导，例如用到了线性代数中的Vieta定理，它的证明我们不用关心，直接采用其结论就好了。在计算椭圆曲线两点相加时，总共有四种情况要考虑，分别为两点形成的直线与曲线相交于第3点；两点在同一条竖直线上；两点其实是同一点，这种情况计算改点切线与曲线相交的另一点；两点都是同一点，而且y坐标为0，这种情况如下图所示：
![请添加图片描述](https://img-blog.csdnimg.cn/c237e7f675b74533a339fe27febc2d67.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAdHlsZXJfZG93bmxvYWQ=,size_20,color_FFFFFF,t_70,g_se,x_16)
我们测试完成的代码看看情况：
```
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
```
代码运行后所得结果如下：
```
x:18.0, y:77.0, a:5, b:7
x:3.0, y:-7.0, a:5, b:7
x:None, y:None, a:5, b:7
```
下一节我们看看如何使用椭圆曲线来进行加解密。
