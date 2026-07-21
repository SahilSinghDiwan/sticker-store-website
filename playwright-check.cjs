const { chromium } = require("playwright");

const baseURL = process.env.BASE_URL || "http://frontend:80";

async function check(path) {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  const consoleLogs = [];
  const pageErrors = [];

  page.on("console", (msg) => {
    consoleLogs.push(`[${msg.type()}] ${msg.text()}`);
  });
  page.on("pageerror", (err) => {
    pageErrors.push(err.message);
  });

  const url = `${baseURL}${path}`;
  const response = await page.goto(url, { waitUntil: "networkidle", timeout: 30000 });

  await page.waitForTimeout(2000);

  const title = await page.title();
  const rootText = await page.locator("#root").innerText().catch(() => "");
  const rootHtml = await page.locator("#root").innerHTML().catch(() => "");
  const bodyText = await page.locator("body").innerText().catch(() => "");

  console.log(`\n=== ${path} ===`);
  console.log(`URL: ${url}`);
  console.log(`HTTP: ${response?.status()}`);
  console.log(`Title: ${title}`);
  console.log(`Root text length: ${rootText.length}`);
  console.log(`Body text preview: ${bodyText.slice(0, 300).replace(/\n/g, " ")}`);
  console.log(`Root HTML preview: ${rootHtml.slice(0, 500)}`);

  if (pageErrors.length) {
    console.log("Page errors:");
    pageErrors.forEach((e) => console.log(`  - ${e}`));
  }

  if (consoleLogs.length) {
    console.log("Console:");
    consoleLogs.slice(0, 20).forEach((l) => console.log(`  ${l}`));
  }

  const slug = path.replace(/\//g, "_") || "home";
  await page.screenshot({ path: `/artifacts/screenshot-${slug}.png`, fullPage: true });
  await browser.close();
}

(async () => {
  await check("/");
  await check("/login");
})();
