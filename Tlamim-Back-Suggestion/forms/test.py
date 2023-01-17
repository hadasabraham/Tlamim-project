from forms.FormServer import FormServer


def main():
    server = FormServer()

    form_id = '1K4v6Iyh9MWTu-4i3uYWtblb57wrwJC_hLnzYLk8UKtk'
    responses = server.parse_responses_to_add(form_id=form_id, responses_file_type='xlsx')

    print(responses)


if __name__ == '__main__':
    main()
