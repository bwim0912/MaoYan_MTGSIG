const fs = require("fs");

const sourcePath = process.argv[2] || "C:\\Users\\hp\\PycharmProjects\\pythonProject\\js逆向\\猫眼\\猫眼_code.js";
const source = fs.readFileSync(sourcePath, "utf8");

const targetUrl =
  process.env.MAOYAN_URL ||
  "https://piaofang.maoyan.com/i/api/encrypt/dashboard-ajax/movie" +
  "?showDate=20260925&movieId=&orderType=1&yodaReady=h5" +
  "&csecplatform=4&csecversion=4.3.0";

const dfpId =
  process.env.WEBDFPID ||
  "2yyw47xwz0475y41z14yv24w4xvzz4vw8z9w9757036679584817wz9v";

const requestHeaders = {
  accept: "application/json, text/plain, */*",
  "accept-language": "zh-CN,zh;q=0.9",
  channelid: "40009",
  "m-appkey": "fe_com.sankuai.movie.fe.ipro",
  "m-traceid": "-3856982171655403735",
  referer: "https://piaofang.maoyan.com/i/dashboard/movie",
  "sec-ch-ua": "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Google Chrome\";v=\"140\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-origin",
  uid: "86a7cabae1a5a584c9dbc6973a9d490dd8084ed0",
  "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
  uuid: "1a0d0242425c8-0f704622b11fd68-26061951-240000-1a0d0242425c8",
};

const fullPath =
  process.env.H5GUARD_FULL ||
  "C:\\Users\\hp\\.codex\\attachments\\e6a1ab6f-c0eb-46dd-8006-96d527910c65\\Pasted text.txt";
const full = fs.readFileSync(fullPath, "utf8");
const opcodeMatch = full.match(/\$_c_Nk\s*=\s*(\[[\s\S]*?\]),\s*a\s*=/);
if (!opcodeMatch) {
  throw new Error("无法从完整 H5guard 文件提取 $_c_Nk");
}

const bOStart = full.indexOf("function bO(");
const bXStart = full.indexOf("function bX(", bOStart);
if (bOStart < 0 || bXStart < 0) {
  throw new Error("无法从完整 H5guard 文件提取 bO/bW 辅助代码");
}
const bHelpers = full.slice(bOStart, bXStart);

const helpers = `
const $_c_Nk = ${opcodeMatch[1]};
${bHelpers}

function hy(k5) {
  const out = [];
  for (let i = 0; i < k5.length; i += 2) {
    out.push(parseInt(k5.slice(i, i + 2), 16));
  }
  return out;
}

function hw(k5 = []) {
  return k5.map((x) => {
    const n = x & 255;
    return "0123456789abcdef"[n >>> 4] + "0123456789abcdef"[n & 15];
  }).join("");
}

function hx(k5) {
  return [k5 >>> 24 & 255, k5 >>> 16 & 255, k5 >>> 8 & 255, k5 & 255];
}

function hs(k5) {
  return [k5 >>> 24 & 255, k5 >>> 16 & 255, k5 >>> 8 & 255, k5 & 255];
}

function d7() {
  return ${JSON.stringify(dfpId)};
}
`;

let runnable = source;
runnable = runnable.replace(
  "var ks = [];",
  "var ks = [];\n" + helpers
);

const oldTest = /\/\/ ================= 5\. 测试生成 =================[\s\S]*$/;
const newTest = `
function getMtgSig(url) {
  const request = {
    url,
    method: "GET",
    headers: Object.assign({}, requestHeaders),
    data: null,
    SCaApp: false,
    isKaptor: false
  };
  k9 = Date.now();
  return hq(request, true);
}

const signed = getMtgSig(targetUrl);
const signature = signed.headers && signed.headers.mtgsig;
if (!signature) {
  throw new Error("签名生成失败：返回对象中没有 headers.mtgsig");
}
console.log(signature);
`;

runnable = runnable.replace(oldTest, newTest);
if (runnable === source) {
  throw new Error("没有成功替换原始测试入口");
}

global.targetUrl = targetUrl;
global.requestHeaders = requestHeaders;
eval(runnable);
