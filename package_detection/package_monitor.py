from copy import deepcopy
import time
import paho.mqtt.client as mqtt

class PackageMonitor:
    def __init__(self):
        """This class enables a state machine system for package detection.
        """
        self.previous_packages = {}
        self.current_packages = {}
        self.packages_added = []
        self.packages_removed = []
        self.pending = False
        self.timer = time.time()
        self.rois = {}
        self.mqtt_client = mqtt.Client("Package_Monitor")
        self.mqtt_client.connect("broker.hivemq.com")
        self.mqtt_client.loop_start()

    def set_packages(self, objects):
        """Sets previous packages to the current packages and
        sets the current packages to the input objects.

        Args:
            objects (dictionary): the object ID is the key 
        and the ObjectDetectionPrediction as the value.
        """
        self.previous_packages = deepcopy(self.current_packages)
        
        self.current_packages = deepcopy(objects)
        self.check_for_updates()

    def get_count(self):
        """Returns the number of current packages.

        Returns:
            int: Number of items in the current_packages dictionary.
        """
        return len(self.current_packages)

    def get_current_packages(self):
        """Returns current package dictionary.

        Returns:
            dictionary: the object ID is the key 
        and the ObjectDetectionPrediction as the value.
        """
        return self.current_packages

    def action(self):
        """Checks the state of the system. Replace returned
        string with desired action items for customized system.

        Returns:
            string: A string description of the state.
        """
        action = "{}: ".format(time.asctime())
        if self.pending:
            if time.time() - self.timer >= 5:
                # check for old ROIs 
                if not self.check_overlap():
                    # if packages have been removed, send alert
                    action += "Send Alert: packages removed.\n"
                    print(action) #printing this for demo purposes
                    self.mqtt_client.publish("alwaysai/package-alert", "Alert: packages removed")
                else:
                    action += "False alarm, packages are there.\n"
                    print(action) #printing this for demo purposes
                    self.mqtt_client.publish("alwaysai/package-alert", "False alarm: packages are there")
                self.pending = False  
                self.rois = deepcopy(self.current_packages)
            else:
                return action       

        if len(self.packages_removed) > 0:
            self.pending = True
            self.rois = deepcopy(self.previous_packages)
            self.timer = time.time()
            action += "Packages may have been removed\n"
            print(action) #printing this for demo purposes
            self.mqtt_client.publish("alwaysai/package-alert", "Packages may have been removed")

        if len(self.packages_added) > 0:
            action += "More packages have arrived!\n"
            print(action) #printing this for demo purposes
            self.mqtt_client.publish("alwaysai/package-alert", "More packages have arrived!")

        if len(self.packages_removed) == 0 and len(self.packages_added) == 0:
            action += "Nothing new here, waiting for packages. Package count is {}".format(self.get_count())

        return action

    def check_overlap(self):
        """Checks if new predictions match the last non-empty
        bounding boxes sufficiently. Helps avoid false alerts.

        Returns:
            boolean: True if all previous boxes have sufficient current overlap.
        """
        rois = [prediction.box for prediction in self.rois.values()]
        predictions = [prediction.box for prediction in self.current_packages.values()]
        print("roi length {}".format(len(rois)))
        print("predictions length {}".format(len(predictions)))
        for roi in rois:
            match = False
            for pred in predictions:
                if pred.compute_overlap(roi) > 0.9:
                    match = True
            if not match:
                return False

        return True

    def check_for_updates(self):
        """Updates state for new and missing packages.
        """
        self.packages_added = list(self.current_packages.keys() 
                                    - self.previous_packages.keys())
        self.packages_removed = list(self.previous_packages.keys() 
                                    - self.current_packages.keys())
    
    def package_is_detected(self):
        """Gives current count of packages

        Returns:
            int: number of packages detected
        """
        return len(self.current_packages) > 0
