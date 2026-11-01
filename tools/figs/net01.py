"""第1回 インターネットとアプリケーション層 の図"""
from svgkit import Fig


def f0101():
    """アプリケーションから見たネットワーク"""
    f = Fig(720, 380)
    for x, name, app in [(40, 'クライアント', 'ブラウザ'), (500, 'サーバ', 'Web サーバ')]:
        f.text(x + 90, 26, name, cls='t-s b')
        f.box(x, 40, 180, 50, [app], cls='accT s', tcls='t-s b', rx=6)
        f.rect(x, 104, 180, 150, cls='none sm dash', rx=6)
        for i, layer in enumerate(['トランスポート層', 'インターネット層', 'データリンク層', '物理層']):
            f.box(x + 14, 114 + i * 34, 152, 28, [layer], cls='tint s', tcls='t-xs lbl', rx=3)
    f.line(224, 58, 496, 58, cls='sa', arrow='aa')
    f.line(496, 74, 224, 74, cls='sa', arrow='aa')
    f.text(360, 46, 'HTTP のメッセージ', cls='t-xs acc b')
    f.text(360, 92, '形式・順番・意味の約束 ＝ プロトコル', cls='t-xs')
    f.text(360, 150, 'この講義では', cls='t-xs lbl')
    f.text(360, 168, '中身を見ない', cls='t-xs lbl')
    # 土管
    f.rect(60, 286, 600, 40, cls='tint2 s', rx=20)
    f.text(360, 306, '土管：メッセージを相手まで届けてくれる', cls='t-s b')
    f.line(130, 254, 130, 284, cls='sm', arrow='am')
    f.line(590, 284, 590, 254, cls='sm', arrow='am')
    f.text(360, 356, 'アプリケーションは「何を送るか」だけを考え、「どう届けるか」は下の層に任せる', cls='t-xs b')
    return f


def f0102():
    """インターネットは網の網"""
    f = Fig(720, 400)
    # 上位の事業者
    f.rect(170, 20, 380, 50, cls='tint2 s', rx=25)
    f.text(360, 45, '大手の通信事業者（互いに直接つながる）', cls='t-s b')
    # ISP と IX
    f.box(90, 140, 150, 50, ['ISP A'], cls='tint s', tcls='t-s b', rx=6)
    f.box(480, 140, 150, 50, ['ISP B'], cls='tint s', tcls='t-s b', rx=6)
    f.box(295, 140, 130, 50, ['IX', '（相互接続点）'], cls='accT s', tcls='t-xs b', rx=6, lh=16)
    f.line(240, 165, 295, 165, cls='s')
    f.line(425, 165, 480, 165, cls='s')
    f.line(165, 140, 250, 70, cls='s')
    f.line(555, 140, 470, 70, cls='s')
    f.text(176, 92, '費用を払って', cls='t-xs lbl', anchor='end')
    f.text(176, 108, 'つないでもらう', cls='t-xs lbl', anchor='end')
    f.text(360, 212, '対等な事業者どうしは IX で直接交換する', cls='t-xs lbl')
    # 末端
    ends = [(20, '家庭'), (180, '大学の LAN')]
    for x, name in ends:
        f.box(x, 270, 130, 46, [name], cls='bg s', tcls='t-xs', rx=4)
        f.line(x + 65, 270, 165, 190, cls='sm')
    ends = [(410, 'データセンター'), (570, '企業')]
    for x, name in ends:
        f.box(x, 270, 130, 46, [name], cls='bg s', tcls='t-xs', rx=4)
        f.line(x + 65, 270, 555, 190, cls='sm')
    f.text(475, 332, 'Web や生成AI のサーバ', cls='t-xs lbl')
    f.text(360, 366, '中央の管理者はいない。独立に運営される多数のネットワークがつながっている', cls='t-s b')
    f.text(360, 390, '海外とは海底ケーブルでつながる', cls='t-xs lbl')
    return f


def f0103():
    """IP アドレスとポート番号"""
    f = Fig(720, 380)
    # クライアント
    f.rect(20, 60, 220, 180, cls='tint s', rx=8)
    f.text(130, 82, 'あなたの PC', cls='t-s b')
    f.text(130, 102, '192.168.1.23', cls='t-xs m lbl')
    f.box(40, 130, 180, 50, ['ブラウザ', 'ポート 50123（一時的）'], cls='accT s', tcls='t-xs', rx=4, lh=16)
    # サーバ
    f.rect(470, 40, 230, 250, cls='tint s', rx=8)
    f.text(585, 62, 'サーバ', cls='t-s b')
    f.text(585, 82, '203.0.113.10', cls='t-xs m lbl')
    apps = [('Web サーバ', 'ポート 443'), ('メールサーバ', 'ポート 587'), ('SSH サーバ', 'ポート 22')]
    for i, (a, p) in enumerate(apps):
        f.box(490, 100 + i * 60, 190, 46, [a, p], cls='accT s' if i == 0 else 'bg s', tcls='t-xs', rx=4, lh=16)
    f.arrow(222, 155, 486, 123, cls='sa', marker='aa')
    f.text(354, 124, '宛先 203.0.113.10 の 443 番へ', cls='t-xs acc b')
    f.text(354, 300 - 140, 'IP アドレスで計算機を選び', cls='t-xs')
    f.text(354, 300 - 122, 'ポート番号でアプリを選ぶ', cls='t-xs')
    f.text(360, 324, '通信は5つ組で区別する：送信元の IP とポート・宛先の IP とポート・TCP か UDP か', cls='t-xs b')
    f.text(360, 350, 'だから1台のサーバで Web とメールを同時に動かせ、ブラウザのタブを何枚開いても混ざらない',
           cls='t-xs lbl')
    return f


FIGURES = {'01-01': f0101, '01-02': f0102, '01-03': f0103}
