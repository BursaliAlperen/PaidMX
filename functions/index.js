const { onRequest } = require("firebase-functions/v2/https");
const { defineSecret } = require("firebase-functions/params");
const { initializeApp } = require("firebase-admin/app");
const { getFirestore, FieldValue } = require("firebase-admin/firestore");
const crypto = require("node:crypto");

initializeApp();
const db = getFirestore();
const BOT_TOKEN = defineSecret("BOT_TOKEN");
const DAY = 86400000;
const DEFAULTS = {
  spin_daily_limit: 20, spin_cooldown_sec: 300, min_withdraw_gr: 1000,
  withdraw_min_plays: 5, game_daily_plays: 2, game_min_elapsed_sec: 8,
  game_max_elapsed_sec: 180, promo_fail_daily_limit: 5,
  daily_rewards: [100,100,175,250,300,400,750],
  features: { daily: true, promo: true, withdraw: true, tasks: true, game: true, spin: true },
  ref: { join: 50, bonus: 200, threshold: 300, pct: 2 },
  wheel: [{id:0,gr:5,weight:30},{id:1,gr:10,weight:25},{id:2,gr:5,weight:20},{id:3,gr:20,weight:12},{id:4,gr:0,weight:8},{id:5,gr:10,weight:3},{id:6,gr:50,weight:1},{id:7,gr:100,weight:1}],
  game: { k:[80,.9,.06], n:[125,1.2,.12], z:[150,1.6,.2] }
};
const ADMIN_IDS = new Set((process.env.ADMIN_IDS || "").split(",").map(x=>x.trim()).filter(Boolean));
const now = () => Date.now();
const dayBucket = t => Math.floor(t / DAY);
const num = (v,min=0,max=1e9) => Number.isSafeInteger(Number(v)) && Number(v)>=min && Number(v)<=max ? Number(v) : null;
const clean = (v,n=120) => String(v ?? "").trim().slice(0,n);
class ApiError extends Error { constructor(code, extra={}) { super(code); this.code=code; this.extra=extra; } }
function send(res,status,body){res.status(status).set("Content-Type","application/json").send(body);}
function allowedOrigin(origin){return (process.env.CORS_ORIGINS||"").split(",").map(x=>x.trim()).includes(origin);}
function verifyTelegramInitData(initData, token) {
  if(typeof initData!=="string"||!initData||initData.length>8192) throw new ApiError("telegram_auth_required");
  const p=new URLSearchParams(initData), hash=p.get("hash"), authDate=Number(p.get("auth_date"));
  if(!hash||!Number.isInteger(authDate)) throw new ApiError("telegram_auth_invalid");
  const t=Math.floor(now()/1000);
  if(authDate>t+60||t-authDate>86400) throw new ApiError("telegram_auth_expired");
  p.delete("hash");
  const check=[...p.entries()].sort(([a],[b])=>a.localeCompare(b)).map(([k,v])=>k+"="+v).join("\n");
  const secret=crypto.createHmac("sha256","WebAppData").update(token).digest();
  const expected=crypto.createHmac("sha256",secret).update(check).digest("hex");
  const a=Buffer.from(expected,"hex"), b=Buffer.from(hash,"hex");
  if(a.length!==b.length||!crypto.timingSafeEqual(a,b)) throw new ApiError("telegram_auth_invalid");
  const raw=p.get("user"); if(!raw) throw new ApiError("telegram_user_missing");
  const user=JSON.parse(raw); if(!Number.isSafeInteger(Number(user.id))) throw new ApiError("telegram_user_invalid");
  return {...user,id:String(user.id),authDate};
}
async function getUser(id){const r=db.collection("users").doc(id),s=await r.get();if(!s.exists)throw new ApiError("user_missing");return {ref:r,...s.data()};}
async function touchUser(tg){
  const ref=db.collection("users").doc(tg.id), snap=await ref.get();
  const profile={telegramId:tg.id,firstName:clean(tg.first_name,128),username:clean(tg.username,64),photoUrl:clean(tg.photo_url,2048),lastSeenAt:now(),updatedAt:now()};
  if(!snap.exists) await ref.create({...profile,balanceGr:0,playsTotal:0,totalWithdrawnGr:0,spinsTotal:0,banned:false,lang:"tr",streak:0,lastDailyAt:0,dailyNextAt:0,lastSpinAt:0});
  else await ref.set(profile,{merge:true});
  const u=(await ref.get()).data();
  if(u.banned) throw new ApiError("banned");
  return {ref,...u,id:tg.id};
}
async function settings(){const s=await db.collection("system").doc("settings").get();return {...DEFAULTS,...(s.exists?s.data():{}),features:{...DEFAULTS.features,...(s.exists?s.data().features||{}:{})}};}
async function ensureSeed(){
  const b=db.batch();
  for(const x of DEFAULTS.wheel)b.set(db.collection("wheelSegments").doc(String(x.id)),{...x,active:true},{merge:true});
  for(const [tier,v] of Object.entries(DEFAULTS.game))b.set(db.collection("gameTiers").doc(tier),{tier,capGr:v[0],speed:v[1],bombRate:v[2],durationSec:30,maxRawScore:tier==="k"?250:tier==="n"?350:450,active:true},{merge:true});
  await b.commit();
}
async function credit(userId,kind,gr,meta={}){
  if(!num(gr,0))throw new ApiError("invalid_amount");
  const ref=db.collection("users").doc(userId), led=db.collection("ledger").doc();
  return db.runTransaction(async tx=>{const s=await tx.get(ref);if(!s.exists||s.data().banned)throw new ApiError("banned");const balance=(s.data().balanceGr||0)+gr;tx.update(ref,{balanceGr:balance,updatedAt:now()});tx.set(led,{userId,kind,grDelta:gr,grAfter:balance,meta,createdAt:now()});return {balance};});
}
async function debit(userId,kind,gr,meta={}){
  const ref=db.collection("users").doc(userId),led=db.collection("ledger").doc();
  return db.runTransaction(async tx=>{const s=await tx.get(ref);if(!s.exists||s.data().banned)throw new ApiError("banned");const bal=s.data().balanceGr||0;if(bal<gr)throw new ApiError("insufficient");const balance=bal-gr;tx.update(ref,{balanceGr:balance,updatedAt:now()});tx.set(led,{userId,kind,grDelta:-gr,grAfter:balance,meta,createdAt:now()});return {balance};});
}
async function audit(actorId,action,target,detail){await db.collection("auditLog").add({actorId,action,target:String(target??""),detail:detail||null,createdAt:now()});}
function requireAdmin(id){if(!ADMIN_IDS.has(id))throw new ApiError("forbidden");}
async function rpc(name,p,u){
  const t=now(), day=dayBucket(t), uid=u.id, userRef=u.ref, s=await settings();
  if(name==="authCheck")return {ok:true,user:{id:uid},admin:ADMIN_IDS.has(uid)};
  if(name==="lang"){const lang=clean(p.lang,2);if(!["tr","en","ar","ru","es","pt","hi","id","zh"].includes(lang))throw new ApiError("invalid_lang");await userRef.update({lang});return {lang};}
  if(name==="me"){
    const [hist,done,wd,plays,refRows]=await Promise.all([
      db.collection("ledger").where("userId","==",uid).orderBy("createdAt","desc").limit(30).get(),
      db.collection("userTasks").where("userId","==",uid).where("status","==","done").get(),
      db.collection("withdrawals").where("userId","==",uid).where("status","==","pending").limit(1).get(),
      db.collection("gamePlays").where("userId","==",uid).where("dayBucket","==",day).get(),
      db.collection("referrals").where("referrerId","==",uid).get()
    ]);
    const spins=(u.spinDay===day?u.spinCount||0:0), gameUsed=(u.gameDay===day?u.gameCount||0:0);
    const best=plays.docs.reduce((m,d)=>Math.max(m,d.data().score||0),0);
    const earned=refRows.docs.reduce((a,d)=>a+(d.data().pctEarnedGr||0)+(d.data().activeBonusGr||0),0);
    return {user:{id:uid,name:u.firstName,photo:u.photoUrl||null},lang:u.lang||"tr",balance:u.balanceGr||0,plays:u.playsTotal||0,left:Math.max(0,s.spin_daily_limit-spins),history:hist.docs.filter(d=>(d.data().grDelta||0)>0).map(d=>({kind:d.data().kind,amt:d.data().grDelta,ts:d.data().createdAt})),daily:{day:u.streak||0,next:u.dailyNextAt||0},ref:{earned,friends:refRows.size,active:refRows.docs.filter(d=>d.data().status==="active").length},game:{left:Math.max(0,s.game_daily_plays-gameUsed),best,today:plays.size,lb:[]},tasksDone:done.docs.map(d=>d.data().taskId),withdrawalPending:!wd.empty,admin:ADMIN_IDS.has(uid),withdrawn:u.totalWithdrawnGr||0,minWd:s.min_withdraw_gr,wdPlays:s.withdraw_min_plays};
  }
  if(name==="config"){
    const [segs,tiers,tasks]=await Promise.all([db.collection("wheelSegments").where("active","==",true).get(),db.collection("gameTiers").where("active","==",true).get(),db.collection("tasks").where("active","==",true).orderBy("sort").get()]);
    const game={};tiers.forEach(d=>{const x=d.data();game[x.tier]=[x.capGr,x.speed,x.bombRate];});
    return {seg:segs.docs.map(d=>({id:Number(d.id),gr:d.data().gr})).sort((a,b)=>a.id-b.id),daily:s.spin_daily_limit,cooldown:s.spin_cooldown_sec,features:s.features,minWd:s.min_withdraw_gr,wdPlays:s.withdraw_min_plays,dailyRewards:s.daily_rewards,gameDaily:s.game_daily_plays,ref:s.ref,game,tasks:tasks.docs.map(d=>({id:d.id,...d.data(),desc:d.data().description,img:false})),lb:[]};
  }
  if(name==="spin"){
    if(!s.features.spin)throw new ApiError("feature_off");
    const key=clean(p.key,80);if(!key)throw new ApiError("invalid_key");
    const resultRef=db.collection("idempotency").doc(uid+"_spin_"+key);
    return db.runTransaction(async tx=>{
      const idem=await tx.get(resultRef);if(idem.exists)return idem.data().response;
      const us=await tx.get(userRef),v=us.data();const count=v.spinDay===day?v.spinCount||0:0;
      if(count>=s.spin_daily_limit)throw new ApiError("daily_limit");
      if((v.lastSpinAt||0)+s.spin_cooldown_sec*1000>t)throw new ApiError("cooldown",{retry:Math.ceil(((v.lastSpinAt||0)+s.spin_cooldown_sec*1000-t)/1000)});
      const segSnap=await tx.get(db.collection("wheelSegments").where("active","==",true));const segs=segSnap.docs.map(d=>d.data());const total=segs.reduce((a,x)=>a+(x.weight||1),0);let r=Math.random()*total,seg=segs.find(x=>(r-=x.weight||1)<0)||segs[0];
      const balance=(v.balanceGr||0)+(seg.gr||0);tx.update(userRef,{spinDay:day,spinCount:count+1,lastSpinAt:t,spinsTotal:(v.spinsTotal||0)+1,balanceGr:balance});
      tx.set(db.collection("ledger").doc(),{userId:uid,kind:"wheel",grDelta:seg.gr||0,grAfter:balance,createdAt:t,meta:{segment:seg.id}});
      const out={segment:seg.id,gr:seg.gr||0,balance};tx.create(resultRef,{response:out,createdAt:t});return out;
    });
  }
  if(name==="daily"){
    if(!s.features.daily)throw new ApiError("feature_off");const key=clean(p.key,80),idem=db.collection("idempotency").doc(uid+"_daily_"+key);
    return db.runTransaction(async tx=>{const [ir,ur]=await Promise.all([tx.get(idem),tx.get(userRef)]);if(ir.exists)return ir.data().response;const v=ur.data();if((v.dailyNextAt||0)>t)throw new ApiError("daily_wait",{retry:Math.ceil((v.dailyNextAt-t)/1000)});const streak=(v.lastDailyAt&&t-v.lastDailyAt>48*3600000)?0:(v.streak||0),reward=s.daily_rewards[streak%s.daily_rewards.length],balance=(v.balanceGr||0)+reward;tx.update(userRef,{streak:streak+1,lastDailyAt:t,dailyNextAt:t+DAY,balanceGr:balance});tx.set(db.collection("ledger").doc(),{userId:uid,kind:"daily",grDelta:reward,grAfter:balance,createdAt:t});const out={gr:reward,day:streak+1,next:t+DAY,balance};tx.create(idem,{response:out,createdAt:t});return out;});
  }
  if(name==="redeem"){
    if(!s.features.promo)throw new ApiError("feature_off");const code=clean(p.code,24).toUpperCase();if(!/^[A-Z0-9_-]{3,24}$/.test(code))throw new ApiError("invalid_code");
    const idem=db.collection("idempotency").doc(uid+"_redeem_"+clean(p.key,80)),pr=db.collection("promoCodes").doc(code),red=db.collection("promoRedemptions").doc(code+"_"+uid);
    return db.runTransaction(async tx=>{const [ir,ur,ps,rr]=await Promise.all([tx.get(idem),tx.get(userRef),tx.get(pr),tx.get(red)]);if(ir.exists)return ir.data().response;if(!ps.exists||!ps.data().active)throw new ApiError("invalid_code");const promo=ps.data();if(promo.expiresAt&&promo.expiresAt<t)throw new ApiError("code_expired");if((ur.data().playsTotal||0)<(promo.minPlays||0))throw new ApiError("need_plays",{need:promo.minPlays});if(rr.exists)throw new ApiError("code_already_redeemed");if(promo.maxUses>0&&(promo.usedCount||0)>=promo.maxUses)throw new ApiError("code_used");const gr=promo.rewardGr,balance=(ur.data().balanceGr||0)+gr;tx.update(pr,{usedCount:(promo.usedCount||0)+1});tx.update(userRef,{balanceGr:balance});tx.create(red,{userId:uid,code,gr,redeemedAt:t});tx.set(db.collection("ledger").doc(),{userId:uid,kind:"promo",grDelta:gr,grAfter:balance,createdAt:t});const out={gr,balance};tx.create(idem,{response:out,createdAt:t});return out;});
  }
  if(name==="withdraw"){
    if(!s.features.withdraw)throw new ApiError("feature_off");const gr=num(p.gr,1),contact=clean(p.contact,120);if(!gr||contact.length<3)throw new ApiError("invalid_contact");if(gr<s.min_withdraw_gr)throw new ApiError("min_withdraw",{min:s.min_withdraw_gr});if((u.playsTotal||0)<s.withdraw_min_plays)throw new ApiError("need_plays",{need:s.withdraw_min_plays});
    const idem=db.collection("idempotency").doc(uid+"_withdraw_"+clean(p.key,80)),wref=db.collection("withdrawals").doc();
    return db.runTransaction(async tx=>{const [ir,ur,pending]=await Promise.all([tx.get(idem),tx.get(userRef),tx.get(db.collection("withdrawals").where("userId","==",uid).where("status","==","pending"))]);if(ir.exists)return ir.data().response;if(!pending.empty)throw new ApiError("pending_exists");const v=ur.data();if((v.balanceGr||0)<gr)throw new ApiError("insufficient");const balance=v.balanceGr-gr;tx.update(userRef,{balanceGr:balance});tx.create(wref,{userId:uid,gr,contact,status:"pending",createdAt:t});tx.set(db.collection("ledger").doc(),{userId:uid,kind:"withdraw",grDelta:-gr,grAfter:balance,createdAt:t,meta:{withdrawalId:wref.id}});const out={id:wref.id,gr,balance};tx.create(idem,{response:out,createdAt:t});return out;});
  }
  if(name==="gameStart"){
    if(!s.features.game)throw new ApiError("feature_off");const tier=clean(p.tier,1);if(!["k","n","z"].includes(tier))throw new ApiError("invalid_tier");const key=clean(p.key,80),idem=db.collection("idempotency").doc(uid+"_gameStart_"+key),play=db.collection("gamePlays").doc();
    return db.runTransaction(async tx=>{const [ir,ur,tr]=await Promise.all([tx.get(idem),tx.get(userRef),tx.get(db.collection("gameTiers").doc(tier))]);if(ir.exists)return ir.data().response;if(!tr.exists||!tr.data().active)throw new ApiError("invalid_tier");const v=ur.data(),count=v.gameDay===day?v.gameCount||0:0;if(count>=s.game_daily_plays)throw new ApiError("no_plays");tx.update(userRef,{gameDay:day,gameCount:count+1});tx.create(play,{userId:uid,tier,dayBucket:day,status:"started",startedAt:t,score:0,rewardGr:0});const out={play:play.id,left:s.game_daily_plays-count-1};tx.create(idem,{response:out,createdAt:t});return out;});
  }
  if(name==="game"){
    if(!s.features.game)throw new ApiError("feature_off");const playId=clean(p.play,100),score=num(p.score,0,10000000);if(score===null)throw new ApiError("invalid_score");const pr=db.collection("gamePlays").doc(playId);
    return db.runTransaction(async tx=>{const [ps,ur]=await Promise.all([tx.get(pr),tx.get(userRef)]);if(!ps.exists||ps.data().userId!==uid||ps.data().status!=="started")throw new ApiError("invalid_play");const pl=ps.data(),elapsed=t-pl.startedAt;if(elapsed<s.game_min_elapsed_sec*1000||elapsed>s.game_max_elapsed_sec*1000){tx.update(pr,{status:"rejected",flagged:true,finishedAt:t});throw new ApiError("invalid_play");}const tier=(await db.collection("gameTiers").doc(pl.tier).get()).data();const reward=score>tier.maxRawScore?0:Math.min(score,tier.capGr);const balance=(ur.data().balanceGr||0)+reward;tx.update(pr,{status:"finished",score,rewardGr:reward,finishedAt:t});tx.update(userRef,{playsTotal:FieldValue.increment(1),balanceGr:balance});tx.set(db.collection("ledger").doc(),{userId:uid,kind:"game",grDelta:reward,grAfter:balance,createdAt:t});return {gr:reward,balance};});
  }
  if(name==="taskImage"){const id=clean(p.id,100),m=await db.collection("taskMedia").doc(id).get();return {data:m.exists?m.data().data:null};}
  if(name==="task"){
    if(!s.features.tasks)throw new ApiError("feature_off");const id=clean(p.id,100),tr=db.collection("tasks").doc(id),ur=db.collection("userTasks").doc(uid+"_"+id);
    return db.runTransaction(async tx=>{const [ts,us,done]=await Promise.all([tx.get(tr),tx.get(userRef),tx.get(ur)]);if(!ts.exists||!ts.data().active)throw new ApiError("invalid_task");if(done.exists&&done.data().status==="done")throw new ApiError("task_done");const task=ts.data();if(task.verify==="member")throw new ApiError("task_check_unavailable");if(!done.exists){tx.create(ur,{userId:uid,taskId:id,status:"started",startedAt:t});throw new ApiError("task_wait",{retry:task.minDelaySec||10});}const wait=(task.minDelaySec||10)*1000-(t-done.data().startedAt);if(wait>0)throw new ApiError("task_wait",{retry:Math.ceil(wait/1000)});const gr=task.rewardGr,balance=(us.data().balanceGr||0)+gr;tx.update(ur,{status:"done",doneAt:t});tx.update(userRef,{balanceGr:balance});tx.set(db.collection("ledger").doc(),{userId:uid,kind:"task",grDelta:gr,grAfter:balance,createdAt:t});return {gr,balance};});
  }
  if(name.startsWith("admin")){
    requireAdmin(uid);
    if(name==="adminGet"){
      const [users,wds,tasks,promos,ledger]=await Promise.all([db.collection("users").get(),db.collection("withdrawals").where("status","==","pending").limit(50).get(),db.collection("tasks").orderBy("createdAt","desc").limit(100).get(),db.collection("promoCodes").orderBy("createdAt","desc").limit(30).get(),db.collection("ledger").where("grDelta",">",0).get()]);
      return {stats:{users:users.size,active24:users.docs.filter(d=>t-(d.data().lastSeenAt||0)<DAY).length,pendingN:wds.size,pendingSum:wds.docs.reduce((a,d)=>a+d.data().gr,0),issued:ledger.docs.reduce((a,d)=>a+d.data().grDelta,0)},pending:wds.docs.map(d=>({id:d.id,...d.data()})),tasks:tasks.docs.map(d=>({id:d.id,...d.data()})),promos:promos.docs.map(d=>({code:d.id,...d.data()}))};
    }
    if(name==="adminPromo"){
      const code=clean(p.code,24).toUpperCase();if(p.action==="off"){await db.collection("promoCodes").doc(code).update({active:false});await audit(uid,"promo_off",code);return {ok:true};}
      if(p.action!=="create"||!/^[A-Z0-9_-]{3,24}$/.test(code))throw new ApiError("invalid_input");const gr=num(p.gr,1),maxUses=num(p.maxUses,0)||0,hours=num(p.hours,0)||0;if(!gr)throw new ApiError("invalid_input");const ref=db.collection("promoCodes").doc(code);if((await ref.get()).exists)throw new ApiError("code_exists");await ref.create({rewardGr:gr,maxUses,usedCount:0,minPlays:0,expiresAt:hours?t+hours*3600000:0,active:true,createdBy:uid,createdAt:t});await audit(uid,"promo_create",code,{gr,maxUses,hours});return {ok:true,code};
    }
    if(name==="adminTask"){
      const id=clean(p.id,100);if(p.action==="toggle"){await db.collection("tasks").doc(id).update({active:!!p.active});await audit(uid,"task_toggle",id,{active:!!p.active});return {ok:true};}
      if(p.action==="create"){const title=clean(p.title,100),gr=num(p.gr,1),kind=clean(p.kind,20);if(!title||!gr)throw new ApiError("invalid_input");const ref=db.collection("tasks").doc();await ref.create({kind,title,description:clean(p.description,300),rewardGr:gr,url:clean(p.url,500),chatId:clean(p.chatId,100),verify:p.chatId?"member":"click",minDelaySec:num(p.minDelaySec,5,600)||10,sort:t,active:true,createdAt:t});await audit(uid,"task_create",ref.id);return {ok:true,id:ref.id};}
    }
    if(name==="adminTaskImage"){const id=clean(p.id,100);if(p.data===null){await db.collection("taskMedia").doc(id).delete();return {ok:true};}const data=String(p.data||"");if(data.length>180000||!/^data:image\/(png|jpeg|webp);base64,/.test(data))throw new ApiError("invalid_image");await db.collection("taskMedia").doc(id).set({data,updatedAt:t});return {ok:true};}
    if(name==="adminWd"){const id=clean(p.id,100),wr=db.collection("withdrawals").doc(id);return db.runTransaction(async tx=>{const ws=await tx.get(wr);if(!ws.exists||ws.data().status!=="pending")throw new ApiError("invalid_withdrawal");const w=ws.data(),target=db.collection("users").doc(w.userId),tu=await tx.get(target);if(p.action==="reject"){const balance=(tu.data().balanceGr||0)+w.gr;tx.update(target,{balanceGr:balance});tx.set(db.collection("ledger").doc(),{userId:w.userId,kind:"withdraw_refund",grDelta:w.gr,grAfter:balance,createdAt:t});tx.update(wr,{status:"rejected",note:clean(p.note,200),processedAt:t,processedBy:uid});}else if(p.action==="paid"){tx.update(wr,{status:"paid",note:clean(p.note,200),processedAt:t,processedBy:uid});tx.update(target,{totalWithdrawnGr:FieldValue.increment(w.gr)});}else throw new ApiError("invalid_input");return {ok:true};});}
  }
  throw new ApiError("rpc_not_migrated",{rpc:name});
}

exports.api=onRequest({region:"us-central1",secrets:[BOT_TOKEN],maxInstances:20,timeoutSeconds:30},async(req,res)=>{
  const origin=req.get("origin");if(origin&&allowedOrigin(origin)){res.set("Access-Control-Allow-Origin",origin);res.set("Vary","Origin");res.set("Access-Control-Allow-Headers","Content-Type, X-Telegram-Init-Data");res.set("Access-Control-Allow-Methods","POST, OPTIONS");}
  if(req.method==="OPTIONS")return res.status(204).send("");if(req.method==="GET"&&req.path==="/health")return send(res,200,{ok:true,service:"paidmx-api",project:"paidmx"});
  if(req.method!=="POST")return send(res,405,{ok:false,error:"method_not_allowed"});if(origin&&!allowedOrigin(origin))return send(res,403,{ok:false,error:"origin_not_allowed"});
  try{const tg=verifyTelegramInitData(req.get("X-Telegram-Init-Data")||req.body?.initData,BOT_TOKEN.value());const user=await touchUser(tg);await ensureSeed();const result=await rpc(String(req.body?.rpc||""),req.body?.payload&&typeof req.body.payload==="object"?req.body.payload:{},user);return send(res,200,result);}
  catch(e){const code=e.code||e.message||"internal_error",status=code.startsWith("telegram_")?401:code==="forbidden"?403:code==="rpc_not_migrated"?501:code==="internal_error"?500:400;console.error("PaidMX API:",code);return send(res,status,{ok:false,error:code,params:e.extra||{}});}
});
