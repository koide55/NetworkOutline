"""第5回 クラウド・仮想化・P2P の図"""
from svgkit import Fig


def f0501():
    """オーバレイネットワークとファイルの交換"""
    f = Fig(720, 400)
    # 下：インターネット
    f.rect(30, 300, 660, 40, cls='tint2 s', rx=20)
    f.text(360, 320, 'インターネット（実際の経路）', cls='t-xs b')
    # ピア
    peers = {'A': (120, 90), 'B': (330, 60), 'C': (560, 100), 'D': (220, 210), 'E': (480, 220)}
    have = {'A': [1, 2], 'B': [2, 3, 4], 'C': [1, 4], 'D': [3], 'E': [1, 2, 3]}
    links = [('A', 'B'), ('B', 'C'), ('A', 'D'), ('D', 'E'), ('B', 'E'), ('C', 'E')]
    for a, b in links:
        (x1, y1), (x2, y2) = peers[a], peers[b]
        f.line(x1, y1, x2, y2, cls='sm dash')
    for n, (x, y) in peers.items():
        f.rect(x - 56, y - 24, 112, 48, cls='bg s', rx=6)
        f.text(x - 40, y - 8, n, cls='t-xs b')
        for i in range(4):
            on = (i + 1) in have[n]
            f.rect(x - 30 + i * 20, y - 2, 16, 16, cls='accT s' if on else 'bg sm', rx=2)
            if on:
                f.text(x - 22 + i * 20, y + 7, str(i + 1), cls='t-xs')
        f.line(x, y + 24, x, 296, cls='sm dot')
    # 交換の例
    f.arrow(300, 76, 176, 84, cls='sa', marker='aa')
    f.text(232, 64, '片 3 を渡す', cls='t-xs acc b')
    f.arrow(424, 210, 270, 210, cls='sa', marker='aa')
    f.text(347, 198, '片 1・2 を渡す', cls='t-xs acc b')
    f.text(640, 168, '点線：ピアどうしの', cls='t-xs lbl', anchor='middle')
    f.text(640, 184, '論理的なつながり', cls='t-xs lbl', anchor='middle')
    f.text(360, 370, 'ファイルを小片に分け、持っている片を互いに配り合う。参加者が増えるほど配る側も増える', cls='t-xs b')
    f.text(360, 392, 'インターネットの上に、アプリケーションのための網（オーバレイネットワーク）を築いている', cls='t-xs lbl')
    return f


def f0502():
    """WebRTC：ブラウザどうしが直接つながる"""
    f = Fig(720, 380)
    f.box(20, 150, 150, 60, ['ブラウザ A'], cls='tint s', tcls='t-s b', rx=6)
    f.box(550, 150, 150, 60, ['ブラウザ B'], cls='tint s', tcls='t-s b', rx=6)
    f.box(270, 20, 180, 50, ['シグナリングサーバ', '（Web サーバ）'], cls='bg s', tcls='t-xs b', rx=4, lh=16)
    f.path('M95,150 C95,90 180,48 266,45', cls='sm', arrow='am')
    f.path('M625,150 C625,90 540,48 454,45', cls='sm', arrow='am')
    f.text(180, 100, '① つなぎ方の情報を', cls='t-xs lbl', anchor='start')
    f.text(180, 116, '交換する（HTTP など）', cls='t-xs lbl', anchor='start')
    f.box(290, 270, 140, 44, ['STUN / TURN'], cls='tint2 s', tcls='t-xs b', rx=4)
    f.text(360, 330, '② 外から見えるアドレスを調べる', cls='t-xs lbl')
    f.text(360, 346, '直接つながらないときは中継してもらう', cls='t-xs lbl')
    f.line(170, 200, 290, 280, cls='sm dash')
    f.line(550, 200, 430, 280, cls='sm dash')
    f.arrow(174, 172, 546, 172, cls='sa', marker='aa')
    f.arrow(546, 190, 174, 190, cls='sa', marker='aa')
    f.text(360, 160, '③ 映像・音声・データを直接送り合う', cls='t-xs acc b')
    f.text(360, 212, '暗号化は必須', cls='t-xs lbl')
    return f


FIGURES = {'05-01': f0501, '05-02': f0502}
