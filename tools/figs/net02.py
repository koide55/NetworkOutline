"""第2回 DNS と電子メール の図"""
from svgkit import Fig


def f0201():
    """反復問い合わせによる名前解決"""
    f = Fig(720, 420)
    f.box(14, 176, 120, 60, ['クライアント'], cls='tint s', tcls='t-s b', rx=4)
    f.rect(214, 166, 160, 80, cls='accT s', rx=4)
    f.text(294, 194, 'キャッシュ DNS サーバ', cls='t-xs b')
    f.text(294, 214, '（フルリゾルバ）', cls='t-xs')
    f.arrow(134, 196, 210, 196, cls='sa', marker='aa')
    f.arrow(210, 218, 134, 218, cls='sa', marker='aa')
    f.text(172, 150, '① www.kyushu-u.ac.jp は？', cls='t-xs acc b')
    f.text(172, 266, '⑤ 答え（IP アドレス）', cls='t-xs acc b')
    servers = [('ルート DNS', '② 「jp はあちらへ」'), ('jp の DNS', '③ 「kyushu-u.ac.jp はあちらへ」'),
               ('kyushu-u.ac.jp の DNS', '④ 「www の IP アドレスはこれ」')]
    for i, (name, ans) in enumerate(servers):
        y = 40 + i * 120
        f.box(500, y, 200, 48, [name], cls='tint s', tcls='t-xs b', rx=4)
        f.text(600, y + 66, ans, cls='t-xs lbl')
        f.arrow(374, 190, 496, y + 18, cls='sm', marker='am')
        f.arrow(496, y + 32, 374, 206, cls='sm', marker='am')
    f.text(294, 288, 'TTL の間、答えを覚えておく', cls='t-xs lbl')
    f.text(360, 384, '誰も全体を知らないが、階層をたどれば必ず答えに着く', cls='t-s b')
    f.text(360, 408, 'キャッシュがあるので、実際の問い合わせはほとんどが1〜2段で終わる', cls='t-xs lbl')
    return f


def f0202():
    """メールが届くまで"""
    f = Fig(720, 400)
    f.box(10, 160, 110, 64, ['送信者の', 'メールソフト'], cls='tint s', tcls='t-xs b', rx=4, lh=16)
    f.box(190, 160, 120, 64, ['送信側の', 'メールサーバ'], cls='bg s', tcls='t-xs b', rx=4, lh=16)
    f.rect(390, 150, 140, 84, cls='accT s', rx=4)
    f.text(460, 172, '受信側の', cls='t-xs b')
    f.text(460, 189, 'メールサーバ', cls='t-xs b')
    f.box(405, 200, 110, 26, ['メールボックス'], cls='bg s', tcls='t-xs', rx=3)
    f.box(610, 160, 100, 64, ['受信者の', 'メールソフト'], cls='tint s', tcls='t-xs b', rx=4, lh=16)
    for x1, x2, top, sub1, sub2, acc in [(120, 190, 'SMTP 587', 'ログイン', 'して送る', False),
                                         (310, 390, 'SMTP 25', 'サーバ', 'どうし', True),
                                         (610, 530, 'IMAP 993', '読みに', '行く', False)]:
        f.arrow(x1, 192, x2 - 4 if x2 > x1 else x2 + 4, 192, cls='sa' if acc else 's',
                marker='aa' if acc else 'a')
        cx = (x1 + x2) / 2
        f.text(cx, 180, top, cls='t-xs b' + (' acc' if acc else ''))
        f.text(cx, 212, sub1, cls='t-xs lbl')
        f.text(cx, 228, sub2, cls='t-xs lbl')
    # DNS
    f.box(200, 30, 260, 50, ['DNS', '「example.jp の MX は？」'], cls='tint2 s', tcls='t-xs', rx=4, lh=16)
    f.path('M250,160 C250,120 270,100 290,84', cls='sm dash', arrow='am')
    f.text(272, 118, '宛先のドメインの受け取り先を引く', cls='t-xs lbl', anchor='start')
    # Web メール
    f.box(590, 300, 120, 50, ['ブラウザ', '（Web メール）'], cls='tint s', tcls='t-xs', rx=4, lh=16)
    f.path('M590,325 C530,325 490,300 475,238', cls='sm', arrow='am')
    f.text(520, 330, 'HTTPS 443', cls='t-xs', anchor='end')
    f.text(360, 380, '送るのは SMTP、読むのは IMAP（か HTTPS）、受け取り先を教えるのは DNS', cls='t-s b')
    return f


FIGURES = {'02-01': f0201, '02-02': f0202}
