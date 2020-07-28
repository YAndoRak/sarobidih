import pdfcrowd
import sys
from datetime import datetime


def convert_url_img(url):
    filename1 = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = './tmp/img/{}.png'.format(filename1)
    try:
        client = pdfcrowd.HtmlToImageClient('sarobidih', 'babe7d12fc919f55df5f43f259b914e0')
        client.setOutputFormat('png')
        client.convertUrlToFile(url, path)
    except pdfcrowd.Error as why:
        print('Pdfcrowd Error: {}\n'.format(why))
        raise
    return path

def convert_url_pdf(url):
    filename1 = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = './tmp/pdf/{}.pdf'.format(filename1)
    try:
        # create the API client instance
        client = pdfcrowd.HtmlToPdfClient('sarobidih', 'babe7d12fc919f55df5f43f259b914e0')

        # run the conversion and write the result to a file
        client.convertUrlToFile(url, path)
    except pdfcrowd.Error as why:
        # report the error
        sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))

        # rethrow or handle the exception
        raise
    return path

if __name__ == "__main__":
    filename1 = datetime.now().strftime("%Y%m%d-%H%M%S")
    test = convert_url_pdf('https://www.youtube.com/watch?v=73_DOquGBD4&list=RDDKbfBSrjVHA&index=9')
    print (test)
