```
Title:   vagrant-note
Author:  Xiaoxue Wang<xxwjoy@hotmail.com>
Date:    2019-04-22
```

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

