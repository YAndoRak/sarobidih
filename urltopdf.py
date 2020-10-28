import requests
def convert_url_img(urls):
	url="https://webpagetopdf999.herokuapp.com/api/render?output=screenshot&url="+urls
	response = requests.get(url)
	path = "tmp/render.png"
	with open('tmp/render.png', 'wb') as f:
		f.write(response.content)
	return path

def convert_url_pdf(urls):
	url="https://webpagetopdf999.herokuapp.com/api/render?url="+urls+"&scrollPage=true"
	response = requests.get(url)
	path = "tmp/render.pdf"
	with open('tmp/render.pdf', 'wb') as f:
		f.write(response.content)
	return path