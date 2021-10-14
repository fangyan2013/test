from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to http://www.baidu.com/
    page.goto("http://www.baidu.com/")

    # Click input[name="wd"]
    page.click("input[name=\"wd\"]")

    # Fill input[name="wd"]
    page.fill("input[name=\"wd\"]", "ces")

    # Click input[name="wd"]
    page.click("input[name=\"wd\"]")

    # Fill input[name="wd"]
    page.fill("input[name=\"wd\"]", "测试")

    # Click text=百度一下
    # with page.expect_navigation(url="http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E6%B5%8B%E8%AF%95&fenlei=256&rsv_pq=96ebac880000634d&rsv_t=a74fUMNB8VSve8wzwgauZANPn60AbX5bKry%2Fa2jM7fGdvUP9R5cSz2ePohU&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_sug3=11&rsv_sug1=3&rsv_sug7=100&rsv_btype=i&inputT=5363&rsv_sug4=6093&rsv_jmp=fail"):
    with page.expect_navigation():
        page.click("text=百度一下")
    # assert page.url == "http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E6%B5%8B%E8%AF%95&fenlei=256&rsv_pq=96ebac880000634d&rsv_t=a74fUMNB8VSve8wzwgauZANPn60AbX5bKry%2Fa2jM7fGdvUP9R5cSz2ePohU&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_sug3=11&rsv_sug1=3&rsv_sug7=100&rsv_btype=i&inputT=5363&rsv_sug4=6093"

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
