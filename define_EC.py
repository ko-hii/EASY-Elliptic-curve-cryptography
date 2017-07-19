from random import randint, choice
from rho import rho
from multiprocessing import Process, cpu_count, Queue


# 楕円曲線上の全ての点を求め、その数を返す
def get_group_order(param):
    a = param['a']
    b = param['b']
    mod = param['mod']
    point_list = list()
    point_list.append((-1, -1))   # 無限遠点の設定
    for x in range(mod):
        for y in range(int(mod/2) + 1):   # yは+-が違うだけの二つを同時に見つけることができるため、実行回数は半分でよい
            left = pow(y, 2) % mod               # 左辺
            right = (pow(x, 3) + a*x + b) % mod  # 右辺
            if left == right:
                point_list.append((x, y))
                if y:   # yが0じゃなければ
                    point_list.append((x, mod-y))
    return point_list


def define_ec(mod, queue):

    # 位数が素数になるまでパラメータを適当に選び続ける
    while True:
        # 適当にパラメータを決める
        a = randint(1, mod)
        b = randint(1, mod)
        param = {'a': a, 'b': b, 'mod': mod}

        # 位数を求め、それが素数なら終わり
        point_list = get_group_order(param)  # 曲線上の全ての点を求める
        group_order = len(point_list)        # 点の数を求める
        if rho(group_order):   # ρ法で素数か判定
            break
        print('a=' + str(a) + ' , b=' + str(b) + ' : group order = ' + str(group_order) + ' is not prime.')

    print('a=' + str(a) + ' , b=' + str(b) + ' : group order = ' + str(group_order) + ' is prime.')

    # 公開点とする楕円曲線上の点を１つランダムに選ぶ
    param['point'] = choice(point_list)

    # 親に位数が素数になるパラメータを見つけたことを伝える
    queue.put(param)


"""
main.pyのmain()の中でどちらを選ぶかを決める。
位数が素数の(a,b)を選ぶ --> define_ec_main(mod)
位数が素数か判定しない  --> define_ec_easy(mod)
"""


# define_ecをマルチプロセスにした
def define_ec_main(mod):
    process_queue = dict()
    param = None

    # 論理プロセッサ数-1のdefine_ecを生成
    for i in range(cpu_count()-1):
        queue = Queue()
        p = Process(target=define_ec, args=(mod, queue, ))
        process_queue[p] = queue
        p.start()

    # どれか一つのプロセスがパラメータを見つけるまで
    flag = True
    while flag:
        for queue in process_queue.values():
            try:
                param = queue.get(block=True, timeout=1)
            except Exception:
                pass
            else:
                flag = False
                break

    # 全プロセスを殺す
    for process in process_queue.keys():
        process.terminate()

    return param


# 位数が素数かどうかは確認しない。パラメータの決定
def define_ec_easy(mod):
    while True:
        a = randint(1, mod)
        x = randint(1, mod)
        y = randint(1, mod)
        b = y**2 - (x**3 + a*x)

        # 重根を持たないかチェック
        if 4 * pow(a, 3) + 27 * pow(b, 2):
            break

    # パラメータの情報をまとめる
    b %= mod
    parm_dic = {'a': a, 'b': b, 'mod': mod, 'point': (x, y)}
    return parm_dic
