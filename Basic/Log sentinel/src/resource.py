paths = [
    "/",                                   # homepage – very common
    "/index.html",
    "/about",
    "/contact",
    "/blog",
    "/blog/page/2",
    "/products",
    "/products/widgets",
    "/products/checkout",
    "/login",
    "/logout",
    "/admin",
    "/admin/dashboard",                    # these will trigger 404s on purpose
    "/admin/users",
    "/api/v1/users",
    "/api/v1/orders",
    "/static/css/main.css",
    "/static/js/app.js",
    "/static/images/logo.png",
    "/static/images/hero.jpg",
    "/robots.txt",                         # bots love this
    "/favicon.ico",                        # classic 404 source
    "/wp-login.php",                       # script kiddies trying WordPress
    "/phpmyadmin",
    "/.env",                               # hackers probing
    "/backup.sql",
    "/sitemap.xml",
    "/search?q=python",
    "/search?q=hacking",
    "/user/profile/12345",
    "/profile/67890",
    "/downloads/report-2025.pdf",
    "/old-page-that-no-longer-exists",     # intentional 404 bait
    "/nonexistent-page-xyz",
    "/this-page-was-deleted",
]

path_weights = [
    150,  # "/"
     80,  # "/index.html"
     60,
     50,
     40,
     10,
     70,
     30,
     20,
     45,
      8,   # "/logout" – rare
      3,   # "/admin" – very rare but attackers try
      2,   # "/admin/dashboard" – almost never works → 404 gold
      1,
     25,
     20,
     35,
     40,
     30,
     25,
     60,  # "/robots.txt" – bots hit this constantly
     90,  # "/favicon.ico" – browsers request every visit
      8,   # "/wp-login.php" – bots
      5,
      4,
      3,
     15,
     12,
      8,
     10,
      9,
      5,
      2,   # old broken links → perfect for 404s
      1,
      1,
]

user_agents = [
    # Super common – modern browsers (2025)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",

    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.6; rv:131.0) Gecko/20100101 Firefox/131.0",

    # Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",

    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",

    # Bots & crawlers (these generate tons of 404s)
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36 (compatible; Googlebot/2.1)",
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Slackbot-LinkExpanding 1.0 (+https://api.slack.com/robots)",

    # Scanners & bad bots (almost always 404/403)
    "Mozilla/5.0 (compatible; MJ12bot/v1.4.8; http://mj12bot.com/)",
    "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)",
    "Mozilla/5.0 (compatible; SemrushBot/7~bl; +http://www.semrush.com/bot.html)",
    "Python-urllib/3.11",
    "curl/8.5.0",
    "Wget/1.21.4",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/132.0.0.0 Safari/537.36",
]

us_weights = [
    180, 160, 140, 110, 120,   # normal browsers – very common
    90, 80,
    70,
    60,

    100, 80,                  # Google & Bing bots – hit the site constantly
    70,
    30,
    20,

    25, 20, 18,               # scanners – less common but noisy
    12,
    10,
    8,
    15,
]