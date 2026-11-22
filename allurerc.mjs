// Allure 3 report settings (https://allurereport.org/docs/v3/). No Java needed.
//   npx allure generate allure-results   →   allure-report/index.html, one file

// Without this the report would load a web analytics script when opened.
process.env.ALLURE_NO_ANALYTICS ??= "true";

export default {
  name: "BooKing Lab tests",
  output: "./allure-report",
  // Runs are added to this file; keep it between runs to see the trend (the Pages job does).
  historyPath: "./allure-history/history.jsonl",
  historyLimit: 20,
  plugins: {
    allure2: { options: { singleFile: true, reportName: "BooKing Lab tests" } },
  },
};
