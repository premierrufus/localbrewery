from selenium import webdriver

browser = webdriver.Firefox()


# Ron has heard about a cool new packaging app. He
# checks out the homepage
browser.get('http://localhost:8000')

# He notices the page title and header mention Packaging Events
assert 'Packaging' in browser.title

# He's invited to make a packaging list
# He types "Veridian"

