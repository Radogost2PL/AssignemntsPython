import requests

from decorator_time_func.decorator import log_time
from download_app import exceptions
from download_app.download import download_file
from download_app.simple_etl import SimpleETL

if __name__ == "__main__":
    URLS = [
        "https://oleksandr-fedoruk.com/sggw/podyplomowe/file",
        "http://oleksandr-fedoruk.com/sggw/podyplomowe/404",
        "http://oleksandr-fedoruk.com/sggw/podyplomowe/403",
    ]

    @log_time
    def process(url, file_name="sample.csv"):
        path = download_file(url, file_name)
        return SimpleETL(path).run()


    def main():
        for url in URLS:
            try:
                values_path, missing_path = process(url)
            except exceptions.NotFoundError as e:
                print("Błąd 404:", e)
            except exceptions.AccessDeniedError as e:
                print("Błąd 403:", e)
            except exceptions.DownloadError as e:
                print("Inny błąd pobierania:", e)
            except exceptions.DataFormatError as e:
                print("Zły format danych:", e)
            except exceptions.ProcessingError as e:
                print("Błąd przetwarzania:", e)
            except requests.RequestException as e:
                print("Błąd sieci lub HTTP:", e)
            else:
                print("Zapisano plik źródłowy z:", values_path, missing_path)
            finally:
                print("Zakończono przetwarzanie:", url)


    if __name__ == "__main__":
        main()

