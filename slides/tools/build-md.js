#!/usr/bin/env node
// Markdown（Marp 形式）のスライドを書き出す。  node slides/tools/build-md.js [回番号 …]
//
// 入力は decks/lecNN.js。pptx を組む build.js、HTML を組む build-html.js と同じデータを読む。
// 1枚のスライドを `---` で区切る。Marp でそのままスライドとして表示でき、普通の Markdown としても読める。
// 図は figures/ の SVG を相対パスで参照する（slides/md/ から ../../figures/）。
const path = require('path');
const fs = require('fs');

const ROOT = path.join(__dirname, '..', '..');
const OUT = path.join(ROOT, 'slides', 'md');
const COURSE = '通信工学通論';   // 講義名。kit.js・kit-html.js と揃える

const want = process.argv.slice(2).map((v) => parseInt(v, 10)).filter(Number.isFinite);
const nums = want.length ? want : Array.from({ length: 8 }, (_, i) => i + 1);

// --- 文字の整形 -------------------------------------------------------
// コードブロックの外の「<」は HTML のタグと見なされて消えるので逃がす（例：/api/posts/<id>）
const esc = (t) => String(t).replace(/</g, '&lt;');
// 本文の改行は Markdown の改行（行末の空白2つ）に、空行は段落の区切りにする
const para = (t) => esc(t).split('\n').map((l) => l.trimEnd()).join('  \n').replace(/ {2}\n {2}\n/g, '\n\n');
// 表のセルでは改行を <br> に、縦棒を逃がす
const cell = (t) => esc(t).replace(/\|/g, '\\|').replace(/\n/g, '<br>');

function table(rows) {
  const [head, ...body] = rows;
  const line = (r) => `| ${r.map(cell).join(' | ')} |`;
  return [line(head), `| ${head.map(() => '---').join(' | ')} |`, ...body.map(line)].join('\n');
}

function code(lines) {
  return ['```', ...lines, '```'].join('\n');
}

function figure(name, alt, h) {
  // Marp は代替テキストの「h:400」を高さの指定として読む。他の表示環境では代替テキストになるだけ
  return `![h:${h} ${alt}](../../figures/fig-${name}.svg)`;
}

function callout(c) {
  if (!c) return null;
  if (Array.isArray(c)) return `> **${c[0]}**  \n> ${c[1]}`;
  return `> **${c}**`;
}

const note = (t) => (t ? `**${para(t)}**` : null);
const kick = (k) => (k ? `<!-- ${k} -->` : null);

// --- スライドの種類ごとの書き方 ---------------------------------------
function render(sl) {
  const out = [];
  const push = (...xs) => xs.forEach((x) => { if (x) out.push(x); });
  switch (sl.kind) {
    case 'section':
      push('<!-- _class: lead -->', `# ${sl.n}　${sl.name}`, sl.tagline && `*${sl.tagline}*`);
      break;
    case 'cards':
      push(kick(sl.kicker), `## ${sl.title}`, sl.lead && para(sl.lead));
      push(sl.items.map(([h, b]) => `- **${esc(h)}** — ${b ? para(b) : ''}`.trimEnd()).join('\n'));
      push(callout(sl.callout), note(sl.note));
      break;
    case 'bullets':
      push(kick(sl.kicker), `## ${sl.title}`, sl.lead && para(sl.lead));
      push(sl.items.map((t) => {
        const [text, lvl] = Array.isArray(t) ? t : [t, 0];
        return `${'  '.repeat(lvl)}- ${esc(text)}`;
      }).join('\n'));
      push(note(sl.note));
      break;
    case 'figure':
      push(kick(sl.kicker), `## ${sl.title}`, sl.lead && para(sl.lead));
      push(figure(sl.fig, sl.title, sl.lead ? 360 : 440));
      push(sl.caption && para(sl.caption), sl.sub && para(sl.sub));
      break;
    case 'table':
      push(kick(sl.kicker), `## ${sl.title}`, sl.lead && para(sl.lead));
      push(table(sl.rows), callout(sl.callout), sl.sub && para(sl.sub), note(sl.note));
      break;
    case 'code':
      push(kick(sl.kicker), `## ${sl.title}`, sl.lead && para(sl.lead), code(sl.code));
      if (sl.side) push(`**${sl.side.title}**`, para(sl.side.body));
      push(sl.sub && para(sl.sub), note(sl.note));
      break;
    case 'split':
      push(kick(sl.kicker), `## ${sl.title}`, sl.lead && para(sl.lead));
      [sl.left, sl.right].forEach((col) => {
        push(`### ${col.title}`);
        if (col.code) push(code(col.code));
        if (col.rows) push(table(col.rows));
        if (col.items) push(col.items.map((t) => `- ${esc(t)}`).join('\n'));
        push(col.body && para(col.body), col.note && `*${col.note}*`);
      });
      push(note(sl.note));
      break;
    case 'statement':
      push(kick(sl.kicker), `## ${sl.title}`, sl.lead && para(sl.lead), callout(sl.statement));
      if (sl.map) push(sl.map.map(([a, b]) => `- ${esc(a)} → **${esc(b)}**`).join('\n'));
      push(sl.sub && para(sl.sub), note(sl.note));
      break;
    case 'steps':
      push(kick(sl.kicker), `## ${sl.title}`, sl.lead && para(sl.lead));
      push(sl.steps.map(([h, b], i) => `${i + 1}. **${esc(h)}** — ${esc(b).replace(/\n/g, '　')}`).join('\n'));
      push(sl.sub && para(sl.sub), note(sl.note));
      break;
    default:
      throw new Error('不明な kind: ' + sl.kind);
  }
  return out.join('\n\n');
}

function build(sp) {
  const slides = [];
  // 表紙
  slides.push(['<!-- _class: lead -->', `${COURSE}`, `# 第${sp.no}回　${sp.title}`,
    `*${sp.question}*`, '九州大学'].join('\n\n'));
  (sp.preface || []).forEach((sl) => slides.push(render(sl)));
  // 今回の問い
  slides.push(['<!-- _class: lead -->', '## 今回の問い',
    `> **${para(sp.bigQuestion || sp.question)}**`,
    sp.questionSub, 'この90分で、この問いに答えを出す。'].filter(Boolean).join('\n\n'));
  // 到達目標
  slides.push([`## 到達目標`,
    sp.goals.map(([h, b], i) => `${i + 1}. **${esc(h)}** ${esc(b)}`).join('\n')].join('\n\n'));
  sp.slides.forEach((sl) => slides.push(render(sl)));
  // 演習
  if (sp.exercises && sp.exercises.length) {
    slides.push(['## 演習', sp.exercises.map(([n, t]) => `- **${n}**　${esc(t)}`).join('\n')].join('\n\n'));
  }
  // まとめ
  slides.push(['## まとめ', table([['', ''], ...sp.summary]).replace(/^\|  \|  \|\n\| --- \| --- \|\n/, '| 項目 | 要点 |\n| --- | --- |\n'),
    sp.next && `次回　${sp.next}`].filter(Boolean).join('\n\n'));

  const front = ['---', 'marp: true', 'paginate: true', 'size: 16:9',
    `title: 第${sp.no}回 ${sp.title}`, '---'].join('\n');
  const header = [
    `<!-- ${COURSE}　第${sp.no}回 ${sp.title} -->`,
    `<!-- slides/decks/lec${String(sp.no).padStart(2, '0')}.js から node slides/tools/build-md.js で書き出したもの。`,
    '     pptx 版・HTML 版と同じ内容。直すときは decks の側を直して書き出し直す。 -->',
  ].join('\n');
  return { md: `${front}\n\n${header}\n\n${slides.join('\n\n---\n\n')}\n`, n: slides.length };
}

fs.mkdirSync(OUT, { recursive: true });
for (const n of nums) {
  const f = path.join(ROOT, 'slides', 'decks', `lec${String(n).padStart(2, '0')}.js`);
  let spec;
  try { spec = require(f); } catch (e) {
    if (e.code === 'MODULE_NOT_FOUND') { console.log(`第${n}回: 未作成`); continue; }
    throw e;
  }
  const { md, n: pages } = build(spec);
  const name = `第${String(n).padStart(2, '0')}回_${spec.title}.md`;
  fs.writeFileSync(path.join(OUT, name), md, 'utf8');
  console.log(`第${n}回  ${pages} 枚  ${name}`);
}
