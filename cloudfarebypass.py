import undetected_chromedriver as uc
import json


opts = uc.ChromeOptions()
opts.headless = True
opts.add_argument('--headless')
opts.add_argument("--window-size=1020,900")  

driver = uc.Chrome(options=opts, use_subprocess=True)

driver.get('https://api.tracker.gg/api/v2/for-honor/standard/profile/uplay/matty_webz?')
pre = driver.find_element_by_tag_name("pre").text
data = json.loads(pre)
print(data)
