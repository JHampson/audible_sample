import audible
import os.path
import json
import os


def main():
    auth_file = 'audible.auth'
    if os.path.isfile(auth_file):
        auth = audible.FileAuthenticator(auth_file)
    else:
        auth = audible.LoginAuthenticator(
            os.getenv('AUDIBLE_USERNAME'),
            os.getenv('AUDIBLE_PASSWORD'),
            locale='uk',
            register=True)
        auth.to_file(auth_file)

    client = audible.Client(auth)

    # library = client.get("1.0/library")
    # print(library)
    # for book in library["items"]:
    #     print(book)
    country_codes = ["de", "us", "ca", "uk", "au", "fr", "jp", "it", "in"]

    for country in country_codes:
        client.switch_marketplace(country)
        library = client.get("library", num_results=1000, response_groups="media, price")
        asins = [book["asin"] for book in library["items"]]
        print(f"Country: {client.marketplace.upper()} | Number of books: {len(asins)}")
        print(34 * "-")

        with open(f'library_{country}.json', 'w') as fp:
            json.dump(library, fp)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
