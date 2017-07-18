from fractions import gcd
from random import randint


# 写像関数
def mapping_func(x):
    return pow(x, 2) + x + 1


# 素数と判定されたらTrueを返す
# 改良ρ法ではgcd()の結果が1から抜け出せないことが多かったため、改良ρ法はやめた
def rho(n):
    # 特別処理
    if n < 2:
        return False  # 負数、0, 1は素数ではない
    elif n < 4:
        return True   # 2, 3は素数

    x = 1
    x_list = list()
    result = 1
    while result == 1:
        x = mapping_func(x) % n
        for past_x in x_list:
            result = gcd(x-past_x, n)
            if result > 1:
                break
        x_list.append(x)
    if result == n:
        return True
    else:
        return False


# lengthの桁数の乱奇数を生成し、ρ法でそれが素数かどうかを判定
def get_prime(length):

    # 素数が作れるまでループ
    while True:
        # length桁の奇数nの生成
        n = str(randint(1, 9))       # 最初の桁は0以外
        for i in range(length-2):
            n += str(randint(0, 9))  # 間の桁は0-9の範囲なら何でも
        n += str(randint(1, 5) * 2 - 1)  # 最後の桁は奇数にする

        # 素数判定
        if n[length-1] == '5':
            continue   # 最後の桁が5なら絶対に素数ではないため、ρ法でチェックする必要がない
        if sum([int(i) for i in n]) % 3 == 0:
            continue   # 全ての桁を足し合わせて3で割り切れると素数ではないため、ρ法でチェックする必要がない

        # ρ法による素数判定
        if rho(int(n)):
            break

    return int(n)
