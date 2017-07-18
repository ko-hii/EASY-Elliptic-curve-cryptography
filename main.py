from key_exchange import key_exchange_main
from rho import get_prime
from decryption import decryption_main
from time import time
from define_EC import define_ec_easy, define_ec_main


def main():

    # 1. 楕円曲線暗号の法になる素数を決める
    print('---get prime---')
    start = time()
    mod = get_prime(6)   # 4桁の素数(4桁なら解読までもまぁすぐに終わる)
    print('prime = ' + str(mod))
    print('get_prime time = ' + str(time() - start) + ' sec')
    print('\n')

    # 2. 楕円曲線の定数と公開する点Pを決める (modが4桁の素数なら、define_ec_main()を使ってもまぁすぐ終わる)

    param = define_ec_easy(mod)   # 位数が素数かどうかのチェックをしない

    """
    # 位数が素数になるまでパラメータの選びなおしを行う
    start = time()
    param = define_ec_main(mod)   # 位数を計算し、それが素数になるまでaとbを選び続ける関数
    print('define elliptic curve parameter time = ' + str(time() - start) + ' sec')
    print('')
    """

    # 3. 楕円曲線暗号を用いてアリスとボブが鍵交換を行う
    print('---key exchange---')
    start = time()
    public_info = key_exchange_main(param)   # 有限体 F_mod = mod^1
    print('key_exchange time = ' + str(time() - start) + ' sec')
    print('')

    # 楕円曲線暗号を用いた鍵交換の際に第三者が盗聴可能な情報を出力
    print('---public information---')
    print('Elliptic curve : y^2 = x^3 + ' + str(param['a']) + ' * x + ' + str(param['b']) +
          ' (mod ' + str(param['mod']) + ')')
    for k, v in public_info.items():
        print(k + ' \t: ' + str(v))
    print('\n')

    # 4. 盗聴可能な情報から、アリスとボブの秘密鍵を解読する(総当たり攻撃)
    print('---decryption---')
    start = time()
    key_info = decryption_main(public_info, param)
    print('alice secret key= ' + str(key_info['alice_secret']))
    print('bob secret key = ' + str(key_info['bob_secret']))
    print('decryption time = ' + str(time() - start) + ' sec')
    print('')

    # 解読した鍵からアリスとボブが秘密裏に交換した座標を求める
    from key_exchange import mul_point
    alice = mul_point(public_info['send_data_bob'], key_info['alice_secret'], param)  # アリスの秘密鍵で復号
    print("decrypted point by Alice's secret key\t: " + str(alice))
    bob = mul_point(public_info['send_data_alice'], key_info['bob_secret'], param)    # ボブの秘密鍵で復号
    print("decrypted point by Bob's secret key\t\t: " + str(bob))


if __name__ == '__main__':
    main()
