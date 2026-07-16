## Start an experiment

Now, you are ready to run an experiment on ARA!

ARA provides a [sandbox](https://arawireless.readthedocs.io/en/latest/ara_technical_manual/sandbox_service.html) where you can test wireless experiments in a controlled lab environment. Each sandbox host from 001 through 025 is connected to two USRP B210 radios, so a reservation for one host gives you access to both radios.

In this "Hello, ARA" experiment, you will reserve one sandbox host, send a wireless signal with one radio, receive it with the other radio, and visualize the received signal power.

### Check resource availability

Before you create a reservation, identify a sandbox host that is available now and for the next few hours.

From the ARA dashboard,

1. In the menu on the left, click "Project > Summary > Overview".
2. Scroll down to the "Sandbox" section.
3. Find a sandbox host that shows "Available" in the "Reservable", "SDR 1", and "SDR 2" columns.

The "Reservable" column indicates whether you can reserve the host right now. The other two columns indicate whether both radios connected to that host are available. Make a note of the host name, e.g. `Sandbox-Host-001`.

Next, check that the host will remain available for the duration of your experiment:

1. In the menu on the left, click "Project > Reservations > Leases".
2. Click "Host Calendar" on the right side of the page.
3. Find the host you selected and confirm that it has no reservation for at least the next few hours.

If the host is reserved soon, return to the Resource Overview and choose another host.

### Create a lease and launch a container

We will use an "orchestration template" to reserve the sandbox host and launch a container on it. 

First, download the [`hello_ara_sandbox.yaml`](resources/hello_ara_sandbox.yaml) template to your computer.

In the ARA dashboard, go to `Project > Orchestration > Stacks` and click "Launch Stack". Upload the template. You will be asked to specify three parameters:

* For the stack name, use `hello-ara-USERNAME`, where `USERNAME` is the first part of your ARA username. For example, use `hello-ara-ffund` if your username is `ffund@nyu.edu`. 
* Specify the three-digit sandbox host number you identified earlier (e.g. `001`).
* Finally, paste in the full contents of your SSH public key.

Then, click "Launch".

> Sometimes, the stack may fail with an error message "Start Date Must Be Later Than Current Date". This can happen when the lease starts at the same minute that you submit the stack. If this happens, you can delete the stack and submit a new one!

When the stack status changes to "Create Complete", it will have created a "container" running on the sandbox host. You'll need its address in order to access it over SSH.

To find the floating IP associated with your container, open `Project > Container > Containers`, find your container (with the selected sandbox host number as part of its name!), and click on it to see an overview of the container details. On the right side, next to "Addresses", it will have an address in the form `10.189.X.Y` (for some `X` and `Y`) labeled as the "floating IP address". Make a note of this address.

> Sometimes, ARA may fail to automatically assign a floating IP to your container. If that happens, you can still assign one yourself! Make a note of the `10.0.4.X` address associated with your container. Then, in the ARA Portal, click on Network > Floating IPs. Click the "Allocate IP to Project" button, then "Allocate IP". Next to the newly added IP, click "Associate", and under "Portal to be Associated", select the `10.0.4.X` address associated with your container.

Then, in your terminal, use the floating IP shown there to connect through the jumpbox:

```
ssh -i ~/.ssh/id_ed25519_ara -J YOUR_USERNAME@jbox.arawireless.org root@FLOATING_IP
```

where you replace `YOUR_USERNAME` with the jumpbox username shown when you uploaded your public key, and replace `FLOATING_IP` with the floating IP from `container_addresses`.

### Verify radio hardware


After you connect to the container, verify that two radios are available:

```
uhd_find_devices
```

The output should list two USRP B210 radio devices. Make a note of the serial number for each device.

### Send a signal from one radio to another

Now we are ready to send a signal from one radio to another! Here is a brief demo of what we will see:

![](images/spectrum.gif)


* First, a live view from the receiver will show no meaningful transmission - just the "noise floor".
* Then, once we start the transmitter, the receiver will show a signal at a 250 kHz offset from the center.
* After we stop the transmitter, the signal will disappear and we will just see noise floor again.

You will need two SSH sessions: one for the transmitter, and one for the receiver. Use the same SSH command in a new terminal window to open a second SSH session.

In the first SSH session, start a receiver. Use the command below, but:

* in place of `DEVICE_0_SERIAL`, substitute the serial number shown in the output of `uhd_find_devices` for the *first* radio
* in place of `FREQUENCY_HZ`, use `3400 + 5 * HOST_NUMBER` followed by `e6`, where `HOST_NUMBER` is the sandbox host number you are using For example, host `002` uses `3410e6` (3410 MHz).

```bash
# runs on sandbox host
/usr/local/lib/uhd/examples/rx_ascii_art_dft \
  --step 10000000 \
  --num-bins 1024 \
  --rate 1e6 \
  --frame-rate 5 \
  --ref-lvl -30 \
  --dyn-rng 50 \
  --gain 70 \
  --ant RX2 \
  --freq FREQUENCY_HZ \
  --args "serial=DEVICE_0_SERIAL" 
```

You will see a live visualization of the received wireless signal power around the frequency you have specified. Leave this running.


In the second SSH session, transmit a wireless signal within that frequency range. Use the command below, but:

* in place of `DEVICE_1_SERIAL`, substitute the serial number shown in the output of `uhd_find_devices` for the *second* radio
* in place of `FREQUENCY_HZ`, use the same frequency you computed previously.

```bash
# runs on sandbox host
/usr/local/lib/uhd/examples/tx_waveforms \
  --wave-type SINE \
  --wave-freq 250000 \
  --rate 1e6 \
  --gain 40 \
  --ant TX/RX \
  --freq FREQUENCY_HZ \
  --args "serial=DEVICE_0_SERIAL" 
```

Once the transmitter starts, the receiver should show a peak near the transmitted 250 kHz offset (i.e. near the right side of the display). 


Press Ctrl+C in both sessions when finished.


## Clean up resources

Your experiment resources should automatically be deleted after two hours, but you can also manually delete anything that is left over:

* Under Project > Orchestration > Stacks, use the drop-down menu at the right side, next to your stack (the one with your name in it!) and "Delete Stack". 

Leave other resources - not associated with your experiment - alone. These belong to other users that are part of the same ARA "project" as you (e.g. your classmates or lab mates).