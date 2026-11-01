// 第4回 Web アプリケーションと Web API
//
// 流用元（スライド番号）
//   CompOutline 第10回 … 10-04 の図（Web アプリケーションの三層構成）
//   CompOutline 第12回 … OAuth 2.0 と OpenID Connect（24）
//   network2026.pptx … Web 2.0（140〜150、短くした）、REST（660〜661）、OAuth の目的（684）
//   vuln-webapp 第3回 … Cookie 型認証とサーバセッション型認証
//   webapp-security-programming-handson … HTTP はステートレス・Cookie（25〜35）、bottle
//   iot-handson … 発展課題（local-python-receiver に POST する）
module.exports = {
  no: 4,
  title: 'Web アプリケーションと Web API',
  question: '状態を持たない HTTP の上で、ログインや掲示板はどう作られているのか。',
  bigQuestion: '状態を持たない HTTP の上で、\nログインはどう作られているのか。',
  questionSub: 'そして、プログラムどうしは Web をどう使ってやりとりしているのか。',
  goals: [
    ['Web アプリの三層構成', 'を説明できる'],
    ['Cookie とセッション', 'でログイン状態を保つ2つの方式を説明できる'],
    ['REST と JSON', 'で作られた Web API を読み、呼び出せる'],
    ['WebSocket と SSE', 'が何のためにあるかを説明できる'],
    ['OAuth 2.0 と OpenID Connect', 'が何を任せているかを説明できる'],
  ],
  slides: [
    { kind: 'section', n: '4.1', name: 'Web アプリケーション', tagline: 'ページを見せるだけでなく、仕事をする' },
    {
      kind: 'split', kicker: '4.1　Web アプリ', title: 'Web 2.0 から、今の Web アプリへ',
      left: {
        title: 'Web 2.0（2005年頃）',
        items: ['利用者が書き込み、共有する（ブログ、SNS、Wiki）', 'ページ全体を読み直さずに一部を更新する（Ajax）', 'Web がアプリケーションの土台になる'],
      },
      right: {
        title: '今の Web アプリ',
        items: ['1枚のページの中で、JavaScript が画面を作り替える（SPA）', 'データは Web API から JSON で受け取る', 'スマートフォンのアプリも同じ API を使う'],
      },
      note: 'Google マップ（2005年）は、ページを読み直さずに地図を動かせることで驚かれた。今はそれが当たり前になった。',
      noteY: 4.6,
    },
    {
      kind: 'figure', kicker: '4.1　Web アプリ', title: 'Web アプリケーションの三層構成', fig: 'co-10-04', h: 4.5,
      caption: '各層を独立に増やせる。アクセスが増えたらアプリサーバを、データが増えたら DB を強くする。',
    },

    { kind: 'section', n: '4.2', name: 'ログイン状態を保つ', tagline: 'Cookie が、ステートレスな HTTP に記憶を足す' },
    {
      kind: 'cards', kicker: '4.2　Cookie', title: 'Cookie とは',
      items: [
        ['サーバが渡す', '応答の Set-Cookie ヘッダで、ブラウザに小さなデータを保存させる'],
        ['ブラウザが返す', '同じサイトへのその後の要求に、Cookie ヘッダで自動的に付けて送る'],
        ['使いみち', 'ログイン状態、カートの中身、表示の設定'],
      ], per: 3, cardH: 1.6,
      callout: ['HTTP はステートレス。状態は Cookie として、要求に毎回乗せる',
        'サーバは「覚えている」のではなく、毎回「名札を見せてもらって」いる。'],
    },
    {
      kind: 'figure', kicker: '4.2　セッション', title: 'ログイン状態を保つ2つの方式', fig: '04-01', h: 4.9,
    },
    {
      kind: 'table', kicker: '4.2　セッション', title: '2つの方式の比較',
      rows: [['', 'Cookie 型', 'サーバセッション型'],
        ['状態を持つ場所', 'ブラウザ（署名して書き換えを防ぐ）', 'サーバの表（ブラウザには番号だけ）'],
        ['サーバを増やすとき', 'そのまま増やせる', 'セッションの表を共有する必要がある'],
        ['強制的にログアウトさせる', '難しい（期限まで有効）', '表から消せばよい'],
        ['Cookie が盗まれたら', '期限まで使われうる', '表から消せば止められる']],
      colW: [3.2, 4.3, 4.3], rowH: 0.5,
      sub: 'どちらの方式でも、Cookie が盗まれれば、なりすましが起きる（第8回のセッションハイジャック）。\nvuln-webapp の教材アプリでは、2つの方式を切り替えて比べられる。',
    },

    { kind: 'section', n: '4.3', name: 'Web API', tagline: 'プログラムどうしが HTTP で話す' },
    {
      kind: 'statement', kicker: '4.3　Web API', title: 'Web API：相手は人ではなくプログラム',
      statement: '同じ HTTP で、HTML の代わりに JSON を返す',
      map: [['ブラウザで人が見る', 'HTML を返す'],
        ['プログラムが使う', 'JSON を返す'],
        ['スマホのアプリ・IoT 機器・AI', '同じ API を呼ぶ']],
      sub: '天気、地図、決済、翻訳、LLM —— 多くのサービスが Web API を公開している。',
    },
    {
      kind: 'table', kicker: '4.3　REST', title: 'REST：資源を URL で、操作をメソッドで',
      rows: [['操作', 'メソッドと URL', '意味'],
        ['一覧', 'GET /posts', '投稿の一覧を取る'],
        ['1件', 'GET /posts/42', '42 番の投稿を取る'],
        ['作成', 'POST /posts', '新しい投稿を作る'],
        ['更新', 'PUT /posts/42', '42 番を置き換える'],
        ['削除', 'DELETE /posts/42', '42 番を消す']],
      colW: [1.8, 4.2, 5.8], rowH: 0.46,
      callout: 'URL が名詞、メソッドが動詞になる',
      sub: 'REST は、2000年に Roy Fielding が博士論文で示した設計の考え方である。',
    },
    {
      kind: 'split', kicker: '4.3　JSON', title: 'JSON：データの書き方',
      left: {
        title: '例：掲示板の投稿1件',
        code: [
          '{',
          '  "id": 42,',
          '  "author": "alice",',
          '  "text": "明日のゼミは14時から",',
          '  "tags": ["ゼミ", "連絡"],',
          '  "likes": 3,',
          '  "pinned": false',
          '}',
        ],
        codeH: 3.0, size: 12,
      },
      right: {
        title: '読み方',
        items: ['{ } はオブジェクト（名前と値の組）、[ ] は配列',
          '文字列・数・真偽値・null を表せる',
          'ほとんどのプログラミング言語で読み書きできる',
          'Content-Type: application/json で送る',
          '第6・7回の LLM API や MCP も、この形でやりとりする'],
      },
    },
    {
      kind: 'table', kicker: '4.3　押し出す通信', title: 'サーバから送りたいとき：SSE と WebSocket',
      lead: 'HTTP は「要求があって初めて応答する」形なので、サーバから先に送りたいときに工夫が要る。',
      rows: [['方式', '向き', '向いている用途'],
        ['ポーリング', 'クライアントが繰り返し聞く', '単純だが、無駄な要求が多い'],
        ['SSE（Server-Sent Events）', 'サーバ → クライアント（片方向）', '通知、LLM の答えを少しずつ表示する（第6回）'],
        ['WebSocket', '双方向', 'チャット、共同編集、オンラインゲーム']],
      colW: [3.6, 3.8, 4.4], rowH: 0.5,
    },
    {
      kind: 'code', kicker: '4.3　確かめる', title: '確かめてみよう：公開されている API を呼ぶ',
      code: [
        'curl -i https://api.github.com/users/octocat',
        '',
        'HTTP/2 200',
        'content-type: application/json; charset=utf-8',
        'x-ratelimit-remaining: 59',
        '',
        '{',
        '  "login": "octocat",',
        '  "public_repos": …,',
        '  …',
        '}',
      ],
      codeH: 3.8, size: 11,
      side: {
        title: '読み方',
        body: 'GitHub の API は、認証なしでも一部を呼べる（回数に制限がある）。\n\n応答ヘッダの x-ratelimit-remaining で、残りの回数が分かる。使い切ると 403 や 429 が返る。\n\nブラウザで同じ URL を開くと、JSON がそのまま見える。',
      },
    },

    { kind: 'section', n: '4.4', name: 'OAuth 2.0 と OpenID Connect', tagline: 'パスワードを渡さずに、権限だけを渡す' },
    {
      kind: 'figure', kicker: '4.4　OAuth', title: 'OAuth 2.0：権限をトークンで渡す', fig: '04-02', h: 4.9,
    },
    {
      kind: 'table', kicker: '4.4　OAuth', title: 'OAuth 2.0 と OpenID Connect',
      rows: [['', 'OAuth 2.0', 'OpenID Connect'],
        ['目的', '認可：このアプリに何をさせてよいか', '認証：この人は誰か'],
        ['受け取るもの', 'アクセストークン', 'ID トークン（誰がログインしたか）'],
        ['例', '「カレンダーの読み取りだけを許可する」', '「Google でログイン」']],
      colW: [2.4, 4.7, 4.7], rowH: 0.5,
      callout: 'パスワードを渡さないので、権限を絞れ、期限を付けられ、後から取り消せる',
      sub: '第7回の AIエージェントも、メールやカレンダーを使う許可を OAuth で受け取っている。',
    },

    { kind: 'section', n: '4.5', name: '実習：Web API を作って呼ぶ', tagline: '第3回の bottle を広げる' },
    {
      kind: 'code', kicker: '4.5　実習', title: '実習：JSON を返す API を作る（api.py）',
      code: [
        'from bottle import get, post, request, run',
        '',
        'posts = []',
        '',
        "@get('/api/posts')",
        'def list_posts():',
        "    return {'posts': posts}          # 辞書を返すと JSON になる",
        '',
        "@post('/api/posts')",
        'def add_post():',
        '    data = request.json              # 送られてきた JSON を読む',
        "    posts.append({'id': len(posts) + 1, 'text': data['text']})",
        "    return {'ok': True, 'count': len(posts)}",
        '',
        "run(host='localhost', port=8080)",
      ],
      codeH: 4.0, size: 11,
      sub: 'GET で一覧を返し、POST で1件を受け取る。bottle は、関数が辞書を返すと JSON にして Content-Type も付けてくれる。',
    },
    {
      kind: 'code', kicker: '4.5　実習', title: '呼んでみる',
      code: [
        'curl -X POST localhost:8080/api/posts \\',
        "     -H 'Content-Type: application/json' \\",
        `     -d '{"text": "こんにちは"}'`,
        '',
        'curl localhost:8080/api/posts',
        '# → {"posts": [{"id": 1, "text": "こんにちは"}]}',
      ],
      codeH: 2.6, size: 11,
      side: {
        title: 'やること',
        body: '① 2件投稿してから、一覧を取る。\n② サーバを止めて起動し直すと、投稿は消える。なぜか（三層構成の DB の層がない）。\n③ 存在しない URL を呼ぶと、何が返るか。\n④ 発展：iot-handson の受信サーバに、温度を JSON で POST する。',
      },
      sub: 'Windows の PowerShell では引用符の扱いが違う。curl.exe を使い、JSON はファイルに書いて -d @post.json で送るとよい。',
    },
  ],
  exercises: [
    ['4-1', 'HTTP はステートレスなのに、ログイン状態が続くのはなぜか。Cookie の働きから説明せよ。'],
    ['4-2', 'Cookie 型とサーバセッション型の違いを、強制的にログアウトさせるときの観点から説明せよ。'],
    ['4-3', '（手を動かす）実習の API に、投稿を1件消す DELETE /api/posts/<id> を追加せよ。'],
    ['4-4', 'OAuth を使うと、外部のアプリにパスワードを教えずに済むのはなぜか。アクセストークンの性質とともに説明せよ。'],
  ],
  summary: [
    ['Web アプリ', 'ブラウザ・アプリサーバ・DB の三層。HTTP がステートレスだからサーバを増やせる'],
    ['Cookie', 'ステートレスな HTTP に記憶を足す。状態をブラウザに持つか、サーバに持つか'],
    ['Web API', 'HTML の代わりに JSON を返す。REST では URL が名詞、メソッドが動詞'],
    ['押し出す通信', 'SSE は片方向、WebSocket は双方向。LLM の答えが少しずつ出るのは SSE'],
    ['OAuth', 'パスワードを渡さず、絞った権限をトークンで渡す。OpenID Connect は「誰か」を伝える'],
  ],
  next: '第5回　クラウド・仮想化・P2P',
};
