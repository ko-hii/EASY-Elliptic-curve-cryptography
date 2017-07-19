from key_exchange import add_point
from multiprocessing import Pool


# 総当たり攻撃による解読
def decryption(dic):
    target = dic['send_data']
    public_point = dic['point']
    param = dic['param']

    temp = public_point
    secret_key = 1
    while True:
        secret_key += 1
        temp = add_point(temp, public_point, param)  # 公開されている座標を正解が見つかるまで足し続ける
        if temp == target:
            return secret_key


def decryption_main(info, param):
    public_point = info['public_point']
    send_data_alice = info['send_data_alice']
    send_data_bob = info['send_data_bob']

    # アリスとボブの秘密鍵を求める(並列化した)
    p = Pool(2)
    alice_secret_key, bob_secret_key = p.map(decryption, [
        {'point': public_point, 'send_data': send_data_alice, 'param': param},
        {'point': public_point, 'send_data': send_data_bob, 'param': param}
    ])
    print('alice secret key = ' + str(alice_secret_key))
    print('bob secret key = ' + str(bob_secret_key))

    return {'alice_secret': alice_secret_key, 'bob_secret': bob_secret_key}
