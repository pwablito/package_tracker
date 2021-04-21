from package_checker import PackageChecker
import argparse
from email_updater import email_update
import time


def main():
    parser = argparse.ArgumentParser(
        "Tool for checking status updates of USPS packages")
    parser.add_argument("-d", "--delay", type=int,
                        help="Delay between checks (in seconds)", default=5)
    parser.add_argument("-u", "--usps_id", type=str,
                        help="User ID registered with USPS API", required=True)
    parser.add_argument("-p", "--package_ids", nargs="+",
                        type=str, help="Package IDs to check", required=True)
    parser.add_argument("-s", "--smtp_server", type=str,
                        help="SMTP server to send notifications through", required=True)
    parser.add_argument("-f", "--from-address", type=str,
                        help="Email address to send notifications from", required=True)
    parser.add_argument("-t", "--to-address", type=str,
                        help="Email address to send notifications to", required=True)
    args = parser.parse_args()

    checker = PackageChecker(args.usps_id)
    for id in args.package_ids:
        checker.register_package(id)
    while True:
        change_occurred = False
        changes = checker.get_changes()
        for change in changes:
            if change["changed"]:
                change_occurred = True
                print("Package {} updated: {}".format(
                    change["id"], change["now"]["Event"]))
                email_update(
                    "Package {} update".format(change["id"]), change["now"]["Event"], args.from_address, args.to_address, args.smtp_server)
        if not change_occurred:
            print("No updates")
        # Wait until next update time
        time.sleep(args.delay)


if __name__ == "__main__":
    main()
