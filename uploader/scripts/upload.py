from uploader.cli import get_args_parser
from uploader.uploader import upload


def main():
    parser = get_args_parser()
    args = parser.parse_args()
    link = upload(
        args.server,
        args.token,
        args.filepath,
        args.reponame,
        args.repopath,
        args.fpassword,
        args.fexpiration
    )
    print(link)


if __name__ == "__main__":
    main()
