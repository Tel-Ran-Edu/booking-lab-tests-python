// Writes a short pass/fail table of the last Allure report, in Markdown.
//   node scripts/report-summary.mjs [allure-report]
// In GitHub Actions it goes to the job summary ($GITHUB_STEP_SUMMARY); elsewhere to the console.
import { appendFileSync, existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

const dir = process.argv[2] ?? "allure-report";
const file = join(dir, "test-results.json");
const lines = ["## Test results", ""];

if (!existsSync(file)) {
  lines.push("No report was generated: the tests did not run. See the job log.");
} else {
  const tests = Object.values(JSON.parse(readFileSync(file, "utf8")).byId);
  const count = (status) => tests.filter((t) => t.status === status).length;
  const icons = { passed: "✅", failed: "❌", broken: "💥", skipped: "⏭️", unknown: "❔" };
  lines.push("| Status | Tests |", "| --- | --- |");
  for (const status of Object.keys(icons)) {
    if (count(status)) lines.push(`| ${icons[status]} ${status} | ${count(status)} |`);
  }
  lines.push(`| **total** | **${tests.length}** |`, "");
  const bad = tests.filter((t) => t.status === "failed" || t.status === "broken");
  if (bad.length) {
    lines.push("**Not passed:**", "", ...bad.map((t) => `- ${icons[t.status]} ${t.name}`), "");
  }
  lines.push("The full report is the `allure-report` artifact of this run: download it and open "
    + "`index.html`.");
}

const text = `${lines.join("\n")}\n`;
if (process.env.GITHUB_STEP_SUMMARY) appendFileSync(process.env.GITHUB_STEP_SUMMARY, text);
else process.stdout.write(text);
