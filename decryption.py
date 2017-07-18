from key_exchange import add_point


def decryption_main(info, param):
    public_point = info['public_point']
    send_data_alice = info['send_data_alice']
    send_data_bob = info['send_data_bob']

    # アリスの秘密鍵を求める
    temp = public_point
    alice_secret_key = 1
    while True:
        alice_secret_key += 1
        temp = add_point(temp, public_point, param)   # 公開されている座標を正解が見つかるまで足し続ける
        if temp == send_data_alice:
            break

    # ボブの秘密鍵を求める
    temp = public_point
    bob_secret_key = 1
    while True:
        bob_secret_key += 1
        temp = add_point(temp, public_point, param)   # 公開されている座標を正解が見つかるまで足し続ける
        if temp == send_data_bob:
            break

    return {'alice_secret': alice_secret_key, 'bob_secret': bob_secret_key}
