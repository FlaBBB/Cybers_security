const puppeteer = require("puppeteer");

const FLAG = process.env.FLAG;
const TARGET = process.env.TARGET;

const generateRandomString = (length) => {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
};

const sleep = async (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const visit = async (url) => {
  const browser = await puppeteer.launch({
    headless: "new",
    executablePath: "/usr/bin/google-chrome-stable",
    args: [
      "--no-sandbox",
      "--headless",
      "--disable-gpu",
      "--disable-dev-shm-usage",
    ],
  });
  const context = await browser.createIncognitoBrowserContext();
  const page = await context.newPage();

  try {
    const username = generateRandomString(16);
    const password = generateRandomString(16);

    // Register
    await page.goto(`https://${TARGET}/register`, { waitUntil: "networkidle0" });
    await page.evaluate((username, password) => {
      document.getElementsByName('username')[0].value = username;
      document.getElementsByName('password')[0].value = password;
      document.childNodes[1].childNodes[2].childNodes[1].childNodes[7].click();
    }, username, password);
    await sleep(1000);

    // Login
    await page.goto(`https://${TARGET}/login`, { waitUntil: "networkidle0" });
    await page.evaluate((username, password) => {
      document.getElementsByName('username')[0].value = username;
      document.getElementsByName('password')[0].value = password;
      document.childNodes[1].childNodes[2].childNodes[1].childNodes[7].click();
    }, username, password);
    await sleep(1000);

    await page.setCookie({
      name: "flag",
      value: FLAG,
      domain: TARGET,
      httpOnly: false,
      SameSite: "None",
    });
    await page.goto(url, {
      waitUntil: "networkidle0",
      timeout: 5 * 1000,
    });
    await sleep(5 * 1000);
  } catch (e) {
    console.log(e);
  } finally {
    await page.close();
    await context.close();
    await browser.close();
  }
};

module.exports = { visit: visit };
