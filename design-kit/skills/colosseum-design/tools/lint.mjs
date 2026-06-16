#!/usr/bin/env node
// Colosseum design-kit — anti-slop / brand 자가검사 (daemon-free)
// open-design daemon의 lint-artifact 최소 복제. craft/anti-ai-slop.md P0 + 콜로 하드룰.
// 사용: node lint.mjs <html-file>   (종료코드: P0 위반 시 1)

import { readFileSync } from "node:fs";

const file = process.argv[2];
if (!file) { console.error("usage: node lint.mjs <html-file>"); process.exit(2); }
const html = readFileSync(file, "utf8");

const P0 = [], P1 = [];
const add = (arr, rule, detail) => arr.push({ rule, detail });

// ── P0 (must-fix) ──
// 1. AI-tell indigo / 비-브랜드 accent (CL Blue 외 하드코딩)
const INDIGO = /#(6366f1|4f46e5|4338ca|3730a3|8b5cf6|7c3aed|a855f7)\b/gi;
const indigo = html.match(INDIGO);
if (indigo) add(P0, "indigo-accent", `Tailwind indigo 발견: ${[...new Set(indigo)].join(", ")} → CL Blue #005BF6 사용`);

// 2. UI 그라데이션 (콜로 금지, 로고 SVG 제외)
const noSvg = html.replace(/<svg[\s\S]*?<\/svg>/gi, "");
const grad = noSvg.match(/linear-gradient|radial-gradient|conic-gradient/gi);
if (grad) add(P0, "gradient", `그라데이션 ${grad.length}곳 → 콜로 UI 크롬 그라데이션 금지(단색+타입 위계)`);

// 3. 이모지 (프로덕션 UI 금지) — 픽토그래픽 emoji만. 화살표(→)·⌘·기술기호는 슬롭 아님 → 제외
const EMOJI = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{FE0F}]/gu;
const emoji = html.match(EMOJI);
if (emoji) add(P0, "emoji", `이모지 ${emoji.length}개(${[...new Set(emoji)].slice(0,6).join("")}) → Material Symbols Outlined 사용`);

// 4. serif (콜로는 Pretendard 단일)
if (/font-family[^;]*serif(?!\s*;?\s*\/\*ok\*\/)/i.test(html) && !/sans-serif/i.test(RegExp.lastMatch))
  add(P0, "serif", "serif 폰트 지정 → 콜로는 Pretendard 단일(위계는 크기·weight)");

// 5. weight 600 (콜로 금지)
if (/font-weight:\s*600|:\s*600\b/.test(html.replace(/\d{3,}/g, m => m === "600" ? "600" : "")) && /font-weight:\s*600/.test(html))
  add(P0, "weight-600", "font-weight:600 → 콜로는 500(Medium)/700(Bold)만, 600 미사용");

// ── P1 (should-fix) ──
// raw hex outside :root (대략) > 12
const hexAll = (html.match(/#[0-9a-f]{3,6}\b/gi) || []).length;
const rootBlock = (html.match(/:root\s*\{[\s\S]*?\}/i) || [""])[0];
const hexInRoot = (rootBlock.match(/#[0-9a-f]{3,6}\b/gi) || []).length;
const hexOutside = hexAll - hexInRoot;
if (hexOutside > 12) add(P1, "raw-hex", `:root 밖 raw hex ${hexOutside}개 → CSS 변수(var(--color-...)) 사용`);

// CL Blue 과다 — 마케팅 화면 기준 ≤2가 craft 규칙. admin은 active/selected/primary/code로
// 정당하게 더 씀 → admin 톨러런스로 임계 14. 마케팅 산출물이면 craft/color.md의 ≤2를 직접 적용.
const accentUses = (html.match(/#005BF6|var\(--clblue-500\)|var\(--color-(text|background|borders)-primary\)/gi) || []).length;
if (accentUses > 14) add(P1, "accent-overuse", `accent(CL Blue) 참조 ${accentUses}회 → 마케팅이면 화면당 2회로 제한(admin은 affordance 허용)`);

// lang
if (!/<html[^>]*lang="ko"/i.test(html)) add(P1, "lang", 'html lang="ko" 누락 → 한국어 우선');

// ── report ──
const fmt = (a, tag) => a.map(v => `  [${tag}] ${v.rule}: ${v.detail}`).join("\n");
console.log(`\n🔍 ${file}`);
if (!P0.length && !P1.length) { console.log("  ✓ 위반 없음 — 브랜드/anti-slop 통과"); process.exit(0); }
if (P0.length) console.log("P0 (must-fix):\n" + fmt(P0, "P0"));
if (P1.length) console.log("P1 (should-fix):\n" + fmt(P1, "P1"));
console.log(`\n총 P0 ${P0.length} · P1 ${P1.length}`);
process.exit(P0.length ? 1 : 0);
