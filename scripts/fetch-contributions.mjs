// Merges the public GitHub contribution calendars (what a logged-out visitor sees) of several accounts
// into src/data/contributions.json. Writes nothing unless every year of every account parses.
import { writeFileSync } from 'node:fs';

const ACCOUNTS = ['arunima811', 'arunima-rokt'];
// The site shows the last 53 weeks, which can reach back into the calendar year before last.
const YEARS_BACK = 2;
const OUT = 'src/data/contributions.json';
const TIMEOUT_MS = 30_000;

const DAY_CELL = /<td\b[^>]*\bdata-date="[^"]*"[^>]*>/g;
const TOOLTIP = /<tool-tip\b([^>]*)>([^<]*)<\/tool-tip>/g;

const attr = (tag, name) => tag.match(new RegExp(`\\b${name}="([^"]*)"`))?.[1];

function parseCount(label, login, year) {
  const match = label.trim().match(/^(No|[\d,]+) contributions? on /);
  if (!match) throw new Error(`${login} ${year}: unexpected day label "${label.trim()}"; GitHub's calendar markup may have changed`);
  return match[1] === 'No' ? 0 : Number(match[1].replace(/,/g, ''));
}
const daysIn = (year) => (new Date(Date.UTC(year, 1, 29)).getUTCMonth() === 1 ? 366 : 365);

async function calendarDays(login, year) {
  const url = `https://github.com/users/${login}/contributions?from=${year}-01-01&to=${year}-12-31`;
  const res = await fetch(url, { headers: { 'user-agent': 'arunima-site' }, signal: AbortSignal.timeout(TIMEOUT_MS) });
  if (!res.ok) throw new Error(`${login} ${year}: HTTP ${res.status}`);
  const html = await res.text();

  const dateById = new Map([...html.matchAll(DAY_CELL)].map(([tag]) => [attr(tag, 'id'), attr(tag, 'data-date')]));
  const days = [...html.matchAll(TOOLTIP)]
    .map(([, attrs, label]) => ({ date: dateById.get(attr(attrs, 'for')), count: parseCount(label, login, year) }))
    .filter(({ date }) => date?.startsWith(`${year}-`));

  if (days.length !== daysIn(year)) {
    throw new Error(`${login} ${year}: parsed ${days.length} days, expected ${daysIn(year)}; GitHub's calendar markup may have changed`);
  }
  return days;
}

async function main() {
  const lastYear = new Date().getUTCFullYear();
  const calendars = [];
  for (const login of ACCOUNTS) {
    for (let year = lastYear - YEARS_BACK; year <= lastYear; year++) {
      calendars.push({ login, year, days: await calendarDays(login, year) });
    }
  }

  const merged = calendars
    .flatMap(({ days }) => days)
    .filter(({ count }) => count > 0)
    .reduce((acc, { date, count }) => ({ ...acc, [date]: (acc[date] ?? 0) + count }), {});
  const days = Object.fromEntries(Object.entries(merged).sort(([a], [b]) => a.localeCompare(b)));

  writeFileSync(OUT, `${JSON.stringify({ generatedAt: new Date().toISOString(), accounts: ACCOUNTS, days }, null, 2)}\n`);
  console.table(
    Object.fromEntries(
      calendars
        .map(({ login, year, days: d }) => [`${login} ${year}`, d.reduce((sum, { count }) => sum + count, 0)])
        .filter(([, total]) => total > 0),
    ),
  );
}

main().catch((err) => {
  console.error(`fetch-contributions: ${err.message}`);
  process.exit(1);
});
