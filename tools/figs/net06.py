"""第6回 LLM のしくみと API の図"""

from svgkit import Fig

def f0601():
    """AI という言葉の入れ子"""
    f = Fig(720, 380)
    levels = [
        ('AI（人工知能）', '知的な作業を計算機で行う技術の総称', '例：囲碁AI、ルールで動く診断システム'),
        ('機械学習', '規則を人が書かず、データから作らせる', '例：迷惑メールの判定'),
        ('深層学習', '多層のニューラルネットワークで学習する', '例：画像認識、音声認識'),
        ('生成AI', '文章・画像・音声を新しく作り出す', '例：画像生成、音声合成'),
        ('LLM（大規模言語モデル）', '大量のテキストで学習した言語モデル', '例：ChatGPT、Claude、Gemini'),
    ]
    for i, (name, desc, ex) in enumerate(levels):
        x, y = 20 + 22 * i, 20 + 56 * i
        w, h = 420 - 44 * i, 330 - 66 * i
        last = i == len(levels) - 1
        f.rect(x, y, w, h, cls=('accT s' if last else ('tint s' if i % 2 else 'bg s')), rx=8)
        f.text(x + 14, y + 22, name, cls='t-s b' + (' acc' if last else ''), anchor='start')
        f.text(470, y + 16, desc, cls='t-s', anchor='start')
        f.text(470, y + 34, ex, cls='t-xs lbl', anchor='start')
        f.line(x + 14 + len(name) * 12 + 8, y + 22, 462, y + 22, cls='sm dot')
    f.text(360, 366, 'ニュースで言う「AI」は、たいてい一番内側の LLM のことである', cls='t-s b')
    return f

def f0602():
    """LLM API を呼ぶときの通信"""
    f = Fig(720, 360)
    # 両端
    f.box(20, 130, 150, 76, ['あなたの', 'プログラム'], cls='tint s', tcls='t-s b', rx=6)
    f.rect(540, 108, 160, 120, cls='accT s', rx=6)
    f.text(620, 132, 'LLM の API サーバ', cls='t-s b')
    f.text(620, 150, 'データセンター', cls='t-xs lbl')
    for r in range(2):
        for c in range(4):
            f.rect(566 + c * 28, 166 + r * 24, 22, 18, cls='bg s')
    f.text(620, 222, 'GPU', cls='t-xs lbl')
    # DNS
    f.box(290, 22, 140, 38, ['DNS'], cls='tint2 s', tcls='t-s b', rx=4)
    f.path('M120,130 C120,60 200,41 286,41', cls='sm dash', arrow='am')
    f.text(160, 68, '① 名前を引く', cls='t-xs lbl', anchor='start')
    # TLS の管
    f.rect(184, 112, 340, 112, cls='none sa dash', rx=14)
    f.text(354, 102, '② TLS で相手を確かめ、暗号化する（HTTPS）', cls='t-xs acc b')
    f.arrow(196, 146, 532, 146, cls='s')
    f.text(354, 136, '③ POST ＋ JSON（会話の履歴・API キー）', cls='t-xs')
    f.arrow(532, 192, 196, 192, cls='s')
    f.text(354, 182, '④ 200 OK ＋ JSON（答え・使ったトークン数）', cls='t-xs')
    # SSE
    f.text(354, 254, 'stream を指定すると、④ は SSE で少しずつ届く（画面に文字が順に出る理由）',
           cls='t-xs lbl')
    f.text(360, 300, '第2〜4回で学んだ DNS・TLS・HTTP・JSON が、そのまま使われている', cls='t-s b')
    f.text(360, 324, '巨大なモデルは手元では動かないので、GPU を持つデータセンターに要求を送る',
           cls='t-xs lbl')
    return f

FIGURES = {'06-01': f0601, '06-02': f0602}
