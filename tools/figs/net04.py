"""第4回 Web アプリケーションと Web API の図"""
from svgkit import Fig


def _arrow(f, x1, y, x2, label, acc=False, below=None, lx=None):
    d = 4 if x2 > x1 else -4
    f.arrow(x1 + d, y, x2 - d, y, cls='sa' if acc else 's', marker='aa' if acc else 'a')
    cx = lx if lx is not None else (x1 + x2) / 2   # 長い矢印は、縦線に重ならない位置を指定する
    f.text(cx, y - 8, label, cls='t-xs' + (' acc b' if acc else ''))
    if below:
        f.text(cx, y + 14, below, cls='t-xs lbl')


def f0401():
    """ログイン状態を保つ2つの方式"""
    f = Fig(720, 400)
    # 左：Cookie 型
    f.text(175, 22, 'Cookie 型（状態をブラウザが持つ）', cls='t-s b')
    for x, n in [(50, 'ブラウザ'), (300, 'Web アプリ')]:
        f.box(x - 45, 36, 90, 30, [n], cls='tint s', tcls='t-xs b', rx=4)
        f.line(x, 66, x, 300, cls='sm dash')
    _arrow(f, 50, 96, 300, 'POST /login')
    _arrow(f, 300, 140, 50, 'Set-Cookie:', below='署名付きの「alice」')
    _arrow(f, 50, 200, 300, 'GET /mypage + Cookie', acc=True)
    f.rect(214, 222, 150, 40, cls='accT s', rx=4)
    f.lines(289, 236, ['署名を確かめて', '「alice」と分かる'], cls='t-xs', lh=14)
    # 右：サーバセッション型
    f.line(380, 20, 380, 310, cls='sm dot')
    f.text(545, 22, 'サーバセッション型（状態をサーバが持つ）', cls='t-s b')
    for x, n in [(425, 'ブラウザ'), (555, 'Web アプリ'), (665, 'セッション表')]:
        f.box(x - 40, 36, 80, 30, [n], cls='tint s', tcls='t-xs b', rx=4)
        f.line(x, 66, x, 300, cls='sm dash')
    _arrow(f, 425, 96, 555, 'POST /login')
    _arrow(f, 555, 120, 665, '保存')
    f.text(610, 136, '7f3a → alice', cls='t-xs m lbl')
    _arrow(f, 555, 168, 425, 'Set-Cookie:', below='sid=7f3a（番号だけ）')
    _arrow(f, 425, 220, 555, 'GET + Cookie', acc=True)
    _arrow(f, 555, 250, 665, '7f3a は？')
    _arrow(f, 665, 276, 555, 'alice')
    f.text(360, 340, 'どちらも、ブラウザが毎回 Cookie を見せることで「続き」を作っている', cls='t-s b')
    f.text(360, 366, 'サーバは覚えているのではなく、名札を見て思い出している', cls='t-xs lbl')
    return f


def f0402():
    """OAuth 2.0 の流れ（認可コード）"""
    f = Fig(720, 430)
    cols = [('利用者', 70), ('予定管理アプリ', 250), ('認可サーバ', 450), ('カレンダー API', 640)]
    for n, x in cols:
        f.box(x - 65, 20, 130, 34, [n], cls='tint s', tcls='t-xs b', rx=4)
        f.line(x, 54, x, 360, cls='sm dash')
    X = dict(cols)
    _arrow(f, X['予定管理アプリ'], 86, X['利用者'], '① 認可サーバへ案内')
    _arrow(f, X['利用者'], 128, X['認可サーバ'], '② ログインして許可', acc=True, below='「読み取りだけ」', lx=160)
    _arrow(f, X['認可サーバ'], 170, X['予定管理アプリ'], '③ 認可コード（利用者経由）', lx=350)
    _arrow(f, X['予定管理アプリ'], 212, X['認可サーバ'], '④ コードをトークンに交換')
    _arrow(f, X['認可サーバ'], 248, X['予定管理アプリ'], 'アクセストークン')
    _arrow(f, X['予定管理アプリ'], 296, X['カレンダー API'], '⑤ トークンを付けて呼ぶ', acc=True, lx=545)
    _arrow(f, X['カレンダー API'], 334, X['予定管理アプリ'], '予定の一覧（JSON）', lx=545)
    f.text(360, 392, 'アプリは利用者のパスワードを一度も見ない。受け取るのは、絞られた権限のトークンだけ', cls='t-s b')
    f.text(360, 416, 'トークンには範囲と期限があり、利用者は後から取り消せる', cls='t-xs lbl')
    return f


FIGURES = {'04-01': f0401, '04-02': f0402}
