# Hello, ARA

ARA is a wireless research platform for experiments involving advanced wireless technologies (such as 5G).

ARA supports experiments in a controlled sandbox environment and in outdoor environments around the Iowa State campus in Ames, Iowa. In this tutorial you will create an account on ARA and run an example experiment in the sandbox. 

In the example experiment, you will send a wireless signal with one radio, receive it with another radio, and visualize the received signal power.


>[!NOTE]
>Before your start: You need to be added to an ARA project by your advisor or instructor! Your advisor or instructor should have already set up a project and added your email address to the list of project users.

## Prepare your workstation 

To use ARA, you'll need to prepare your workstation (the laptop or PC you are going to use for your experiments) with a terminal application.

You will need a terminal application with SSH to connect to your ARA resources. You may use the built-in terminal on Linux or Mac. On Windows, you may use [cmder](https://cmder.app/) or any other terminal application that has an SSH client.

### Generate an SSH key

Next, you must generate SSH keys that you will later add to your ARA profile. You will use these keys when connecting to resources in ARA.

> Note: If you already have an SSH key pair, you can use it with ARA. Locate its public key file, which ends in `.pub`, then skip to the next section. If you do not have an SSH key pair, continue with the rest of this section.

SSH public-key authentication uses a pair of separate keys (i.e., a key pair): one “private” key, which you keep a secret, and the other “public”. A key pair has a special property: any message that is encrypted with your private key can only be decrypted with your public key, and any message that is encrypted with your public key can only be decrypted with your private key. 

This property can be exploited for authenticating login to a remote machine. First, you upload the public key to a special location on the remote machine. Then, when you want to log in to the machine: 

* You use a special argument with your SSH command to let your SSH application know that you are going to use a key, and the location of your private key. If the private key is protected by a passphrase, you may be prompted to enter the passphrase (this is not a password for the remote machine, though).
* The machine you are logging in to will ask your SSH client to “prove” that it owns the (secret) private key that matches an authorized public key. To do this, the machine will send a random message to you.
* Your SSH client will encrypt the random message with the private key and send it back to the remote machine.
* The remote machine will decrypt the message with your public key. If the decrypted message matches the message it sent you, it has “proof” that you are in possession of the private key for that key pair, and will grant you access (without using an account password on the remote machine.)

(Of course, this relies on you keeping your private key a secret.)

We’re going to generate a key pair on our laptop, then upload it to our ARA profile.

Open a terminal, and generate a key named `id_ed25519_ara`:

```
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_ara
```

Follow the prompts to generate and save the key pair. The output should look something like this: 

```
$ ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_ara
Generating public/private ed25519 key pair.
Enter file in which to save the key (/users/ffund01/.ssh/id_ed25519_ara):
Enter passphrase (empty for no passphrase):
Enter same passphrase again: 
Your identification has been saved in /users/ffund01/.ssh/id_ed25519_ara.
Your public key has been saved in /users/ffund01/.ssh/id_ed25519_ara.pub.
The key fingerprint is:
SHA256:0s8rm6p0dy1xLrjTpEc1CemZLFnE1mBvD7ZkexJ1W2Q ffund01@example.com
The key's randomart image is:
+--[ED25519 256]--+
|      .o.        |
|      ..+        |
|     . + .       |
|      o S .      |
|     . +E+ .     |
|      o.=.+      |
|     .+*oB       |
|    .o+X+o       |
|    .+B*o.       |
+----[SHA256]-----+
```

If you use a passphrase, make a note of it somewhere safe! (You don’t have to use a passphrase, though - feel free to leave that empty for no passphrase.)

The command creates two files:

* `~/.ssh/id_ed25519_ara` is your private key. Keep it secret and do not upload it.
* `~/.ssh/id_ed25519_ara.pub` is your public key. You will upload this file to ARA.

You will also need to copy the *contents* of your public key file, which you'll use whenever you start an experiment. Run

```
cat ~/.ssh/id_ed25519_ara.pub
```

and copy the entire output (starting from the string `ssh-ed25519`).

## Log in to ARA

Now that everything is set up on your workstation, it's time to log in to ARA. Open the [ARA Dashboard](https://portal.arawireless.org/). On the login page, choose an authentication method from the "Authenticate using" menu as follows:

![](images/ara-login.png)


1. Choose "Globus Auth", and click "Sign In".
2. On the Globus sign-in page, select your organization under "Use your organizational login", then click "Continue". (If your organization does not appear in the list but your university provides an institutional Google account, find "Log in using less common options" and click the Google icon. When Google asks you to choose an account, select your university-issued account. )
3. Log in with your institutional credentials.

>You must authenticate with an email address issued by your university. For example, an NYU student must use an `nyu.edu` address in order to be able to join an NYU project.

After authentication, Globus will return you to the ARA Dashboard.

![](images/globus-login.png)

> If it is not possible to log in with your institutional email address, your advisor or instructor may have you use Keystone authentication instead. In this case, they will also provide your ARA username *and password*. Select "Keystone Credentials", enter those credentials, and click "Sign In".

### Upload your public key

Next, you will need to upload the public part of your key pair to the ARA Dashboard, so that you will be able to use it to log on to ARA resources!

From the ARA dashboard,

1. Click your email address in the upper-right corner.
2. Select "Upload Public Key".
3. For "Public Key File", choose the public key file `~/.ssh/id_ed25519_ara.pub` from your computer. 
4. Click "Upload Key".

![](images/ara-upload-public-key.png)

The page also shows your ARA jumpbox username and an example SSH command. Your username will differ from the one shown in the screenshot; use the username displayed in your own dashboard.

After you have uploaded a key, test it by connecting to the jumpbox. Run the command shown on the upload page, replacing the example identity filename with *your* ARA private key:

```
ssh -i ~/.ssh/id_ed25519_ara YOUR_USERNAME@jbox.arawireless.org
```

Use the username displayed in *your* dashboard in place of `YOUR_USERNAME`. The first time you connect, SSH may ask you to confirm the host key. Type `yes`, and press Enter. 

A successful connection will open a shell on the ARA jumpbox. Run 

```
exit
```

in this shell to return to your local terminal.