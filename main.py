import os
import re
import time
import random
import threading
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from kivy.app import App
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView

requests.packages.urllib3.disable_warnings()

DISCORD_API = "https://discord.com/api/v9/experiments"
GENERAL_URL = "https://httpbin.org/ip"
TIMEOUT = 10
THREADS = 50

PROXY_SOURCES = [
    "https://cdn.jsdelivr.net/gh/proxyscrape/free-proxy-list@main/proxies/all/data.txt",
    "https://cdn.jsdelivr.net/gh/proxyscrape/free-proxy-list@main/proxies/protocols/http/data.txt",
    "https://cdn.jsdelivr.net/gh/proxyscrape/free-proxy-list@main/proxies/protocols/https/data.txt",
    "https://cdn.jsdelivr.net/gh/proxyscrape/free-proxy-list@main/proxies/protocols/socks4/data.txt",
    "https://cdn.jsdelivr.net/gh/proxyscrape/free-proxy-list@main/proxies/protocols/socks5/data.txt",
    "https://raw.githubusercontent.com/dinoz0rg/proxy-list/main/scraped_proxies/http.txt",
    "https://raw.githubusercontent.com/dinoz0rg/proxy-list/main/scraped_proxies/socks4.txt",
    "https://raw.githubusercontent.com/dinoz0rg/proxy-list/main/scraped_proxies/socks5.txt",
    "https://raw.githubusercontent.com/dinoz0rg/proxy-list/main/checked_proxies/http.txt",
    "https://raw.githubusercontent.com/dinoz0rg/proxy-list/main/checked_proxies/socks4.txt",
    "https://raw.githubusercontent.com/dinoz0rg/proxy-list/main/checked_proxies/socks5.txt",
    "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt",
    "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/http/data.txt",
    "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks4/data.txt",
    "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks5/data.txt",
    "https://raw.githubusercontent.com/databay-labs/free-proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/databay-labs/free-proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/databay-labs/free-proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/proxy-free/free-proxy-list/main/all.txt",
    "https://raw.githubusercontent.com/proxy-free/free-proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/proxy-free/free-proxy-list/main/https.txt",
    "https://raw.githubusercontent.com/proxy-free/free-proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/proxy-free/free-proxy-list/main/socks5.txt",
    "https://cdn.jsdelivr.net/gh/officialputuid/KangProxy@main/xResults/Proxies.txt",
    "https://cdn.jsdelivr.net/gh/officialputuid/KangProxy@main/xResults/RAW.txt",
    "https://cdn.jsdelivr.net/gh/officialputuid/KangProxy@main/http/http.txt",
    "https://cdn.jsdelivr.net/gh/officialputuid/KangProxy@main/https/https.txt",
    "https://cdn.jsdelivr.net/gh/officialputuid/KangProxy@main/socks4/socks4.txt",
    "https://cdn.jsdelivr.net/gh/officialputuid/KangProxy@main/socks5/socks5.txt",
    "https://raw.githubusercontent.com/komutan234/Proxy-List-Free/main/proxies/http.txt",
    "https://raw.githubusercontent.com/komutan234/Proxy-List-Free/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/komutan234/Proxy-List-Free/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/Thordata/awesome-free-proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/Thordata/awesome-free-proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/Thordata/awesome-free-proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/Thordata/awesome-free-proxy-list/main/all.txt",
    "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/All_proxies.txt",
    "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/http_proxies.txt",
    "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/socks4_proxies.txt",
    "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/socks5_proxies.txt",
    "https://raw.githubusercontent.com/LoneKingCode/free-proxy-db/main/proxies/all.txt",
    "https://raw.githubusercontent.com/LoneKingCode/free-proxy-db/main/proxies/http.txt",
    "https://raw.githubusercontent.com/LoneKingCode/free-proxy-db/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/LoneKingCode/free-proxy-db/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
]

UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
]

IP_PORT_REGEX = re.compile(r"(?:\d{1,3}\.){3}\d{1,3}:\d{2,5}")

# ---------- theme ----------
BG = (0.043, 0.043, 0.071, 1)
CARD = (0.086, 0.086, 0.133, 1)
PURPLE = (0.475, 0.012, 1, 1)
CYAN = (0.012, 0.973, 0.988, 1)
GREEN = (0.267, 1, 0, 1)
MUTED = (0.55, 0.56, 0.6, 1)

Window.clearcolor = BG


# ---------- core logic (same as the desktop script) ----------
def scrape_from_url(url):
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": random.choice(UAS)})
        if r.status_code != 200:
            return set()
        return set(IP_PORT_REGEX.findall(r.text))
    except Exception:
        return set()


def test_proxy(proxy):
    px = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    hdr = {"User-Agent": random.choice(UAS)}
    try:
        r = requests.get(GENERAL_URL, proxies=px, headers=hdr, timeout=TIMEOUT, verify=False)
        if r.status_code != 200:
            return "dead"
    except Exception:
        return "dead"
    try:
        start = time.time()
        r2 = requests.get(DISCORD_API, proxies=px, headers=hdr, timeout=TIMEOUT, verify=False)
        dc = time.time() - start
        if r2.status_code == 200:
            return "slow" if dc > 5 else "working"
        return "blocked"
    except Exception:
        return "blocked"


# ---------- UI widgets ----------
class RoundButton(Button):
    def __init__(self, color, **kw):
        super().__init__(background_normal="", background_down="",
                         background_color=(0, 0, 0, 0), color=(1, 1, 1, 1),
                         bold=True, font_size=dp(16), **kw)
        self.base = color
        with self.canvas.before:
            self._c = Color(*color)
            self._r = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
        self.bind(pos=self._upd, size=self._upd, state=self._state)

    def _upd(self, *a):
        self._r.pos = self.pos
        self._r.size = self.size

    def _state(self, inst, val):
        if val == "down":
            self._c.rgba = (self.base[0] * 0.7, self.base[1] * 0.7, self.base[2] * 0.7, 1)
        else:
            self._c.rgba = self.base


class Card(BoxLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        with self.canvas.before:
            Color(*CARD)
            self._r = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)])
        self.bind(pos=self._upd, size=self._upd)

    def _upd(self, *a):
        self._r.pos = self.pos
        self._r.size = self.size


class AustinProxy(App):
    title = "Austin Proxy"

    def build(self):
        self.busy = False
        self.good = []
        self.counts = {"working": 0, "slow": 0, "blocked": 0, "dead": 0}
        self.log_lines = []

        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))

        head = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(78))
        head.add_widget(Label(text="AUSTIN PROXY", font_size=dp(28), bold=True,
                              color=PURPLE, size_hint_y=None, height=dp(44)))
        head.add_widget(Label(text="True Proxy Scraper & Checker  |  Owned by Aqua Leaks",
                              font_size=dp(12), color=MUTED, size_hint_y=None, height=dp(24)))
        root.add_widget(head)

        self.btn_scrape = RoundButton(PURPLE, text="Scrape Only", size_hint_y=None, height=dp(52))
        self.btn_check = RoundButton((0.1, 0.55, 0.75, 1), text="Check Only (last scraped)",
                                     size_hint_y=None, height=dp(52))
        self.btn_both = RoundButton((0.12, 0.65, 0.2, 1), text="Scrape + Check",
                                    size_hint_y=None, height=dp(52))
        self.btn_scrape.bind(on_release=lambda *_: self.start("scrape"))
        self.btn_check.bind(on_release=lambda *_: self.start("check"))
        self.btn_both.bind(on_release=lambda *_: self.start("both"))
        for b in (self.btn_scrape, self.btn_check, self.btn_both):
            root.add_widget(b)

        stats = Card(orientation="vertical", size_hint_y=None, height=dp(96),
                     padding=dp(12), spacing=dp(6))
        self.status = Label(text="Idle", color=CYAN, font_size=dp(14), size_hint_y=None, height=dp(22))
        self.bar = ProgressBar(max=100, value=0, size_hint_y=None, height=dp(10))
        self.stats_lbl = Label(text="", markup=True, font_size=dp(14))
        self._refresh_stats()
        stats.add_widget(self.status)
        stats.add_widget(self.bar)
        stats.add_widget(self.stats_lbl)
        root.add_widget(stats)

        logcard = Card(orientation="vertical", padding=dp(10))
        sv = ScrollView(do_scroll_x=False)
        self.log = Label(text="", markup=True, font_size=dp(12), size_hint_y=None,
                         halign="left", valign="top", color=(0.85, 0.85, 0.9, 1))
        self.log.bind(width=lambda *_: setattr(self.log, "text_size", (self.log.width, None)))
        self.log.bind(texture_size=lambda *_: setattr(self.log, "height", self.log.texture_size[1]))
        sv.add_widget(self.log)
        self.sv = sv
        logcard.add_widget(sv)
        root.add_widget(logcard)

        self.btn_copy = RoundButton((0.2, 0.2, 0.3, 1), text="Copy working proxies",
                                    size_hint_y=None, height=dp(46))
        self.btn_copy.bind(on_release=self.copy_good)
        root.add_widget(self.btn_copy)
        return root

    # ----- helpers (always called on the UI thread) -----
    def _refresh_stats(self):
        c = self.counts
        self.stats_lbl.text = (
            f"[color=44ff00]Working {c['working']}[/color]   "
            f"[color=fcf803]Slow {c['slow']}[/color]   "
            f"[color=ff9050]Blocked {c['blocked']}[/color]   "
            f"[color=ff5050]Dead {c['dead']}[/color]"
        )

    def add_log(self, text):
        self.log_lines.append(text)
        self.log_lines = self.log_lines[-200:]
        self.log.text = "\n".join(self.log_lines)
        Clock.schedule_once(lambda dt: setattr(self.sv, "scroll_y", 0), 0.05)

    def ui(self, fn, *a):
        Clock.schedule_once(lambda dt: fn(*a), 0)

    def set_busy(self, val):
        self.busy = val
        for b in (self.btn_scrape, self.btn_check, self.btn_both):
            b.disabled = val

    def copy_good(self, *_):
        if self.good:
            Clipboard.copy("\n".join(self.good))
            self.add_log(f"[color=44ff00]Copied {len(self.good)} proxies[/color]")
        else:
            self.add_log("[color=ff5050]No working proxies yet[/color]")

    # ----- work -----
    def start(self, mode):
        if self.busy:
            return
        self.set_busy(True)
        self.counts = {"working": 0, "slow": 0, "blocked": 0, "dead": 0}
        self.good = []
        self._refresh_stats()
        self.bar.value = 0
        threading.Thread(target=self.run, args=(mode,), daemon=True).start()

    def scraped_path(self):
        return os.path.join(self.user_data_dir, "scraped.txt")

    def run(self, mode):
        try:
            proxies = []
            if mode in ("scrape", "both"):
                proxies = self.do_scrape()
                with open(self.scraped_path(), "w") as f:
                    f.write("\n".join(proxies))
                self.ui(self.add_log, f"[color=44ff00]Scraped {len(proxies)} unique proxies[/color]")
            else:
                if os.path.exists(self.scraped_path()):
                    with open(self.scraped_path()) as f:
                        proxies = [l.strip() for l in f if l.strip()]
                if not proxies:
                    self.ui(self.add_log, "[color=ff5050]Nothing scraped yet. Run Scrape first.[/color]")

            if mode in ("check", "both") and proxies:
                self.do_check(proxies)
        finally:
            self.ui(self.status.__setattr__, "text", "Done")
            self.ui(self.set_busy, False)

    def do_scrape(self):
        self.ui(self.status.__setattr__, "text", "Scraping sources...")
        total = len(PROXY_SOURCES)
        found = set()
        done = [0]
        lock = threading.Lock()

        def worker(url):
            res = scrape_from_url(url)
            with lock:
                found.update(res)
                done[0] += 1
                n = done[0]
            self.ui(setattr, self.bar, "value", n / total * 100)
            host = url.split("/")[2]
            self.ui(self.add_log, f"[color=03f8fc]{host[:28]}[/color]  +{len(res)}")

        with ThreadPoolExecutor(max_workers=20) as exe:
            list(exe.map(worker, PROXY_SOURCES))
        return list(found)

    def do_check(self, proxies):
        total = len(proxies)
        done = [0]
        lock = threading.Lock()
        self.ui(setattr, self.bar, "value", 0)
        self.ui(self.status.__setattr__, "text", f"Checking {total} proxies...")

        def one(p):
            st = test_proxy(p)
            with lock:
                done[0] += 1
                self.counts[st] += 1
                if st == "working":
                    self.good.append(p)
                n = done[0]
            if n % 5 == 0 or n == total:
                self.ui(setattr, self.bar, "value", n / total * 100)
                self.ui(self._refresh_stats)
            if st == "working":
                self.ui(self.add_log, f"[color=44ff00][OK][/color] {p}")

        with ThreadPoolExecutor(max_workers=THREADS) as exe:
            list(as_completed([exe.submit(one, p) for p in proxies]))

        if self.good:
            with open(os.path.join(self.user_data_dir, "good.txt"), "w") as f:
                f.write("\n".join(self.good))
        self.ui(self._refresh_stats)
        self.ui(self.add_log, f"[color=44ff00]Finished: {len(self.good)} working[/color]")


if __name__ == "__main__":
    AustinProxy().run()
