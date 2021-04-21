from usps import USPSApi, USPSApiError

class PackageChecker:
    def __init__(self, user_id):
        self.usps_api = USPSApi(user_id)
        self.packages = {}

    def register_package(self, package_id):
        self.packages[package_id] = None

    def get_changes(self):
        changes = []
        for id in self.packages.keys():
            new_status = self.get_package_status(id)
            old_status = self.packages[id]
            update = {
				"id": id,
				"changed": False,
			}
            if new_status != old_status:
                update["changed"] = True
                update["now"] = new_status
                update["before"] = old_status
                self.packages[id] = new_status
            changes.append(update)
        return changes

    def get_package_status(self, id):
        try:
            status = self.usps_api.track(id).result
            response = status.get('TrackResponse')
            info = response.get('TrackInfo')
            summary = info.get('TrackSummary')
            return summary
        except USPSApiError as e:
            print("USPSAPIError occurred: {}".format(e))
            return None