from playwright.sync_api import sync_playwright
import os
import time
from bs4 import BeautifulSoup
from fastapi import HTTPException, FastAPI
import json
import uvicorn
import requests
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

@app.get("/")
# Define a function to be executed when the endpoint is called.
def root():
    return {"message": "Guitar Data Collector. Uses a provided facebook marketplace username and password to log in and gather data of guitars near Spokane Washington. Also able to gather data from guitar center"}


# Create a route to the return_data endpoint.
@app.get("/crawl_facebook_marketplace")
# Define a function to be executed when the endpoint is called.
# Add a description to the function.
def access_facebook_marketplace():
		os.makedirs("images", exist_ok=True)

		facebook_market_url = 'https://www.facebook.com/marketplace/spokane/search/?query=guitar&exact=false'
		login_url = "https://www.facebook.com/login/device-based/regular/login/"
		conditions = ['new']

		print("Scraper tool called")
		parsed = []

		with sync_playwright() as p:
			browser = p.chromium.launch(headless=False)
			page = browser.new_page()
			page.goto(login_url)
			time.sleep(2)
			try:
				# login(page)
				page.locator('input[name="email"]').type("j89666944@gmail.com",delay=150)
				time.sleep(2)
				page.wait_for_selector('input[name="pass"]').type("jamesjames4", delay=150)
				time.sleep(2)
				page.wait_for_selector('button[name="login"]').click()
				time.sleep(10)
				print("Login Completed")
			except:
				print("login failed")

			parsed = []

			for condition in conditions:
				facebook_market_condition_url = f'https://www.facebook.com/marketplace/spokane/search?itemCondition={condition}&query=guitar&exact=false'
				print(f"Going to page: {facebook_market_condition_url}")
				page.goto(facebook_market_condition_url)
				time.sleep(2)

				divs = page.locator('div.x9f619.x78zum5.x1r8uery.xdt5ytf.x1iyjqo2.xs83m0k.x1e558r4.x150jy0e.x1iorvi4.xjkvuk6.xnpuxes.x291uyu.x1uepa24')
				count = divs.count()
				print(f"Found {count} divs")
				time.sleep(2)
				for j in range(3): #this now deals with amount of guitars.
					divs.nth(j).click()
					time.sleep(1)
					
					html = page.content()
					soup = BeautifulSoup(html, 'html.parser')
					listing = soup.find('div', class_='x1bwycvy x16xn7b0 x1bifzbx x6ikm8r x10wlt62 xh8yej3 x7pk29f x1dr59a3 xiylbte')
					images = soup.find_all('div',class_='x1rg5ohu x2lah0s xc9qbxq x14qfxbe x1mnrxsn x1w0mnb')

					print(f"Images count: {len(images)}")

					title = listing.find('span', 'x1xlr1w8').text
					print(f"Title: {title}")

					pre_price = listing.find('span', 'xk50ysn').text
					pre_price = pre_price.split('$')
					price = pre_price[1]
					print(f"Price: {price}")

					parsed.append({
							'title': title,
							'price': price,
							'condition' : condition
						})
					
					try:
						os.makedirs(f"images/guitar_{j}", exist_ok=True)
						print(f"Created image directory: \"images/guitar_{j}\"")
					except:
						print("Was not able to create directory \"images/guitar_{j}\"")
		   
					if len(images) == 0:
						img_url = listing.find('img').get('src')
						img_data = requests.get(img_url).content
						with open(f"images/guitar_{j}/image_{0}.jpg", "wb") as img_file:
							img_file.write(img_data)
					else:
						for i, image in enumerate(images):
							try:
								img_url = image.find('img').get('src')
								print(f"Img url: {img_url}")
								img_data = requests.get(img_url).content

								with open(f"images/guitar_{j}/image_{i}.jpg", "wb") as img_file:
									img_file.write(img_data)
							except:
								print("there was no image found")
								pass
						
					page.go_back()
					time.sleep(1)

			browser.close()
			print("Finished scraper tool")
			return parsed
		


@app.get("/crawl_guitar_center")
def crawl_guitar_center(listingGuitars, marketGuitars):
		start_up_url = 'https://www.guitarcenter.com/'
		market_list = []
		for i, listing in enumerate(listingGuitars):
			_model = listing.Model
			print(f"Model passed into gs scraper: {_model}")

			with sync_playwright() as p:
					# Open a new browser page.
					browser = p.chromium.launch(headless=False)
					page = browser.new_page()
					# Navigate to the URL.
					page.goto(start_up_url)
					time.sleep(2)
					page.locator('input[id="header-search-input"]').type(_model)
					time.sleep(1)  
					page.wait_for_selector('button[class="absolute right-0 top-0 w-[56px] h-full flex items-center justify-center cursor-pointer"]').click()
					time.sleep(1)
					current_url = page.url
					current_url += '&filters=condition:New'
					page.goto(current_url)
					time.sleep(2)
					page.mouse.wheel(0,500)

					parsed = []
					html = page.content()

					soup = BeautifulSoup(html, 'html.parser')
					listings = soup.find_all('div', class_='jsx-f0e60c587809418b plp-product-details px-[10px]')
					print(f"Number of listings found: {len(listings)}")
					for list in listings:
							title = list.find('h2','jsx-f0e60c587809418b').text
							print("Title was found")
							price = list.find('span', 'jsx-f0e60c587809418b sale-price font-bold text-[#2d2d2d]').text
							print(f"Title found: {title}, Price found: {price}")
							market_list.append({
									'Model' : _model,
									'Price' : price,
									'Condition' : "new"
							})
							break
							
					time.sleep(3)
					browser.close
		return market_list



if __name__ == "__main__":
    # Run the app.
    uvicorn.run(
        'app:app',
        host='127.0.0.1',
        port=8000
    )
