```
Title:   vagrant-note
Author:  Xiaoxue Wang<xxwjoy@hotmail.com>
Date:    2019-04-22
Modify:  2019-05-09
         2019-05-23
```


<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
<!-- code_chunk_output -->

* [Vagrant Notes](#vagrant-notes)
	* [Vagrantfile](#vagrantfile)
		* [primary function of the Vagrantfile](#primary-function-of-the-vagrantfile)
		* [lookup order](#lookup-order)
		* [Load Order and Merging](#load-order-and-merging)
	* [How to package your changes to a box and distribute it?](#how-to-package-your-changes-to-a-box-and-distribute-it)
		* [Package with `vagrant box repackage`, not work(without changes).](#package-with-vagrant-box-repackage-not-workwithout-changes)
		* [Package with `vagrant package`, works(with changes).](#package-with-vagrant-package-workswith-changes)
		* [Package a box with vagrantfile](#package-a-box-with-vagrantfile)
	* [Box Management](#box-management)
		* [update box version (for box from repo)](#update-box-version-for-box-from-repo)
	* [make a box from vm instance](#make-a-box-from-vm-instance)
		* [VirtualBox as provider  -  vagrant package](#virtualbox-as-provider-vagrant-package)
			* [Package box](#package-box)
			* [Add rhel8-box to vagrant:](#add-rhel8-box-to-vagrant)
		* [libvirt as provider](#libvirt-as-provider)

<!-- /code_chunk_output -->


# Vagrant Notes

## Vagrantfile
https://www.vagrantup.com/docs/vagrantfile/

### primary function of the Vagrantfile
to describe the type of machine required for a project,
and how to configure and provision these machines.

Vagrant is meant to run with one Vagrantfile per project,

The syntax of Vagrantfiles is Ruby,



### lookup order

it will search the following paths in order for a Vagrantfile, until it finds one:

/home/mitchellh/projects/foo/Vagrantfile
/home/mitchellh/projects/Vagrantfile
/home/mitchellh/Vagrantfile
/home/Vagrantfile
/Vagrantfile


### Load Order and Merging
An important concept to understand is how Vagrant loads Vagrantfiles.
Vagrant actually loads a series of Vagrantfiles, `merging` the settings as it goes.
This allows Vagrantfiles of varying level of specificity to override prior settings.
Vagrantfiles are loaded in the order shown below.
Note that if a Vagrantfile is not found at any step, Vagrant continues with the next step.

1. Vagrantfile packaged with the box that is to be used for a given machine.
2. Vagrantfile in your Vagrant home directory (defaults to ~/.vagrant.d).
    This lets you specify some defaults for your system user.
3. Vagrantfile from the project directory. This is the Vagrantfile that you will be modifying most of the time.
4. Multi-machine overrides if any.
5. Provider-specific overrides, if any.

For most settings, this means that the newer setting overrides the older one.
However, for things such as defining networks, the networks are actually appended to each other.
By default, you should assume that settings will override each other.
If the behavior is different, it will be noted in the relevant documentation section.

Within each Vagrantfile, you may specify multiple Vagrant.configure blocks.
All configurations will be merged within a single Vagrantfile in the order they're defined.




## How to package your changes to a box and distribute it?

Use `vagrant package [name]`, it will package the local vm to a box named "package.box" by default.
Seems can't tag the version.
```
$ mkdir vagrant-packaging    <-- under any dir.
$ cd vagrant-packaging/      
$ vagrant box list           <-- list global boxes that had been added to this system.
bento/ubuntu-16.04 (virtualbox, 2.3.5)
rhel6-box          (virtualbox, 0)
rhel7-box          (virtualbox, 0)
rhel8-box          (virtualbox, 0)
roboxes/rhel8      (virtualbox, 1.9.6)
$
$ vagrant init rhel8-box       <-- init one base on rhel8-box (v0)
$ vi Vagrantfile               <-- generated just now
$ vagrant status
Current machine states:

default                   poweroff (virtualbox)

The VM is powered off. To restart the VM, simply run `vagrant up`
$
$ vagrant up                   <-- yes, named as 'default'
$ vagrant ssh                  <-- do some changes inside vm
$ vagrant halt                 <-- shut it down
$ vagrant box list
bento/ubuntu-16.04 (virtualbox, 2.3.5)
rhel6-box          (virtualbox, 0)
rhel7-box          (virtualbox, 0)
rhel8-box          (virtualbox, 0)
roboxes/rhel8      (virtualbox, 1.9.6)
$
```

### Package with `vagrant box repackage`, not work(without changes).
```
$ vagrant box repackage rhel8-box --help
Usage: vagrant box repackage <name> <provider> <version>
$
$ vagrant box repackage rhel8-box  virtualbox  0    <-- yes, v0, mean the box in box-list
$ ll
╭[localhost] ~/Work/vagrant-packaging
╰> ll
-rw-rw-r--. 1 joy joy 877810493 Apr  1 17:45 package.box
-rw-rw-r--. 1 joy joy      3016 Apr  1 17:34 Vagrantfile
$
$ vagrant box list             <-- still, the box list are unchanged.
╭[localhost] ~/Work/vagrant-packaging
╰> vagrant box add --name rhel8-box ./package.box
==> box: Box file was not detected as metadata. Adding it directly...
==> box: Adding box 'rhel8-box' (v0) for provider:
    box: Unpacking necessary files from: file:///home/joy/Work/vagrant-packaging/package.box
The box you're attempting to add already exists. Remove it before
adding it again or add it with the `--force` flag.

Name: rhel8-box
Provider: virtualbox
Version: 0
$ vagrant box add ...          <-- add, init, up for test, see no changes are included.
```


### Package with `vagrant package`, works(with changes).
```
╰> vagrant package --help
Usage: vagrant package [options] [name|id]

Options:

        --base NAME                  Name of a VM in VirtualBox to package as a base box (VirtualBox Only)
        --output NAME                Name of the file to output
        --include FILE,FILE..        Comma separated additional files to package with the box
        --vagrantfile FILE           Vagrantfile to package with the box
    -h, --help                       Print this help
╭[localhost] ~/Work/vagrant-packaging
╰> vagrant package default
==> default: Clearing any previously set forwarded ports...
==> default: Exporting VM...
==> default: Compressing package to: /home/joy/Work/vagrant-packaging/package.box
╭[localhost] ~/Work/vagrant-packaging
╰> ll
total 1704012
-rw-rw-r--. 1 joy joy 867088592 Apr  1 18:07 package.box
-rw-rw-r--. 1 joy joy 877810493 Apr  1 17:45 package.box-box-repackage
-rw-rw-r--. 1 joy joy      3016 Apr  1 17:34 Vagrantfile
╭[localhost] ~/Work/vagrant-packaging
╰> vagrant box add --name rhel8-box --box-version 0.1.1 ./package.box
==> box: Box file was not detected as metadata. Adding it directly...
You specified a box version constraint with a direct box file
path. Box version constraints only work with boxes from Vagrant
Cloud or a custom box host. Please remove the version constraint
and try again.
╭[localhost] ~/Work/vagrant-packaging
╰> vagrant box add --name rhel8-box ./package.box
==> box: Box file was not detected as metadata. Adding it directly...
==> box: Adding box 'rhel8-box' (v0) for provider:
    box: Unpacking necessary files from: file:///home/joy/Work/vagrant-packaging/package.box
The box you're attempting to add already exists. Remove it before
adding it again or add it with the `--force` flag.

Name: rhel8-box
Provider: virtualbox
Version: 0
╭[localhost] ~/Work/vagrant-packaging
╰> vagrant box add --name rhel8-box ./package.box --force
==> box: Box file was not detected as metadata. Adding it directly...
==> box: Adding box 'rhel8-box' (v0) for provider:
    box: Unpacking necessary files from: file:///home/joy/Work/vagrant-packaging/package.box
==> box: Successfully added box 'rhel8-box' (v0) for 'virtualbox'!

$ vagrant init rhel8-box       <-- to test if changes saved.
$ vagrant up                   <-- the changes above are inside this box.
```


### Package a box with vagrantfile

1. Example vagrantfile to package:

    ```
    # -*- mode: ruby -*-
    # vi: set ft=ruby :
    #
    # ==============================================================================
    # For rhel8, and also rhel7.5 and later(refer to this below Issue),
    #   https://github.com/projectatomic/adb-vagrant-registration/issues/126#issuecomment-380931941
    # Why this patch needed?
    #   Due to the output of "/usr/sbin/subscription-manager list --consumed" is
    #     changed from "No consumed subscription pools to list" (for rhel6 and rhel7 before rhel7.5)
    #     to "No consumed subscription pools were found." .
    #   While the `grep` string in `subscription_manager_registered?` is the older one
    #     so, the whole `vagrant-registration` part is skipped in `vagrant up` process.
    # Hence, this following patch block is added, since no fix are released.
    # -------------------------------------------------------------------------
    module SubscriptionManagerMonkeyPatches
      def self.subscription_manager_registered?(machine)
        true if machine.communicate.sudo("/usr/sbin/subscription-manager list --consumed --pool-only | grep -E '^[a-f0-9]{32}$'")
      rescue
        false
      end
    end

    VagrantPlugins::Registration::Plugin.guest_capability 'redhat', 'subscription_manager_registered?' do
      SubscriptionManagerMonkeyPatches
    end
    # ==============================================================================
    ```

2. package box with --vagrantfile:
    ```
    $ vagrant package default --vagrantfile Vagrantfile-rhsm-patch
    ```

3. After `box add`, the `Vagrantfile-rhsm-patch` is `include/_Vagrantfile`.

    ```
    ╭[dhcp-137-117] ~/.vagrant.d/boxes
    ╰> tree rhel8-box
    rhel8-box
    └── 0
        └── virtualbox
            ├── box-disk001.vmdk
            ├── box.ovf
            ├── include
            │   └── _Vagrantfile
            ├── master_id
            ├── metadata.json
            ├── Vagrantfile
            └── vagrant_private_key

    3 directories, 7 files
    ```


------------------------------------
## Box Management

### update box version (for box from repo)
https://www.vagrantup.com/docs/cli/box.html#box-update

`vagrant box update --box roboxes/rhel8 --provider virtualbox --insecure`

`--insecure` for some broken download.

When failed with following error, retry the update command.
**Seems** it can benifit from the last broken download data.

```
╰> vagrant box update --box roboxes/rhel8 --provider virtualbox
Checking for updates to 'roboxes/rhel8'
Latest installed version: 1.9.6
Version constraints: > 1.9.6
Provider: virtualbox
Updating 'roboxes/rhel8' with provider 'virtualbox' from version
'1.9.6' to '1.9.12'...
Loading metadata for box 'https://vagrantcloud.com/roboxes/rhel8'
Adding box 'roboxes/rhel8' (v1.9.12) for provider: virtualbox
Downloading: https://vagrantcloud.com/roboxes/boxes/rhel8/versions/1.9.12/providers/virtualbox.box
Download redirected to host: vagrantcloud-files-production.s3.amazonaws.com
An error occurred while downloading the remote file. The error
message, if any, is reproduced below. Please fix this error and try
again.

OpenSSL SSL_read: SSL_ERROR_SYSCALL, errno 104
╰> vagrant box update --box roboxes/rhel8 --provider virtualbox --insecure
```


## make a box from vm instance

### VirtualBox as provider  -  vagrant package

**Note:** vagrant package is for `VirtualBox Only`.
```bash
╰> vagrant package --help
Usage: vagrant package [options] [name|id]

Options:

        --base NAME                  Name of a VM in VirtualBox to package as a base box (VirtualBox Only)
        --output NAME                Name of the file to output
        --include FILE,FILE..        Comma separated additional files to package with the box
        --vagrantfile FILE           Vagrantfile to package with the box
    -h, --help                       Print this help
```

#### Package box
~~~
 1. $ cd /home/joy/VirtualBox VMs/rhel8_default_1553967195277_24844  (where the rhel8-box reside.)
 2. $ vagrant package --base rhel8_default_1553967195277_24844
 3. A package.box is generated:
 4. $ copy the `package.box` to ~/Documents/ for backup
~~~

#### Add rhel8-box to vagrant:
~~~
 $ vagrant box add --name rhel8-box ~/Documents/package.box  [--force]
 $ vagrant box list
~~~

### libvirt as provider

1. Do the normal setup for VM instance, and shutdown. eg. `rhel8-ga.qcow2`.

2. mkdir a new folder to contain the stuffs.
    `$ mkdir -p ~/Documents/rhel8-ga-box/libvirt/v1`

3. Add VM instance's image to folder.
   By default, it's at `/var/lib/libvirt/images/` .
	 In my env, it's put into another volume named `/home/joy/libvirt-vms/`.
	```bash
	╭[localhost] ~/Documents/rhel8-ga-box/libvirt/v1
	╰> sudo cp /home/joy/libvirt-vms/rhel8-ga.qcow2 .
	╭[localhost] ~/Documents/rhel8-ga-box/libvirt/v1
	╰> sudo chown joy:joy rhel8-ga.qcow2
	╭[localhost] ~/Documents/rhel8-ga-box/libvirt/v1
	╰> ll
	total 10487620
	-rw-------. 1 joy joy 10739318784 May 23 17:27 rhel8-ga.qcow2
	```

4. Create the necessary "metadata.json" file:
	 No idea about the mean of `virtual_size`.
	```json
	{
	"provider"     : "libvirt",
	"format"       : "qcow2",
	"virtual_size" : 40
	}
	```

5. Create the "Vagrantfile" file:
	```bash
	Vagrant.configure("2") do |config|
	       config.vm.provider :libvirt do |libvirt|
	       libvirt.driver = "kvm"
	       libvirt.host = 'localhost'
	       libvirt.uri = 'qemu:///system'
	       end
	config.vm.define "new" do |custombox|
	       custombox.vm.box = "custombox"
	       custombox.vm.provider :libvirt do |test|
	       test.memory = 1024
	       test.cpus = 1
	       end
	       end
	end
	```

6. (Skip for already being qcow2.)
   Now you have to convert your image file to qcow2 format:
   `sudo qemu-img convert -f raw -O qcow2 test.img ubuntu.qcow2`
	 Note: currently,libvirt-vagrant support only qcow2 format. So, don't change the format just rename to box.img, ecause it takes input with name box.img by default.

7. Rename the image to ".img" ending:
	```bash
	╭[localhost] ~/Documents/rhel8-ga-box/libvirt/v1
	╰> ll
	total 10487628
	-rw-rw-r--. 1 joy joy          78 May 23 17:38 metadata.json
	-rw-------. 1 joy joy 10739318784 May 23 17:27 box.img
	-rw-rw-r--. 1 joy joy         393 May 23 17:38 Vagrantfile
	```

8. Create the .box archive with all the created (3) files:
	```bash
	╭[localhost] ~/Documents/rhel8-ga-box/libvirt/v1
	╰> tar cvzf rhel8-ga-cus.box ./metadata.json ./Vagrantfile ./box.img
	./metadata.json
	./Vagrantfile
	./box.img
	╭[localhost] ~/Documents/rhel8-ga-box/libvirt/v1
	╰> ll -h
	total 11G
	-rw-------. 1 joy joy  11G May 23 17:27 box.img
	-rw-rw-r--. 1 joy joy   78 May 23 17:38 metadata.json
	-rw-rw-r--. 1 joy joy 635M May 23 17:41 rhel8-ga-cus.box
	-rw-rw-r--. 1 joy joy  393 May 23 17:38 Vagrantfile
	```

9. Add the box to vagrant:
	```bash
	╭[localhost] ~/Documents/rhel8-ga-box/libvirt/v1
	╰> vagrant box add --name rhel8-box-cus rhel8-ga-cus.box
	==> box: Box file was not detected as metadata. Adding it directly...
	==> box: Adding box 'rhel8-box-cus' (v0) for provider:
	    box: Unpacking necessary files from: file:///home/joy/Documents/rhel8-ga-box/libvirt/v1/rhel8-ga-cus.box
	==> box: Successfully added box 'rhel8-box-cus' (v0) for 'libvirt'!
	```

10. Test by vagrant init & up it:

	Failed to up the machine completely, but 50%.

	- The new VM instance is created.
	- VM's memory is 512M, cpu is 1, turn them up, and restart.
	- VM still run into emrgency mode, due to failed mounting /sysroot.
	- Testing stopped here ...

	```bash
	$ vagrant init rhel8-box-cus
	$ vagrant up --provider=libvirt
	Bringing machine 'default' up with 'libvirt' provider...
	==> default: Creating image (snapshot of base box volume).
	==> default: Creating domain with the following settings...
	==> default:  -- Name:              rhel8-box-cus_default
	==> default:  -- Domain type:       kvm
	==> default:  -- Cpus:              1
	==> default:  -- Feature:           acpi
	==> default:  -- Feature:           apic
	==> default:  -- Feature:           pae
	==> default:  -- Memory:            512M
	==> default:  -- Management MAC:    
	==> default:  -- Loader:            
	==> default:  -- Nvram:             
	==> default:  -- Base box:          rhel8-box-cus
	==> default:  -- Storage pool:      default
	==> default:  -- Image:             /home/joy/libvirt-vms/rhel8-box-cus_default.img (40G)
	==> default:  -- Volume Cache:      default
	==> default:  -- Kernel:            
	==> default:  -- Initrd:            
	==> default:  -- Graphics Type:     vnc
	==> default:  -- Graphics Port:     -1
	==> default:  -- Graphics IP:       127.0.0.1
	==> default:  -- Graphics Password: Not defined
	==> default:  -- Video Type:        cirrus
	==> default:  -- Video VRAM:        9216
	==> default:  -- Sound Type:
	==> default:  -- Keymap:            en-us
	==> default:  -- TPM Path:          
	==> default:  -- INPUT:             type=mouse, bus=ps2
	==> default: Creating shared folders metadata...
	==> default: Starting domain.
	==> default: Waiting for domain to get an IP address...
	==> default: Removing domain...
	/home/joy/.vagrant.d/gems/2.4.4/gems/fog-core-1.43.0/lib/fog/core/wait_for.rb:9:in `block in wait_for': The specified wait_for timeout (2 seconds) was exceeded (Fog::Errors::TimeoutError)
		from /home/joy/.vagrant.d/gems/2.4.4/gems/fog-core-1.43.0/lib/fog/core/wait_for.rb:6:in `loop'
	  ...
		from /opt/vagrant/embedded/gems/2.2.3/gems/vagrant-2.2.3/lib/vagrant/batch_action.rb:82:in `block (2 levels) in run'
	```

Refer to https://www.openattic.org/posts/how-to-create-a-vagrant-vm-from-a-libvirt-vmimage/ .
