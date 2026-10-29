import test from "node:test";
import assert from "node:assert/strict";
import { createHmac } from "node:crypto";
import { verifyTelegramInitData } from "../lib/telegram.js";
import { createSession, verifySession } from "../lib/session.js";

function makeInitData(botToken, user, authDate) {
  const params = new URLSearchParams();
  params.set("auth_date", String(authDate));
  params.set("query_id", "AAE-test-query");
  params.set("user", JSON.stringify(user));
  const entries = Array.from(params.entries()).sort(([a],[b])=>a.localeCompare(b));
  const checkString = entries.map(([key,value])=>key+"="+value).join("\n");
  const secret = createHmac("sha256","WebAppData").update(botToken).digest();
  params.set("hash",createHmac("sha256",secret).update(checkString).digest("hex"));
  return params.toString();
}

test("Telegram initData verifies a valid signature and returns safe identity fields",()=>{
  const now=1_800_000_000;
  const initData=makeInitData("test-bot-token",{id:123456789,first_name:"PaidMX Tester",username:"tester"},now-30);
  const user=verifyTelegramInitData(initData,"test-bot-token",now);
  assert.equal(user.id,"123456789");
  assert.equal(user.username,"tester");
  assert.equal(user.firstName,"PaidMX Tester");
});

test("Telegram initData rejects a tampered payload",()=>{
  const now=1_800_000_000;
  const initData=makeInitData("test-bot-token",{id:123456789,first_name:"Tester"},now-30).replace("Tester","Intruder");
  assert.throws(()=>verifyTelegramInitData(initData,"test-bot-token",now),/signature/i);
});

test("Telegram initData rejects stale auth dates",()=>{
  const now=1_800_000_000;
  const initData=makeInitData("test-bot-token",{id:123456789,first_name:"Tester"},now-90000);
  assert.throws(()=>verifyTelegramInitData(initData,"test-bot-token",now),/expired/i);
});

test("signed sessions restore the same user and reject expiration",()=>{
  const secret="test-session-secret-that-is-long-enough-123456";
  const session=createSession("123456789",secret,1000);
  assert.equal(verifySession(session.token,secret,1001).userId,"123456789");
  assert.equal(verifySession(session.token,secret,1000+7*24*60*60),null);
});
