# 通信工学通論（アプリケーション層編）

九州大学 学部講義「通信工学通論」のうち、TCP/IP の**アプリケーション層**を扱う回の講義資料。

90分 × 全8回。インターネットの構成から、DNS・電子メール・HTTP・Web API・クラウドを経て、
LLM と AIエージェント、セキュリティまでを一本の線でつなぐ構成。
アプリケーション層より下（トランスポート層以下）は「中身を見ない土管」として扱う。

## 講義一覧

| 回 | 題目 | 今回の問い |
| ---: | --- | --- |
| 1 | インターネットとアプリケーション層 | 普段使っているアプリは、ネットワークの上で何をやりとりしているのか |
| 2 | DNS と電子メール | 名前しか知らない相手に、どうやって届けるのか。届いたメールは本物か |
| 3 | WWW と HTTP | ブラウザがページを表示するまでに、何が起きているのか |
| 4 | Web アプリケーションと Web API | 状態を持たない HTTP の上で、ログインや掲示板はどう作られているのか |
| 5 | クラウド・仮想化・P2P | アプリはどこで動いているのか。サーバを置かずに動かす形はありうるのか |
| 6 | LLM のしくみと API | LLM は何をしていて、ネットワークの上でどう使われているのか |
| 7 | AIエージェントと MCP | AIエージェントは、ネットワークの上で何をしているのか。何を任せてよいのか |
| 8 | セキュリティ：暗号・認証・Web・AI | 顔の見えない相手を、どう信用するのか。AI に何を任せてよいのか |

各回の時間配分と、流用した素材の対応は [講義計画_アプリケーション層8回.md](講義計画_アプリケーション層8回.md) にある。

## 構成

| パス | 内容 |
| --- | --- |
| `slides/第NN回_*.pptx` | 各回のスライド（PowerPoint 版） |
| `slides/html/第NN回_*.html` | 各回のスライド（HTML 版）。1ファイルで完結する |
| `slides/md/第NN回_*.md` | 各回のスライド（Markdown 版。Marp 形式） |
| `slides/decks/lecNN.js` | 各回の内容。pptx・HTML・Markdown の3つの版で共用する |
| `slides/tools/` | 組み立ての道具（`kit.js` が pptx の体裁、`kit-html.js` が HTML の体裁） |
| `figures/fig-NN-MM.svg` | この講義のために描いた図 |
| `figures/fig-co-*.svg` | [CompOutline](https://github.com/koide55/CompOutline)（コンピュータシステム通論）から複製した図 |
| `tools/figs/netNN.py` | 図を描くプログラム |

スライドの組み立ての仕組みは CompOutline のものを引き継いでいる。
**内容を直すときは `slides/decks/lecNN.js` を直し、3つの版を書き出し直す。**

## 作り直す

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # 最初の1回だけ
(cd slides && npm install)                                            # 最初の1回だけ
```

```bash
python3 tools/build_figures.py     # 図の SVG を描く
slides/tools/figs2png.sh           # SVG を pptx 用の PNG にする
node slides/tools/build.js         # pptx（回番号を渡せばその回だけ）
node slides/tools/build-html.js    # HTML
node slides/tools/build-md.js      # Markdown
```

講義名は `slides/tools/kit.js`・`kit-html.js`・`build-md.js` の `COURSE` で変えられる。

## 実習で使う教材

| 回 | 教材 |
| --- | --- |
| 3・4・8 | [webapp-security-programming-handson](https://github.com/koide55/webapp-security-programming-handson) |
| 4 | [LectureWebApp001](https://github.com/koide55/LectureWebApp001)（vuln-webapp） |
| 5 | [docker-lesson](https://github.com/koide55/docker-lesson) |
| 6・7 | [theme12-seminar](https://github.com/koide55/theme12-seminar)（OpenAI API のキーが要る） |
| 8 | [LecturePassKey](https://github.com/koide55/LecturePassKey) |

脆弱性の実習で使うアプリは、意図的に脆弱にしてある。自分の PC の中だけで動かすこと。

## 元にした資料

旧教材 `network2026.pptx`（約100MB）は、GitHub の1ファイルの上限を超えるためリポジトリに含めていない。
