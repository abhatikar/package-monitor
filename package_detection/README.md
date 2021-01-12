# Package Monitor and Detection App
This app is designed to let you use your own custom package detection model to detect when packages arrive and when they are removed You'll need an alwaysAI account and to have alwayAI installed:

- [alwaysAI account](https://alwaysai.co/auth?register=true)
- [alwaysAI CLI tools](https://dashboard.alwaysai.co/docs/getting_started/development_computer_setup.html)

## Requirements
This app is intended to work on a model you've trained yourself! Follow the steps below before running your app. The alwaysAI support team is available on Discord to help you if you get stuck: https://discord.gg/rjDdRPT.

### Collect a Dataset
To get you up and running, we've prepared a [dataset](https://www.alwaysai.co/docs/_static/beta/Packages.zip) that includes a few hundred images of packages being placed and removed from an outdoor doorstep. This app will work best using a model that has been trained on your own doorstep (or wherever you intend to run your app), so we encourage you to add to this dataset. See [this doc](https://alwaysai.co/docs/model_training/data_collection.html#data-capture-guidelines) for data collection tips). For speedy data collection, you can use this [image capture app](https://github.com/alwaysai/expanded-image-capture-dashboard) available on the alwaysAI GitHub. Also checkout the [hacky hour](https://www.youtube.com/watch?v=jNpxVea8F9Q&feature=youtu.be) on the package dataset collection for tips on how to set up your own data collection process.

### Annotate your Data
Then you can annotate your data, using [this guide](https://alwaysai.co/docs/model_training/data_annotation.html).

### Dataset

The images catpured and annotated look like these. These are the pictures of the package at the doorstep at varied angles and lighting conditions.

<img src="https://github.com/abhatikar/package-monitor/raw/main/assets/data1.png" width="600" height="600">

<img src="https://github.com/abhatikar/package-monitor/raw/main/assets/data2.png" width="600" height="600">


### Train your Model
 Then, follow the [training section](https://alwaysai.co/docs/model_training/quickstart.html#step-3-train-your-model) of our quickstart guide to train your own model. You'll find links to tips for data collection and annotation on that page as well. To see how to use your model in an application, refer to the [Model Publish](#model-publish) section.

### Set up your Project
Clone this repo into a local directory. Then cd into new folder and run `aai app configure` and make the following selections:
- When prompted to choose a project, use the down arrow and select `Create new project`, choosing any name you like.
- Choose to run either locally or on an edge device.

The `app.py` and `alwaysai.app.json` files should be automatically detected and you should not need to create them.

You can find details on working with projects [here](https://alwaysai.co/docs/getting_started/working_with_projects.html).


## Model Conversion

![alt text](https://github.com/abhatikar/package-monitor/raw/main/assets/convert.png "Model Conversion")

If you want to run this app using an OpenNCC camera, you will have to convert the model you have trained into the format that makes it optimized to run on the OpenNCC camera. The conversion uses the OpenVino toolkit to achieve this. That way you could use the camera with a embedded microcomputer like raspberry pi without compromising the speed of the model inferences. To convert your model to the EyeCloud optimized format, run:

```bash
aai model convert <input-model-id> --format eyecloud --output_id <output-model-id>
```

Here the `input model id` is the full id, including your usename; this is what is output at the end of a training session and has a format of `<username/model-name>`. The `output model id` is just the name you want to give the converted model, do not include your username in this.
e.g if `abhatikar/package_detector` is the model name that is trained locally, and the output model id is `package_detector_eyecloud`, so the command to convert the model to eyecloud camera format would be:

```bash
aai model convert abhatikar/package_detector --format eyecloud --output_id package_detector_eyecloud
```

You can then publish the converted model into the alwaysai platform to use them in your projects.

## Publish Your Model
You can either publish your model and add it to your project using aai app models add, or test out an unpublished version using the --local-version flag with this command. See [this documentation](https://alwaysai.co/docs/model_training/using_your_model.html) for full details.

Refer to the AlwaysAI docs to know how you can achieve this using the CLI.

## Running
You can run the application in 6 different ways.

#### <b>Use a laptop with the USB webcam</b>

Connect your Web camera to your laptop's USB port. Replace the models in `app.py` with the name of your own model or leave it as default!
Next, you copy the Dockerfile template for alwaysai.

Run the project as you would any alwaysAI app! See [our docs pages](https://alwaysai.co/blog/building-and-deploying-apps-on-alwaysai) if you need help running your program.

```bash
cp Dockerfile.alwaysai Dockerfile
aai app configure
aai app install
aai app start
```
This will run the app without any acceleration and you will see the inference time is higher

#### <b>Use a laptop with the USB webcam and NCS2 stick</b>

Connect your webcam camera to your laptop's USB port.Connect the NCS2 stick to the laptop's USB 3.0 port. Replace the models in `app.py` with the name of your own model or leave it as default! 
Next, you copy the Dockerfile template for alwaysai.

Run the project as you would any alwaysAI app! See [our docs pages](https://alwaysai.co/blog/building-and-deploying-apps-on-alwaysai) if you need help running your program.

```bash
export NCS2_CAM=1
cp Dockerfile.alwaysai Dockerfile
aai app configure
aai app install
aai app start
```

#### <b>Use a laptop with the OpenNCC camera</b>

Connect your OpenNCC camera to your laptop's USB 3.0 port. Replace the models in `app.py` with the name of your own model which you converted 
or leave it as default! 
Next, you copy the Dockerfile template for alwaysai.

Run the project as you would any alwaysAI app! See [our docs pages](https://alwaysai.co/blog/building-and-deploying-apps-on-alwaysai) if you need help running your program.

```bash
export OpenNCC=1
cp Dockerfile.alwaysai Dockerfile
aai app configure
aai app install
aai app start
```

#### <b>Use a Raspberry Pi4 with the USB webcam</b>
<p>

Connect your webcam to the Raspberry Pi4 USB 3.0 port. Replace the models in `app.py` with the name of your own model or leave it as default! 
Follow the [guide](https://www.balena.io/docs/learn/getting-started/raspberrypi4-64/python/) to setup the Raspberry Pi4 to work with Balena platform.
Next, you copy the Dockerfile template for Balena and run the balena cli commands as shown below from the top level directory

```bash
cp Dockerfile.balena Dockerfile
cd <directory which has docker-compose.yml>
balena push <app name>
```

#### <b>Use a Raspberry Pi4 with the USB webcam and NCS2 stick</b>
<p>

<u><b>*Architecture*</b></u>

![alt text](https://github.com/abhatikar/package-monitor/raw/main/assets/arch.png "Architecture")


<u><b>*Setup*</b></u>

<img src="https://github.com/abhatikar/package-monitor/raw/main/assets/setup.jpg" width="600" height="600">

Connect your webcam and the NCS2 stick to the Raspberry Pi4 USB 3.0 port. Replace the model in `app.py` with the name of your own model or leave it as default! 
Follow the [guide](https://www.balena.io/docs/learn/getting-started/raspberrypi4-64/python/) to setup the Raspberry Pi4 to work with Balena platform.
Next, you copy the Dockerfile template for Balena and run the balena cli commands as shown below from the top level directory
Uncomment the line to enable the NCS2 with USB webcam in the `docker-compose.yaml`

`#- NCS2_CAM=1  #Enable this if you have NCS stick plugged in`

```bash
cp Dockerfile.balena Dockerfile
cd <directory which has docker-compose.yml>
balena push <app name>
```

#### <b>Use a Raspberry Pi4 with the OpenNCC camera</b>
<p>

<u><b>*Architecture*</b></u>

![alt text](https://github.com/abhatikar/package-monitor/raw/main/assets/arch.png "Architecture")


<u><b>*Setup*</b></u>

<img src="https://github.com/abhatikar/package-monitor/raw/main/assets/setup.jpg" width="600" height="600">

Connect your OpenNCC camera to the Raspberry Pi4 USB 3.0 port. Replace the models in `app.py` with the name of your own model which you converted! 
Follow the [guide](https://www.balena.io/docs/learn/getting-started/raspberrypi4-64/python/) to setup the Raspberry Pi4 to work with Balena platform.
Next, you copy the Dockerfile template for Balena and run the balena cli commands as shown below from the top level directory
Uncomment the line to enable the NCS2 with USB webcam in the `docker-compose.yaml`

`# - OPENNCC_CAM=1 #Enable this if you have an EyeCloud camera`

```bash
cp Dockerfile.balena Dockerfile
cd <directory which has docker-compose.yml>
balena push <app name>
```

Here is the [link](https://www.youtube.com/watch?v=fk3arnsZ45Q) to the demo video.

Note: If you use the OpenNCC IPC camera, it has Raspberry Pi 4 built-in which makes it an edge device in itself and you would not require a external micro computer.

#### Mobile App

To get the notification on your mobile phone, download this [app](https://play.google.com/store/apps/details?id=com.app.vetru.mqttdashboard&hl=en_IE&gl=US) on your Android Phone.

Configure the broker to point to the MQTT broker of your choice. I am using a public broker which should be only used for <b>testing purposes</b> only.

Create a Text widget to subscribe to the topic matching in the file package_monitor.py. In our code we are using the MQTT topic <b><i>alwaysai/package-alert</b></i>. I strongly recommend to use a private broker and unique MQTT topic if you are using a public broker for testing.

#### Example Output

```bash
/open_ncc_lib/moviUsbBoot /open_ncc_lib/flicRefApp.mvcmd
Performing bulk write of 8168336 bytes from /open_ncc_lib/flicRefApp.mvcmd...
Successfully sent 8168336 bytes of data in 322.738822 ms (24.136954 MB/s)
device opened
03E7:F63B (usbver:32, bus 2, device 2)get our self usb device ver:32
 path: 6
outEndPoint:[1]
inEndPoint:[81]
outEndPoint:[2]
inEndPoint:[82]
outEndPoint:[3]
inEndPoint:[83]

1D6B:0003 (usbver:30, bus 2, device 1)
1532:0224 (usbver:20, bus 1, device 4) path: 8

0BDA:579F (usbver:20, bus 1, device 3) path: 7
inEndPoint:[81]

0CF3:E300 (usbver:20, bus 1, device 2) path: 4
inEndPoint:[82]
outEndPoint:[2]

1D6B:0002 (usbver:20, bus 1, device 1)
22:18:43 : sdk/sdk.cpp(534) enter watchdog task.....
camera_video_out YUV420p 2
22:18:43 : sdk/sdk.cpp(1230) meanValue: 0.00 0.00 0.00
22:18:43 : sdk/sdk.cpp(889) initstatus ret:0 
--------------------------------------------
Camera detection succeeded!(sc8238)


22:18:43 : sdk/sdk.cpp(900) CAM_AI_MODE
22:18:43 : sdk/sdk.cpp(507) Reading Blob file: /app/models/abhatikar/package_detector_ncc/package_detector_ncc.blob (sz 13937728)

22:18:43 : sdk/sdk.cpp(524) Blob size 13937728 has been sent  return 0 meta size=1408

22:18:43 : sdk/sdk.cpp(970) send blob ret =0  
********Setup Caminfo size =68**********
size   :1920  X 1080 
ai area:(0,0,1920,1080)
ai input: 300 X 300 
meanValue:0.00-0.00-0.00 stdValue:0
Enable Output: YUV=1  H26x=0 MJpeg=0 Encoder type:0
********Setup Caminfo**********
send CameraInfo ret=0 
22:18:43 : sdk/sdk.cpp(991) create queue yuv:0xd48c55c0 26x:0xd4c0a3e0 jpg:0xd4924d70 cnn:0xd4924e00 
initstatus 
--------------------------------------------
Camera detection succeeded!(sc8238)
Device initialized OK!
--------------------------------------------
 
create thread ep 0 success!
create thread ep 1 success!
22:18:43 : sdk/sdk.cpp(258) enter scReadThread ep 0 ******

create thread ep 2 success!
22:18:43 : sdk/sdk.cpp(258) enter scReadThread ep 1 ******

22:18:43 : sdk/sdk.cpp(258) enter scReadThread ep 2 ******

[INFO] Streamer started at http://localhost:5000
22:18:43 : sdk/sdk.cpp(338) EP:0 Meta type:2,seqNo:10, len:3110400 usb_size=3110464

22:18:43 : sdk/sdk.cpp(338) EP:1 Meta type:24,seqNo:10, len:1472 usb_size=1536

```

## Troubleshooting
Docs: https://dashboard.alwaysai.co/docs/getting_started/introduction.html

Community Discord: https://discord.gg/rjDdRPT
