"""Enhanced FruitClaim Bot - FaucetPay Email + Password Login
Version 2.0 - 5-10x Improved with error handling, stats tracking, and better UI
"""
import json
import os
import shutil
import time
import sys
from datetime import datetime
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Color codes
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
BOLD = "\033[1m"

# API URLs (fixed - removed extra spaces)
LOGIN_URL = "https://slotfruits.com/api/v1/users/signupFaucetPayLogin"
SPIN_URL = "https://slotfruits.com/api/v1/users/earnRoll"
ADS_URL_BASE = (
    "https://googleads.g.doubleclick.net/mads/gma?submodel=SM-A217F"
    "&adid_p=1&format=interstitial_mb"
    "&ini_pn=com.google.android.packageinstaller"
    "&ins_pn=com.google.android.packageinstaller"
    "&omid_v=a.1.5.2-google_20241009"
    "&dv=254380203&ev=24.6.0&gl=ID&hl=in"
    "&js=afma-sdk-a-v254380999.253410000.1"
    "&kw=clothing%2Cfashion&lv=253410000"
    "&ms=CqgFmsA_ATEaQQHY5dWIJ1nnZI0TXJOCrRjxy3oie3ZsfYBDue5jJF2CTFQQuf7W9C9KnP8xbLx0FI_PC-5wIrw0itcrK2KvDP4iEt0E6Yp1pn72NO8vWhbzh19JnXz5v7gGWsohjScUvkVohNO_jbecHUPYSmq4yT-WuJZ2EFv8_r-2HeMQg4ZPiq_jwKyeOrQjsiRXsU8vcZpKSMI0Z7Pn6iha94ABhZW_FbLysDgYt2ox4f_FIffLSbr_vjYntwKQpTg44MpacMRJ2_Ch0aplBuEzXYGkOTHBpg58oZtEw_3nZ8wsO9jE5lLVvx_cmKmOEpfemdesE_wTXvV0Hv5MWrZQ2I4ulXfQrY_gKRBI5ivJJLh3XYIzgBBRhoZastP7yEVFBT7Y8iunIsK3VrABvtw9RWUDkE2lETA0ezNEzwFoAhoGTGHuS2JaZ68x68KZGPFPR1CX4CXbMf1DDtzECiUr12lOsiuPUQ2WWtrjma3PKtkBk-0B5HoTVviRRPOHqgth3x80sbtwMn4G95El7JP079-e_jUT0oa75oJQC-Ph3zmllppvqq3dJN_RCGbyELdXc042fsR1fi3Syd6w1SJROO_t2sP3o2Bdzn2_jv1aokWO8NAzbtrWUs64BUiv1-XMv3k6CReZ91Ac9T28vbfulD8b_t8WSPrIHmXCGEC4h50U74SHhRxUcOmlR7sWpB2y8WfC7NlfoGCG5r6vXzVpG1oFOvTYscbEq1GPl1SjpnwS00RVM5_wfwa6GKc53oRubkV-CBhU_KMXUN115FELhAaNab2qn8reOKeN6xdg_OkZjGgHml1GIlVQity3vBcbzP2yE898LCwcwXVc9oLcH_WHL1eb7K19Z6f5kpquk35qGtTP3xrSzDcw6t-GAxGg1lTCxlMgBA"
    "&mv=84923430.com.android.vending&lft=1&vnm=1.1.6&plbs=0&plcs=0"
    "&u_sd=1.75&request_id=1267448703&target_api=35&carrier=51011"
    "&request_agent=rn-invertase-15.8.0&seq_num=2"
    "&eid=318500618,318486317,318491267,318503826,318509511,318509849,318515546,318518927,318527162,318482080,318483611,318484497,318484801,318525018,318526145,318526848"
    "&guci=0.0.0.0.0.0.0.0&sdk_apis=7%2C8"
    "&omid_p=Google%2Fafma-sdk-a-v260480999.253410000.1&cap=m"
    "&u_w=412&u_h=828&msid=com.piratebaixe.slotMobile"
    "&an=17.android.com.spincoin.appmobile.top&u_audio=3&net=ed&u_so=p&rbv=1"
    "&loeid=44766145%2C318502926&preqs_in_session=1&preqs=1&time_in_session=70&pcc=0"
    "&sst=1766181420000&output=html&region=mobile_app&u_tz=420"
    "&client=ca-app-pub-5674874137587223&slotname=7114498212&kw_type=broad&gsb=4g&lite=0"
    "&app_wp_code=ca-app-pub-5674874137587223&app_code=5186053460&num_ads=1"
    "&vpt=8&vfmt=18&vst=0&sdkv=o.254380999.253410000.1&sdmax=0&dmax=1&sdki=3c4d"
    "&stbg=1&bisch=true&blev=0.16&canm=true&_mv=84923430.com.android.vending"
    "&heap_free=35837248&heap_max=268435456&heap_total=67108864&wv_count=0&rdps=5500"
    "&caps=inlineVideo_interactiveVideo_mraid1_mraid2_mraid3_sdkVideo_exo3_th_autoplay_mediation_scroll_av_transparentBackground_sdkAdmobApiForAds_di_aso_sfv_dinm_dim_nav_navc_dinmo_ipd_of_gls_gcache_saiMacro_sai_demuxedGcache_xSeconds"
    "&is_lat=false"
    "&blob=ABPQqLFPLHz2k6c8n6CqX1sW26j7BjCjFG5-MaUl0CxgLB41Sc1B8kpJWaikL2C_Gp9pl25Xd46LPjDMkuzcNeNk1dvygLdxMwK-Y6rlwJbBvC5njmNuysN-8h288vPObPEuoucf6F2FyhorQbQv9YbRKuFGXNMnm3mLs9x1FneK3ofa6gCK_UTEhPBLeTogM4C8tHMwO2a7T816OsKSD0JYRvo61pYUj8Rx-RsJMnAhHhTzRs3ktQdg-BbwRWiEaPEswxrDeM_GpknK8GoDLzwQ_wuTxQDlAIhl0WIPz9VciYotTXJ86Pe3o5uMwqNeQhZ_qFNQWL_Rncwnb9idfxUEGM5ucxxK_zjofg8F"
    "&jsv=sdk_20190107_RC02-production-sdk_20251202_RC00"
)


def clear_screen():
    """Clear screen"""
    os.system("cls" if os.name == "nt" else "clear")


def terminal_width():
    """Get terminal width"""
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80


def make_line(char="═"):
    """Create line"""
    return char * terminal_width()


def center_text(text):
    """Center text"""
    width = terminal_width()
    return text.center(width)


def print_banner():
    """Print banner"""
    now = datetime.now()
    clear_screen()
    print(CYAN + make_line("═"))
    print(center_text("🚀 SLOT MOBILE SYNDICATE BOT v2.0 🚀"))
    print(CYAN + make_line("═"))
    print(f"{MAGENTA}Creator           : {RESET}AlperenThe")
    print(f"{MAGENTA}Version           : {RESET}2.0 Enhanced")
    print(f"{MAGENTA}Time              : {RESET}{now.strftime('%H:%M:%S')}")
    print(CYAN + make_line("═"))


def animate_status(text, duration=1.2):
    """Animated status message"""
    for i in range(3):
        dots = "." * ((i % 3) + 1)
        print(f"\r{YELLOW}{text}{dots}{RESET}", end="", flush=True)
        time.sleep(duration / 3)
    print()


def print_account_info(email, balance, credits):
    """Print account info"""
    print()
    print(f"{GREEN}{'='*50}{RESET}")
    print(f"{GREEN}📧 Email           : {RESET}{email}")
    print(f"{GREEN}💰 Balance         : {RESET}{balance}")
    print(f"{GREEN}🎰 Spin Available  : {RESET}{credits}")
    print(f"{GREEN}{'='*50}{RESET}")
    print()


def create_session():
    """Create robust session with retry mechanism"""
    session = requests.Session()
    
    # Retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    return session


def login(email, password):
    """Login with FaucetPay email + password"""
    animate_status("🔐 Logging in")
    
    payload = {
        "email": email,
        "password": password
    }
    
    headers = {
        "User-Agent": "okhttp/4.12.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
    }
    
    try:
        session = create_session()
        response = session.post(LOGIN_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        response_json = response.json()
        
        token = response_json.get("token")
        user = response_json.get("user", {})
        
        if not token:
            print(f"{RED}❌ Login failed: No token received{RESET}")
            return None, None, 0, 0
        
        user_id = user.get("_id")
        balance = user.get("balance", 0)
        credits = user.get("credits", 0)
        
        print(f"{GREEN}✅ Login successful!{RESET}")
        return token, user_id, balance, credits
        
    except requests.exceptions.RequestException as e:
        print(f"{RED}❌ Login error: {str(e)}{RESET}")
        return None, None, 0, 0
    except Exception as e:
        print(f"{RED}❌ Unexpected error: {str(e)}{RESET}")
        return None, None, 0, 0


def normalize_credit_count(value):
    """Convert credit value to integer"""
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def run_spin_loop(email, token, balance, credits, max_spins=None):
    """Run spin loop"""
    credits = normalize_credit_count(credits)
    repeated_credit_count = 0
    total_spins = 0
    total_reward = 0
    
    print(f"{CYAN}🎰 Starting spin loop...{RESET}")
    
    while credits > 0:
        # Check max spins
        if max_spins and total_spins >= max_spins:
            print(f"{YELLOW}⚠️ Maximum spins reached ({max_spins}){RESET}")
            break
            
        animate_status("🎰 Spinning")
        
        headers = {
            "User-Agent": "okhttp/4.12.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip",
            "Authorization": f"Bearer {token}",
        }
        
        try:
            session = create_session()
            spin_response = session.get(SPIN_URL, headers=headers, timeout=10).json()
            
            reward = spin_response.get("total", 0)
            user = spin_response.get("user", {})
            balance = user.get("balance", balance)
            new_credits = normalize_credit_count(user.get("credits", credits))
            
            # Check credit change
            if new_credits == credits:
                repeated_credit_count += 1
            else:
                repeated_credit_count = 0
            
            credits = new_credits
            total_spins += 1
            total_reward += reward
            
            # Clear screen and show info
            print_banner()
            print_account_info(email, balance, credits)
            print(f"{YELLOW}🎁 Last Reward     : {RESET}{reward}")
            print(f"{YELLOW}📊 Total Spins     : {RESET}{total_spins}")
            print(f"{YELLOW}💎 Total Reward    : {RESET}{total_reward}")
            print(CYAN + make_line("═"))
            
            # Show API message
            if spin_response.get("message"):
                print(f"{YELLOW}📝 API Message     : {RESET}{spin_response.get('message')}")
            
            # Stop conditions
            if spin_response.get("success") is False or repeated_credit_count >= 2:
                print(f"{YELLOW}⚠️ Spin stopped: Credits not decreasing{RESET}")
                break
                
            time.sleep(1)
            
        except Exception as e:
            print(f"{RED}❌ Spin error: {str(e)}{RESET}")
            time.sleep(2)
            continue
    
    return balance, credits, total_spins, total_reward


def run_ads_loop(user_id, max_ads=3):
    """Run ads watching loop"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; SM-A217F Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/147.0.7727.111 Mobile Safari/537.36",
        "sec-ch-ua-platform": '"Android"',
        "sec-ch-ua": '"Android WebView";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        "sec-ch-ua-mobile": "?1",
        "x-requested-with": "com.piratebaixe.slotMobile",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://googleads.g.doubleclick.net/mads/static/sdk/native/sdk-core-v40.html",
        "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "priority": "u=1, i",
        "Cookie": "IDE=AHWqTUmPTIJAy-Z7wZUR-Si3c3uYRcuBwUfjmr_ffdlWQMrcruxMTVUyL8XPtA-y_Dk",
    }
    
    print(CYAN + make_line("─"))
    print(f"{YELLOW}🚀 Starting Ads Farming...{RESET}")
    
    ads_watched = 0
    
    for i in range(max_ads):
        try:
            session = create_session()
            response = session.get(ADS_URL_BASE, headers=headers, timeout=10)
            
            if "application/json" in response.headers.get("Content-Type", ""):
                data = response.json()
                ad_networks = data.get("ad_networks", [])
                
                if ad_networks:
                    video_reward_urls = ad_networks[0].get("video_reward_urls", [])
                    
                    for video_url in video_reward_urls:
                        parsed_url = urlparse(video_url)
                        query_parameters = parse_qs(parsed_url.query, keep_blank_values=True)
                        query_parameters["rwd_userid"] = [user_id]
                        
                        updated_url = urlunparse(
                            parsed_url._replace(query=urlencode(query_parameters, doseq=True))
                        )
                        
                        reward_response = session.get(updated_url, headers=headers, timeout=10)
                        ads_watched += 1
                        
                        print(f"{GREEN}✔ Ad {ads_watched} watched (Status: {reward_response.status_code}){RESET}")
                        time.sleep(2)
                        
        except Exception as e:
            print(f"{RED}❌ Ad error: {str(e)}{RESET}")
        
        time.sleep(3)
    
    print(f"{GREEN}✅ Ads farming completed: {ads_watched} ads watched{RESET}")
    return ads_watched


def save_stats(email, total_spins, total_reward, ads_watched):
    """Save statistics"""
    stats_file = "bot_stats.json"
    stats = {}
    
    # Load existing stats
    if os.path.exists(stats_file):
        try:
            with open(stats_file, 'r') as f:
                stats = json.load(f)
        except:
            stats = {}
    
    # Add new stats
    if email not in stats:
        stats[email] = {
            "total_spins": 0,
            "total_reward": 0,
            "ads_watched": 0,
            "sessions": 0
        }
    
    stats[email]["total_spins"] += total_spins
    stats[email]["total_reward"] += total_reward
    stats[email]["ads_watched"] += ads_watched
    stats[email]["sessions"] += 1
    stats[email]["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save
    try:
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
        print(f"{GREEN}📊 Stats saved to {stats_file}{RESET}")
    except Exception as e:
        print(f"{RED}❌ Error saving stats: {str(e)}{RESET}")


def main():
    """Main function"""
    print_banner()
    
    # Get user credentials
    print(f"{YELLOW}📧 Enter Your FaucetPay Email: {RESET}", end="")
    email = input().strip()
    
    print(f"{YELLOW}🔑 Enter Your Password: {RESET}", end="")
    password = input().strip()
    
    if not email or not password:
        print(f"{RED}❌ Email and password are required!{RESET}")
        return
    
    # Ask for max spins
    print(f"{YELLOW}🎰 Max spins per cycle (0 for unlimited): {RESET}", end="")
    try:
        max_spins_input = input().strip()
        max_spins = int(max_spins_input) if max_spins_input else None
    except:
        max_spins = None
    
    cycle = 0
    
    while True:
        cycle += 1
        print(f"\n{CYAN}{'='*50}{RESET}")
        print(f"{CYAN}🔄 Cycle #{cycle}{RESET}")
        print(f"{CYAN}{'='*50}{RESET}\n")
        
        # Login
        token, user_id, balance, credits = login(email, password)
        
        if not token:
            print(f"{RED}❌ Login failed. Retrying in 5 seconds...{RESET}")
            time.sleep(5)
            continue
        
        # Show account info
        print_banner()
        print_account_info(email, balance, credits)
        
        # Run spin loop
        balance, credits, total_spins, total_reward = run_spin_loop(
            email, token, balance, credits, max_spins
        )
        
        print(f"{GREEN}✅ Spin cycle completed: {total_spins} spins, {total_reward} reward{RESET}")
        
        # Watch ads
        if user_id:
            ads_watched = run_ads_loop(user_id, max_ads=3)
        else:
            ads_watched = 0
            print(f"{RED}❌ Cannot watch ads: No user ID{RESET}")
        
        # Save stats
        save_stats(email, total_spins, total_reward, ads_watched)
        
        # Wait before next cycle
        print(f"\n{CYAN}⏳ Waiting 10 seconds before next cycle...{RESET}")
        print(f"{YELLOW}Press Ctrl+C to stop{RESET}")
        time.sleep(10)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}🛑 Bot stopped by user{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}❌ Fatal error: {str(e)}{RESET}")
        sys.exit(1)
