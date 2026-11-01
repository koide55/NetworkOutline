"""第7回 AIエージェントと MCP の図"""
import math

from svgkit import Fig


def f0701():
    """エージェントの動作ループ"""
    f = Fig(720, 450)
    cx, cy, r = 300, 196, 112
    steps = [('観測', -90), ('計画', 0), ('行動', 90), ('結果を見る', 180)]
    pos = {}
    for name, ang in steps:
        a = math.radians(ang)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        pos[name] = (x, y)
        f.circle(x, y, 42, cls='tint s')
        f.text(x, y, name, cls='t-s b')
    for a0, a1 in [(-90, 0), (0, 90), (90, 180), (180, 270)]:
        s, e = math.radians(a0 + 25), math.radians(a1 - 25)
        f.path(f'M{cx + r * math.cos(s):.1f},{cy + r * math.sin(s):.1f} '
               f'A{r},{r} 0 0 1 {cx + r * math.cos(e):.1f},{cy + r * math.sin(e):.1f}',
               cls='sa', arrow='aa')
    f.circle(cx, cy, 38, cls='accT s')
    f.text(cx, cy, 'LLM', cls='b')

    # 記憶（左の円と重ならない位置に置く）
    f.box(20, 168, 100, 56, ['記憶'], cls='tint2 s', tcls='t-s b', rx=4)
    f.arrow(120, 188, 142, 188, cls='sm', marker='am')
    f.arrow(142, 206, 120, 206, cls='sm', marker='am')

    # ツール（行動から出る）
    f.text(610, 152, 'ツール', cls='t-s b')
    tools = ['検索', 'メール・カレンダー', 'ファイル', 'Web API']
    for i, t in enumerate(tools):
        y = 170 + i * 50
        f.box(530, y, 160, 36, [t], cls='tint2 s', tcls='t-xs', rx=4)
        f.arrow(330, 338, 526, y + 18, cls='sm', marker='am')

    # 承認点
    f.rect(130, 372, 340, 38, cls='accT s', rx=6)
    f.text(300, 391, '承認点：取り消せない操作の前に、人間が確認する', cls='t-s b acc')
    f.line(300, 350, 300, 372, cls='sa dash')

    f.text(360, 434, 'LLM が「次に何をするか」を決め、周りのプログラムが道具を使って実行する', cls='t-xs b')
    return f


def f0702():
    """ツール呼び出しの流れ"""
    f = Fig(720, 440)
    cols = [('利用者', 80), ('プログラム（ホスト）', 270), ('LLM API', 460), ('ツール（メール検索）', 640)]
    for name, x in cols:
        f.box(x - 72, 20, 144, 34, [name], cls='tint s', tcls='t-xs b', rx=4)
        f.line(x, 54, x, 404, cls='sm dash')
    X = {n: x for n, x in cols}
    msgs = [
        ('利用者', 'プログラム（ホスト）', '「来週の会議を教えて」', 'ink'),
        ('プログラム（ホスト）', 'LLM API', '質問 ＋ 使える道具の一覧', 'ink'),
        ('LLM API', 'プログラム（ホスト）', '道具の呼び出しを依頼（JSON）', 'acc'),
        ('プログラム（ホスト）', 'ツール（メール検索）', '実行する', 'acc'),
        ('ツール（メール検索）', 'プログラム（ホスト）', '結果（招待メール3通）', 'ink'),
        ('プログラム（ホスト）', 'LLM API', '結果を添えて、もう一度送る', 'ink'),
        ('LLM API', 'プログラム（ホスト）', '答えの文章', 'ink'),
        ('プログラム（ホスト）', '利用者', '表示する', 'ink'),
    ]
    for i, (a, b, label, tone) in enumerate(msgs):
        y = 90 + i * 42
        x1, x2 = X[a], X[b]
        d = 4 if x2 > x1 else -4
        f.arrow(x1 + d, y, x2 - d, y, cls='sa' if tone == 'acc' else 's',
                marker='aa' if tone == 'acc' else 'a')
        # ツールとの往復はラベルを LLM の縦線に重ねず、プログラム寄りに置く
        lx = (x1 + x2) / 2 if 'ツール（メール検索）' not in (a, b) else 365
        f.text(lx, y - 9, label, cls='t-xs' + (' acc b' if tone == 'acc' else ''))
        f.text(14, y, str(i + 1), cls='t-xs lbl m', anchor='start')
    f.text(365, 189, 'search_mail {"query": "会議"}', cls='t-xs m lbl')
    f.text(360, 428, 'LLM は「この道具を、この引数で呼んで」と頼むだけ。実行するのはプログラムである',
           cls='t-s b')
    return f


def f0703():
    """MCP の構成"""
    f = Fig(720, 420)
    # ホスト
    f.rect(20, 70, 220, 280, cls='tint s', rx=8)
    f.text(130, 92, 'ホスト（AI アプリ）', cls='t-s b')
    f.text(130, 110, 'Claude、IDE、自作のエージェント', cls='t-xs lbl')
    ys = [150, 220, 290]
    for y in ys:
        f.box(50, y - 20, 160, 40, ['MCP クライアント'], cls='bg s', tcls='t-xs', rx=4)
    # LLM API
    f.box(300, 14, 150, 36, ['LLM API'], cls='accT s', tcls='t-s b', rx=4)
    f.path('M190,70 C190,40 240,32 296,32', cls='sm', arrow='am')
    f.text(232, 56, 'HTTPS', cls='t-xs lbl')
    # サーバ
    servers = [('ファイル', 'MCP サーバ（手元）'), ('メール', 'MCP サーバ（遠隔）'),
               ('カレンダー', 'MCP サーバ（遠隔）')]
    links = ['標準入出力', 'HTTP', 'HTTP']
    for (name, kind), y, ln in zip(servers, ys, links):
        f.rect(370, y - 26, 150, 52, cls='accT s' if ln == 'HTTP' else 'bg s', rx=4)
        f.text(445, y - 7, name, cls='t-s b')
        f.text(445, y + 11, kind, cls='t-xs lbl')
        f.arrow(212, y, 366, y, cls='s')
        f.arrow(366, y + 8, 212, y + 8, cls='sm', marker='am')
        f.text(289, y - 9, ln, cls='t-xs')
    f.text(289, 124, 'JSON-RPC 2.0', cls='t-xs acc b')
    # 先のサービス
    f.box(568, 128, 132, 44, ['手元のファイル'], cls='tint2 s', tcls='t-xs', rx=4)
    f.arrow(520, 150, 564, 150, cls='sm', marker='am')
    for y, name in [(220, 'Gmail API'), (290, 'Calendar API')]:
        f.box(568, y - 22, 132, 44, [name], cls='tint2 s', tcls='t-xs', rx=4)
        f.arrow(520, y, 564, y, cls='sm', marker='am')
    f.text(634, 334, 'サービスへは HTTPS ＋ OAuth 2.0', cls='t-xs lbl')
    f.text(360, 384, 'サーバが差し出すもの：tools（道具）・resources（データ）・prompts（定型の指示）',
           cls='t-xs b')
    f.text(360, 406, '1つのクライアントが1つのサーバとつながる。道具を足すときはサーバを足すだけでよい',
           cls='t-xs lbl')
    return f


def f0704():
    """実習：インシデント対応エージェントの流れ"""
    f = Fig(720, 300)
    f.box(14, 96, 104, 64, ['模擬アラート', '（JSON）'], cls='tint s', tcls='t-xs', rx=4)
    f.arrow(118, 128, 146, 128, cls='s')
    f.box(150, 92, 112, 72, ['LLM API', '答えの形を', 'JSON Schema で固定'], cls='accT s',
          tcls='t-xs', rx=4, lh=15)
    f.arrow(262, 128, 290, 128, cls='s')
    f.rect(294, 80, 150, 96, cls='bg s', rx=4)
    f.text(369, 98, 'AI の提案', cls='t-xs b')
    f.lines(306, 120, ['action: isolate_host', 'target: mail-gw01', 'confidence: 0.82'],
            cls='t-xs m', anchor='start', lh=17)
    f.arrow(444, 128, 472, 128, cls='s')
    f.poly([(536, 84), (594, 128), (536, 172), (478, 128)], cls='tint2 s')
    f.text(536, 120, '判断ルール', cls='t-xs b')
    f.text(536, 138, '（DSL）', cls='t-xs')
    f.box(614, 56, 96, 46, ['AI に任せる', '（auto）'], cls='bg s', tcls='t-xs', rx=4, lh=15)
    f.box(614, 154, 96, 46, ['人間が承認', '（ask_human）'], cls='accT s', tcls='t-xs b', rx=4, lh=15)
    f.arrow(566, 106, 610, 80, cls='s')
    f.arrow(566, 150, 610, 176, cls='sa', marker='aa')
    f.text(360, 236, 'ルールの例：重要な機器の隔離は人間が確認する／AI の自信が 0.7 未満なら人間が確認する',
           cls='t-xs')
    f.text(360, 270, '速さ（AI に任せる）と安全（人間が見る）の釣り合いを、ルールとして書き表す',
           cls='t-s b')
    return f


FIGURES = {
    '07-01': f0701, '07-02': f0702, '07-03': f0703, '07-04': f0704,
}
