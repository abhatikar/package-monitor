import time
import edgeiq
import numpy
from package_monitor import PackageMonitor
"""
Monitor an area for packages and people and respond when packages have
been removed from the area.
"""

def main():

    # add a centroid tracker to see if a new package arrives
    centroid_tracker = edgeiq.CentroidTracker(
                                deregister_frames=10, max_distance=50)
    fps = edgeiq.FPS()

    # Variables to limit inference
    counter = 0
    DETECT_RATE = 10

    # Object to monitor the system
    pm = PackageMonitor()

    try:
        with edgeiq.EyeCloud('abhatikar/package_detector_ncc') as camera,\
                 edgeiq.Streamer() as streamer:

            # Allow the camera to warm up
            time.sleep(2.0)

            fps.start()

            # Loop detection
            while True:
                counter += 1

                # Run this loop whenever there's a package detected or every DETECT_RATE frames
                if pm.package_is_detected() or counter % DETECT_RATE == 0:

                    # Read frame from the video stream
                    frame = camera.get_frame()
 
                    package_results = camera.get_model_result(confidence_level=.90)
                    if package_results is not None:

                        # update the package predictions
                        objects = centroid_tracker.update(package_results.predictions)
                        pm.set_packages(objects)

                        # Generate labels to display the face detections on the streamer
                        text = ["Model: {}".format("abhatikar/package_detector_ncc")]
                        text.append(
                                "Inference time: {:1.3f} s".format(package_results.duration))
 
                        predictions = []

                        # update labels for each identified package to print to the screen
                        for (object_id, prediction) in objects.items():
                            new_label = 'Package {}'.format(object_id)
                            prediction.label = new_label
                            text.append(new_label)
                            predictions.append(prediction)

                        # Alter the original frame mark up to show tracking labels
                        frame = edgeiq.markup_image(
                                frame, predictions,
                                show_labels=True, show_confidences=False,
                                line_thickness=3, font_size=1, font_thickness=3)

                        # Do some action based on state
                        text.append(pm.action())

                        # Send the image frame and the predictions to the output stream
                        streamer.send_data(frame, text)

                        fps.update()

                        if streamer.check_exit():
                            break

    finally:
        fps.stop()
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("approx. FPS: {:.2f}".format(fps.compute_fps()))
        print("Program Ending")

if __name__ == "__main__":
    main()
