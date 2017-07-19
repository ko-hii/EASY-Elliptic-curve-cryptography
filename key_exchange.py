from random import randint
from sympy import Symbol
from math import sqrt
from multiprocessing import Pool


# modの法の下でxの逆元を返す(ユークリッド互除法)
def reverse(x, param):
    mod = param['mod']

    x = x % mod
    if x == 1:    # 1(単位元)の逆元は1(単位元)
        return 1

    x1 = Symbol(str(mod) + '_x')  # modを変数化
    x2 = Symbol(str(x) + '_x')    # xを変数化
    formula1 = x2
    formula2 = x1
    mod_ = mod
    div = x
    while True:
        div_temp = int(mod_ / div)
        mod_temp = mod_ % div
        mod_ = div
        div = mod_temp

        temp = formula1
        formula1 = formula2 - formula1 * div_temp
        formula2 = temp

        if mod_temp == 1:
            break
        if div == 0:   # 次のループで0割りエラー落ちする。div==0になるときある？
            print('div = 0 : ' + str(x))

    return int(formula1.coeff(Symbol(str(x) + '_x'))) % mod   # xの係数を返す


# point1 + point2 を返す
def add_point(point1, point2, param):
    a = param['a']
    mod = param['mod']

    # どちらかの点が無限遠点の場合
    if point1 == (-1, -1):
        return point2
    if point2 == (-1, -1):
        return point1

    # 座標
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    if (x1 == x2) and (y1 == (-y2) % mod):   # 加算結果が無限遠点の場合
        return tuple((-1, -1))

    # ラムダを決める
    if point1 != point2:
        lamb = (y2 - y1) * reverse(x2 - x1, param)
    else:
        lamb = (3 * pow(x1, 2) + a) * reverse(2 * y1, param)
    lamb = lamb % mod

    # 座標を計算する
    x = pow(lamb, 2) - x1 - x2
    y = lamb * (x1-x) - y1
    result = (x % mod, y % mod)
    return result   # 座標を返す


# pointのn倍を返す(繰り返し2倍法)
def mul_point(dic):
    n = dic['n']
    point = dic['point']
    param = dic['param']
    if n == 1:
        return point
    n_bin = bin(n)[2:]   # nを2進数(の文字列)に
    if n_bin[-1] == '1':  # リスト[-1]とすると一番後ろの要素が得られる。つまりn_binの一桁目が得られる。
        product = point
    else:
        product = (-1, -1)
    pre_point = point
    for i in range(1, len(n_bin)):   # 1からn_binの桁数の範囲でループ
        pre_point = add_point(pre_point, pre_point, param)
        if n_bin[-i-1] == '1':  # リスト[-i-1]は、一番後ろからi+1番目の要素が得られる。つまりn_binのi+1桁目が得られる
            product = add_point(product, pre_point, param)
    return product


# 楕円曲線暗号を用いて、鍵交換をする
# 返り値は、第３者が盗聴できる情報を返している
def key_exchange_main(param):
    a = param['a']
    b = param['b']
    mod = param['mod']

    # 楕円曲線の定義  y^2 = x^3 + a*x + b (mod)
    print('Elliptic curve : y^2 = x^3 + ' + str(a) + ' * x + ' + str(b) + ' (mod ' + str(mod) + ')')

    # 1. 盗聴されてもいい座標を決める
    public_point = param['point']
    print('Public point\t\t: ' + str(public_point))

    # 2. アリスの秘密鍵を決める (最大値はHasseの定理を参考。最小値は何でもいいが、大きいほどいいはず)
    alice_key = randint(int(mod/2), mod+1 - int(2 * sqrt(mod)))  # 大きいほど解読に時間がかかる
    print("Alice's secret key\t: " + str(alice_key))

    # 2. ボブの秘密座鍵を決める
    bob_key = randint(int(mod/2), mod+1 - int(2 * sqrt(mod)))
    print("Bob's secret key\t: " + str(bob_key))

    print('')

    # 3. それぞれの秘密鍵をpublic座標にかける(並列化した)
    p = Pool(2)
    send_data_alice, send_data_bob = p.map(mul_point, [{'n': alice_key, 'param': param, 'point': param['point']},
                                                       {'n': bob_key, 'param': param, 'point': param['point']}])
    print("Alice's send point\t: " + str(send_data_alice))
    print("Bob's send point\t: " + str(send_data_bob))

    # 4. それぞれが復号してみる(並列化した)
    alice, bob = p.map(mul_point, [{'n': alice_key, 'param': param, 'point': send_data_bob},
                                   {'n': bob_key, 'param': param, 'point': send_data_alice}])
    print('decrypted point in Alice\t: ' + str(alice))
    print('decrypted point in Bob\t\t: ' + str(bob))

    return {'public_point': public_point, 'send_data_alice': send_data_alice, 'send_data_bob': send_data_bob}
