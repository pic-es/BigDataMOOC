Cloudera Quickstart VM installation instructions
================================================

Please use the following instructions to download and install the Cloudera Quickstart VM with VirutalBox.
The screenshots are from a Mac but the instructions should be the same for Windows. Please see the discussion boards if you have any issues.

1. Install VirtualBox. Go to https://www.virtualbox.org/wiki/Downloads to download and install VirtualBox for your computer.

2. Go to the Cloudera VMS downloads page from https://www.cloudera.com/downloads/quickstart_vms.html and download the file containing the VM. You have to complete some steps: 
    
    * Select VirtualBox platform
    
        ![select_platform](_static/select_platform.png) 
    
    * Click the "Get it now!" button
    
        ![get_it_now](_static/get_it_now.png)
    
    * Fill in form and click "Continue"
    
        ![fill_in_continue](_static/fill_in_continue.png)
        
    * Accept Terms and Conditions and click "Continue" to start the download.
    
        ![accept_TC_continue](_static/accept_TC_continue.png)
        
    The VM is over 4GB, so will take some time.

3. Unzip the Cloudera VM:

    Right-click cloudera-quickstart-vm-5.4.2-0-virtualbox.zip and select “Extract All…”

4. Start VirtualBox.

5. Begin importing. Import the VM by going to File -> Import Appliance

    ![import appliance](_static/1YHbnrvaEeWbLwqB7NyVNQ_18b3b1a489e3d9ce53e7b3975d38910a_Untitled.png)

6. Click the Folder icon.

    ![folder icon](_static/EUf7pLvbEeWHhw4MvaB3nw_98aed876336d826ba38b3ff967f59341_Untitled1.png)

7. Select the cloudera-quickstart-vm-X.X.X-0-virtualbox.ovf from the Folder where you unzipped the VirtualBox VM and click Open.

    ![ovf select](_static/kvXZY7vdEeW6FApX76Rguw_04212a7fd040cdd18258055596ba98a7_Untitled2.png)

8. Click Next to proceed.

    ![ovf_next](_static/05MjOLvdEeWHhw4MvaB3nw_d8ba793c18835387ddb02defba586569_Untitled3.png)

9. Click Import.

    ![ovf_import](_static/8ZNYCrvdEeWg-hLO0rEOAw_af0950df42ffc15de1631a512eb6aa46_Untitled4.png)

10. The virtual machine image will be imported. This can take several minutes.

    ![vm_import](_static/AoLTKrveEeWW3xLV17cwNw_b371ba33d261f8b00ac357da5590e2d6_Untitled5.png)

11. Launch Cloudera VM. When the importing is finished, the quickstart-vm-5.4.2-0 VM will appear on the left in the VirtualBox window. Select it and click the Start button to launch the VM.

    ![vm_launch](_static/HdSw4rveEeWg-hLO0rEOAw_8e77353aeafcc336742baf76aa647c8a_Untitled6.png)

12. Cloudera VM booting. It will take several minutes for the Virtual Machine to start. The booting process takes a long time since many Hadoop tools are started.

    ![vm_boot](_static/VKeShLveEeWHhw4MvaB3nw_bfb04aa6c0c0e0705514e617f45b1a86_Untitled7.png)

13. The Cloudera VM desktop. Once the booting process is complete, the desktop will appear with a browser.

    ![vm_desktop](_static/vlPlZruyEeWHhw4MvaB3nw_f128a6a6651d531d31a01f8c4ed79f53_vm-started.png)

14. Shutting down the Cloudera VM. Before we can change the settings for the Cloudera VM, the VM needs to be powered off. If the VM is running, click on System in the top toolbar, and then click on Shutdown:

	![vm_shutdown](_static/GsZrdF8SEeafuBI2oAYa8w_a598868bbbe0914586f3ee1f17313b71_shutdown.png)

15. Next, click on Shut down:

    ![vm_shutdown_bis](_static/DdZY018SEeafuBI2oAYa8w_8e1003755bdeb2ce175c3850e9cd0124_shutdown2.png)


